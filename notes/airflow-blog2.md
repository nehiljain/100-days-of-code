Outline

## Dags

### Parallelizing tasks?

It is very easy to parallelise tasks for a given dag that are not dependent on each other. This is benefitial for 2 reasons.
- remove unneccessary dependencies
- time to completion decreases

example: demo_dag file link

### Start date dynamic or static?

I used to always have static start dates as prescribed by [documention on airflow](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#less-forgiving-scheduler-on-dynamic-start_date), but reading more examples with days_ago made me realise the benifits and how start dates work. Link and description to documentation.

### Business logic/transformation logic in dag or outside?

### Utils,

dates is useful, days ago, parse_date

### Subdags

## Testing

Dags import testing

Testing dags help remove problems around syntax error etc in dags. Things that can be easily test are:
- can all the dags be imported
- verify all the dags that should be on production are the ones that scheduler can see
- there is now way i could figure out testing dag graph logic and retry logic for tasks.
-

Example tests folder


## Deployment and Maintenance

1. Python 3 or 2 or either?

In my experience I have found that airflow is written for python 3 compatibility and it is easier to work if your business logic is written in python 3 as well. It is not strictly required but it makes your life easier as a developer. For example, after you import airflow in your code, all the python 2 relevant functions are aliased as described in [Python Future Docs](http://python-future.org/standard_library_imports.html#standard-library-imports). The file in airflow codebase where this happens is [airflow/configuration.py](https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py#L35)


2. Log maintenance/cleanup?

Airflow has recently changed their logging module and made a lot of improvements. Give this [apace airflow update](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#logging-update) a quick read to understand the minutae.

3. Kill/Halt tasks when killed in the UI from webserver?

4. DB instance and task maintenance

5. Decoupling code deployment with airflow deployment
