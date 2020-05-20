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

# external imports
from flask import Flask, abort, jsonify, Response
from webargs.flaskparser import parser, use_kwargs
from webargs import *


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.url_map.converters['version'] = dt_common.validators.VersionConverter

# Setup logging
index_log = dt_common.logger.get_logger('logger', 'to_do_index.log')

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

# Hardcoded account_id's
# TODO: Implement database to store this information
users = None
with open('users.json', 'r') as f:
    users = json.loads(f) 


@app.errorhandler(422)
def custom_handler(error):

    content_type = 'application/json; charset=utf8'
    index_log.info(error)
    errors = []

    for arg in error.data['messages']['query']:
        if isinstance(error.data['messages']['query'][arg], list):
            for item in error.data['messages']['query'][arg]:
                return Response(str(item), 400, mimetype=content_type)
        elif isinstance(error.data['messages']['query'][arg], dict):
            for item in error.data['messages']['query'][arg]:
                return Response(str(error.data['messages']['query'][arg][item]), 400, mimetype=content_type)

    return str(errors), 400


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
        assert str(kwargs['user_id']) in users, error[2]
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
def ack_chores(version, **kwargs):

    try:
        assert str(kwargs['user_id']) in users, error[2]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x003'])

    try:
        tasks = kwargs['task_ids']
        for item in tasks:
            assert int(item), error['01x008']
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error['01x007'])

    try:
        input_file = open('to_do_list.json', 'r')
    except Exception as e:
        index_log.error(e)

    existing_to_do_list = input_file.read()
    input_file.close()

    if existing_to_do_list == '':
        existing_to_do_list = {}

    try:
        existing_to_do_list = json.loads(existing_to_do_list)
    except:
        existing_to_do_list = {}

    for item in existing_to_do_list:
        if item not in tasks:
            new_task = {
                item: existing_to_do_list[item]
            }

            try:
                output_file = open('to_do_list.json', 'w')
            except Exception as e:
                index_log.error(e)
            existing_to_do_list.update(new_task)
            output_file.write(json.dumps(existing_to_do_list))
            output_file.close()

    if 'pp' in kwargs:
        tasks = json.loads(tasks)
        return jsonify(tasks)

    return tasks


@app.route('/user/<username>')
def show_user(username):
    return {'user': username}
