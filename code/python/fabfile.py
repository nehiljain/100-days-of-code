#!/usr/bin/env python
from fabric.api import local
import pendulum

def uptime():
  local('uptime')

def hello():
    print('Hello from fab')

def date_args(from_date, to_date):
    parsed_from = pendulum.parse(from_date)
    parsed_to = pendulum.parse(to_date)
    print('types are {}, {}'.format(parsed_from, parsed_to))


def backfill_from_to_using_cmd(from_date, to_date, cmd):
    date_period = pendulum.parse(to_date) - pendulum.parse(from_date)
    for i in range(int(date_period.days)):
        run_date_str = pendulum.parse(from_date).add(days=i).to_date_string()
        local('{} {}'.format(cmd, run_date_str))


