'''
    This script serves as the backend to a to-do list app.
    The purpose of this script is to pull data (tasks) from a file.
    If a task has is to be performed on the current date, it is added
    to an active tasks list.  This script will also have the ability to
    accept requests/POST to acknowledge that a task has been completed.
    Author: Donovan Torgerson
    Email: Donovan@Torgersonlabs.com
'''
# built-in imports
import json
import sys
from time import time

# external imports
import arrow
from flask import Flask, abort, jsonify
from flask_cors import CORS, cross_origin
from webargs.flaskparser import FlaskParser, use_kwargs
from webargs import *

# user defined modules
import common.logger as logger


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
CORS(app)
# parser = webargs.flaskparser.parser()
parser = FlaskParser()

# Setup logging
index_log = logger.get_logger('logger', 'to_do_index.log')

# Dictionary of all errors for easier reuse.
error = {
    1: 'Invalid version.',
    2: 'User not found.',
    3: 'Error validating user_id.',
    4: 'Invalid Request: user_id must be a valid UUID.',
    5: 'Invalid Request: user_id is required.',
    6: 'Error retrieving task list.',
    7: 'Error validating task_ids.',
    8: 'Invalid task id. Task_ids must contain valid integer values.'
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
    index_log.info(error)
    errors = []
    if 'user_id' in error.data['messages']:
        if 'Not a valid UUID.' in error.data['messages']['user_id']:
            # return 'Invalid Request: user_id must be a valid UUID.', 400
            errors.append('Invalid Request: user_id must be a valid UUID.')
        if 'Missing data for required field.' in error.data['messages']['user_id']:
            # return 'Invalid Request: user_id is required.', 400
            errors.append('Invalid Request: user_id is required.')
    if 'task_ids' in error.data['messages']:
        errors.append('Invalid Request: task_ids required.')
    if 'task' in error.data['messages']:
        errors.append('Invalid Request: task is required.')
    if 'task_date' in error.data['messages']:
        errors.append('Invalid Request: task_date must be within the next 30 days (Including today).')
    return str(errors), 400


get_chores_args = {
    "pp": fields.String(allow_missing=True, location="query"),
    "user_id": fields.UUID(required=True, location="query")
}


@app.route('/<version>/tsk/get/', methods=['GET'], strict_slashes=False)
@cross_origin(origins='*')
@use_kwargs(get_chores_args)
def get_chores(version, **kwargs):

    if version != 'v1.0':
        abort(400, error[1])

    try:
        assert str(kwargs['user_id']) in users, error[2]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error[3])

    try:
        with open('to_do_list.json', 'r') as f:
            tasks = f.read()
    except Exception as e:
        index_log.error(e)
        abort(400, error[6])

    if 'pp' in kwargs:
        tasks = json.loads(tasks)
        return jsonify(tasks)

    return tasks


ack_chores_args = {
    "pp": fields.String(allow_missing=True, location="query"),
    "task_ids": fields.DelimitedList(fields.Str(), delimiter=',', required=True, location="query"),
    "user_id": fields.UUID(required=True, location="query")
}


@app.route('/<version>/tsk/ack/', methods=['GET'], strict_slashes=False)
@cross_origin(origins='*')
@use_kwargs(ack_chores_args)
def ack_tasks(version, **kwargs):

    if version != 'v1.0':
        abort(400, error[1])

    try:
        assert str(kwargs['user_id']) in users, error[2]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error[3])

    try:
        task_ids = kwargs['task_ids']
        ack_task_count = len(task_ids)
        for item in task_ids:
            assert int(item), error[8]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error[7])

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
        abort(400, error[6])

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


@app.route('/<version>/tsk/add/', methods=['GET'], strict_slashes=False)
@cross_origin(origins='*')
@use_kwargs(add_task_args)
def add_task(version, **kwargs):

    if version != 'v1.0':
        abort(400, error[1])

    try:
        assert str(kwargs['user_id']) in users, error[2]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error[3])

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
        abort(400, error[6])

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
        return 'Fail'

    return 'Success'


@app.route('/user/<username>')
# @cross_origin(origins='*')
def show_user(username):
    return 'user {}'.format(username)
