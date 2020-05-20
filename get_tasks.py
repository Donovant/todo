#!/usr/bin/python3.6
# built-in imports
import json
import logging
from pprint import pprint # for debugging only
import sys

# external imports
import arrow

# user defined modules
import common.logger as logger

# Setup logging
to_do_log = logger.get_logger('logger', 'to_do.log')


def pull_todays_tasks():
    '''This function pulls the most recent version of task_json,
       obtains current system time, and compares it with the date(s)
       for each task.  If a task is due, it is appended to the 
       to_do_list.json file.'''
    ###  Import tasks here so we can pull any tasks that ###
    ###  have been added without restarting the program. ###
    from task_json import tasks

    # ts = int(time.time())
    curr_time = arrow.now('US/Mountain')
    current_time = curr_time.format('YYYY MM DD HH:mm')
    to_do_log.info("in pull function @ {}".format(curr_time))

    # arrow_time = arrow.get(ts)
    year = curr_time.format('YYYY')
    month = curr_time.format('MM')
    month_str = curr_time.format('MMMM')  # January, February, March ...
    day_of_month = curr_time.format('DD')
    day_of_week = curr_time.format('dddd')  # Monday, Tuesday, Wednesday ...

    for item in tasks:
        if day_of_month in tasks[item]['dom'] and month in tasks[item]['month'] and year in tasks[item]['year']:
            try:
                input_file = open('/home/dusr/code/to_do_list.json', 'r')
            except Exception as e:
                to_do_log.error(e)
            existing_to_do_list = input_file.read()
            input_file.close()
            if existing_to_do_list == '':
                existing_to_do_list = {}
            try:
                existing_to_do_list = json.loads(existing_to_do_list)
            except:
                existing_to_do_list = {}

            if not item in existing_to_do_list:
                date_str = "{} {}, {} ".format(month_str, day_of_month, year)
                new_task = {
                    item: {
                        "date": date_str,
                        "task": tasks[item]['name']
                    }
                }
                try:
                    output_file = open('/home/dusr/code/to_do_list.json', 'w')
                except Exception as e:
                    to_do_log.error(e)
                existing_to_do_list.update(new_task)
                output_file.write(json.dumps(existing_to_do_list))
                output_file.close()

                # date, task_id, created
    return


if __name__ == '__main__':
    pull_todays_tasks()
