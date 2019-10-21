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
from flask import Flask, abort, jsonify
from flask_cors import CORS, cross_origin
from webargs.flaskparser import FlaskParser, use_kwargs
from webargs import *

# user defined modules
sys.path.insert(0, '/home/dusr/common')
import logger


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

# Hardcoded account_id's
# TODO: Implement database to store this information
users = None
with open('users.json', 'r') as f:
    users = json.loads(f) 


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
        print(error)
        errors.append('Invalid Request: task_ids required.')
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
def ack_chores(version, **kwargs):

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
        tasks = kwargs['task_ids']
        # tasks = kwargs['task_ids'].split(',')
        for item in tasks:
            print(item)
            assert int(item), error[8]
    except AssertionError as e:
        index_log.error(e)
        abort(400, e)
    except Exception as e:
        index_log.error(e)
        abort(400, error[7])

    try:
        input_file = open('to_do_list.json', 'r')
    except Exception as e:
        index_log.error(e)
        print(e)
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
            print("BP1", item)
            print("BP2", existing_to_do_list[item])

            new_task = {
                item: existing_to_do_list[item]
            }
            try:
                output_file = open('to_do_list.json', 'w')
            except Exception as e:
                to_do_log.error(e)
                print(e)
            existing_to_do_list.update(new_task)
            output_file.write(json.dumps(existing_to_do_list))
            output_file.close()


        else:
            print("COMPLETING {}".format(item))

    if 'pp' in kwargs:
        tasks = json.loads(tasks)
        return jsonify(tasks)

    return tasks


@app.route('/user/<username>')
# @cross_origin(origins='*')
def show_user(username):
    return 'user {}'.format(username)
