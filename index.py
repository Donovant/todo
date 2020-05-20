'''
    This script serves as the backend to a to-do list app.
    The purpose of this script is to pull data (tasks) from a file.
    If a task has is to be performed on the current date, it is added
    to an active tasks list.  This script will also have the ability to
    accept requests to acknowledge that a task has been completed.
    Author: Donovan Torgerson
    Email: Donovan@Torgersonlabs.com
'''

# built-in imports
import json
import sys
from time import time

# external imports
import arrow
from flask import Flask, abort, jsonify, Response
from webargs.flaskparser import parser, use_kwargs
from webargs import *

# user-defined imports
from common import logger
from common import validators

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.url_map.converters['version'] = validators.VersionConverter

# Setup logging
index_log = logger.get_logger('logger', 'to_do_index.log')

# TODO: Make this its own file
# Dictionary of all errors for easier reuse.
error = {
    '01x001': 'Invalid version.',
    '01x002': 'User not found.',
    '01x003': 'Error validating user_id.',
    '01x004': 'Invalid Request: user_id must be a valid UUID.',
    '01x005': 'Invalid Request: user_id is required.',
    '01x006': 'Error retrieving task list.',
    '01x007': 'Error validating task_ids.',
    '01x008': 'Invalid task id. Task_ids must contain valid integer values.'
}

# Hardcode account_id's
# TODO: Implement database to store this information
users = None
f = open('users.json', 'r')
users = json.loads(f.read())

curr_date = arrow.now('US/Mountain').floor('day').timestamp
max_date = arrow.now('US/Mountain').floor('day').shift(days=30).timestamp


@app.errorhandler(422)
def custom_handler(error):

    content_type = 'application/json; charset=utf8'
    index_log.info(error)
    custom_errors = {}

    for arg in error.data['messages']:
        if isinstance(error.data['messages'][arg], list):
            for item in error.data['messages'][arg]:
                custom_errors[arg] = item

    return json.dumps(custom_errors), 400


get_chores_args = {
    "pp": fields.String(
        allow_missing=True,
        location="query",
        # error_messages={}
    ),
    "user_id": fields.UUID(
        required=True,
        location="query",
        error_messages={
            "null": error['01x004'],
            "required": error['01x005'],
            "invalid_uuid": error['01x004'],
            "type": error['01x004']
            # Unused error messages
            # "validator_failed": error['01x004'],
        }
    )
}


@app.route('/<version("v1.0"):version>/tsk/get/', methods=['GET'], strict_slashes=False)
@use_kwargs(get_chores_args)
def get_chores(version, **kwargs):

    try:
        assert str(kwargs['user_id']) in users, error['01x002']
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x003'])

    try:
        with open('to_do_list.json', 'r') as f:
            tasks = f.read()
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x006'])

    if 'pp' in kwargs:
        tasks = json.loads(tasks)
        return jsonify(tasks)

    return tasks


ack_chores_args = {
    "pp": fields.String(
        allow_missing=True,
        location="query",
        # error_messages={}
    ),
    "task_ids": fields.DelimitedList(
        fields.Str(),
        delimiter=',',
        required=True,
        location="query",
        error_messages={
            "null": error['01x008'],
            "required": error['01x008'],
            "invalid": error['01x008'],
            "type": error['01x008']
            # Unused error messages
            # "validator_failed": error['01x008'],
        }
    ),
    "user_id": fields.UUID(
        required=True,
        location="query",
        error_messages={
            "null": error['01x004'],
            "required": error['01x005'],
            "invalid_uuid": error['01x004'],
            "type": error['01x004']
            # Unused error messages
            # "validator_failed": error['01x004'],
        }
    )
}


@app.route('/<version("v1.0"):version>/tsk/ack/', methods=['GET'], strict_slashes=False)
@use_kwargs(ack_chores_args)
def ack_tasks(version, **kwargs):

    try:
        assert str(kwargs['user_id']) in users, error['01x002']
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x003'])

    try:
        task_ids = kwargs['task_ids']
        ack_task_count = len(task_ids)
        for item in task_ids:
            assert int(item), error['01x008']
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x007'])

    existing_tasks = {}
    try:
        with open('to_do_list.json', 'r') as f:
            existing_tasks = f.read()
        existing_tasks = json.loads(existing_tasks)
        assert existing_tasks != '', 'No tasks found.'
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x006'])

    tasks_removed = 0
    for item in task_ids:
        if item in existing_tasks:
            # Remove it
            existing_tasks.pop(item, None)
            tasks_removed += 1

    with open('to_do_list.json', 'w') as f:
        tasks = f.write(json.dumps(existing_tasks))

    if ack_task_count == tasks_removed:
        return "Success"
    elif tasks_removed > 0:
        return "Partial"
    else:
        return "Fail"


add_task_args = {
    "pp": fields.String(allow_missing=True, location="query"),
    "user_id": fields.UUID(required=True, location="query"),
    "task": fields.String(required=True, location="query"),
    "assigned_to_id": fields.UUID(allow_missing=True, location="query"),
    "task_date": fields.Int(allow_missing=True, location="query",
        validate=lambda td: curr_date <= td <= max_date),
    "private": fields.Bool(allow_missing=True, Default=False)
}


@app.route('/<version("v1.0"):version>/tsk/add/', methods=['GET'], strict_slashes=False)
@use_kwargs(add_task_args)
def add_task(version, **kwargs):

    try:
        assert str(kwargs['user_id']) in users, error[2]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x003'])

    assigned_to = kwargs.get('assigned_to_id', kwargs['user_id'])
    task_date = kwargs.get('task_date', curr_date)

    formatted_task_date = arrow.get(task_date).format('MM-DD-YYYY')

    tasks = {}
    try:
        with open('to_do_list.json', 'r') as f:
            tasks = f.read()
        tasks = json.loads(tasks)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x006'])

    custom_task_enum = 1000
    if tasks:
        while str(custom_task_enum) in tasks:
            custom_task_enum += 1

    curr_time = arrow.now('US/Mountain')
    current_time = curr_time.format('YYYY MM DD HH:mm')
    year = curr_time.format('YYYY')
    month = curr_time.format('MM')
    month_str = curr_time.format('MMMM')  # January, February, March ...
    day_of_month = curr_time.format('DD')

    date_str = "{} {}, {} ".format(month_str, day_of_month, year)
    new_task = {
        custom_task_enum:
        {
            "date": date_str,
            "task": kwargs['task']
        }
    }

    try:
        output_file = open('to_do_list.json', 'w')
    except Exception as e:
        index_log.error(e)

    try:
        tasks.update(new_task)
        output_file.write(json.dumps(tasks))
        output_file.close()
    except Exception as e:
        index_log.error(e)
        return {'status': 'fail'}

    return {'status': 'success'}


@app.route('/user/<username>')
def show_user(username):
    return {'user': username}

