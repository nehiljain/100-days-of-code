Outline

#TODO:
1. Check for jargons and definitions
2. Thing of adding why it matters for each point
3.



The more experience I gain with airflow, the more I feel the need to consolidate and share the nuances of airflow with al the others in their early stages of the journey. In this post I write about some gotcha's that consumed more than a couple hours of mine during my time engineering data pipelines with airflow. This is a list of issues that cause situations where the airflow system behaves differently than what you might expect.

## Dags

1. Should I care if my project is Py2 or Py3?

In my experience I have found that airflow is written for python 3 compatibility. It is a smooth ride if you can write your business logic in python 3 as well. It is not a strict requirement but it makes your life easier as a developer. For example, after you `import airflow` in your code, all the python 2 relevant functions are overwritten to python 3 counter parts as described in [Python Future Docs](http://python-future.org/standard_library_imports.html#standard-library-imports). The file in airflow codebase where this happens is [airflow/configuration.py](https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py#L35). Below an example of this unexpected behaviour.

```
import sys

import math
print("Python Version {}".format(sys.version_info))
print("Math ceil function is built in: {} and returns {}".format(math.ceil, type(math.ceil(3.6))))

from airflow.models import DAG

print("Math ceil function is overridden {} and returns {}".format(math.ceil, type(math.ceil(3.6))))

```



2. Can I easily parallelize tasks inside a dag?

It is very easy to parallelise tasks for a given dag that are not dependent on each other. This is benefitial for 2 reasons.
- removes unneccessary dependencies
- decreases time to completion


example: demo_dag code
```
dag = DAG(
    dag_id=DAG_ID,
    default_args=args,
    schedule_interval='*/5 * * * *')


stream1_task = PythonOperator(
    task_id='print_the_context_stream1',
    provide_context=True,
    op_kwargs={'stream': 1},
    python_callable=print_context,
    dag=dag)

stream2_task = PythonOperator(
    task_id='print_the_context_stream2',
    provide_context=True,
    op_kwargs={'stream': 2},
    python_callable=print_context,
    dag=dag)


start_task = DummyOperator(task_id='start_task',
                           dag=dag)

start_task.set_downstream([stream1_task, stream2_task])
```

### Should start date dynamic or static?

I used to always have static start dates as prescribed by [documention on airflow](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#less-forgiving-scheduler-on-dynamic-start_date), but reading more examples with days_ago made me realise the benifits and how start dates work. The main concept to note is that Dag starts executing at start_date + schedule_interval.


https://cwiki.apache.org/confluence/display/AIRFLOW/Common+Pitfalls
```
Using a start_date of datetime.now() can lead to unpredictable behavior, and your DAG never starting. See this post for details. It's recommended to subtract a timespan to force the scheduler to recognize the start_date. ***
```
```
When setting a schedule, align the start date with the schedule. If a schedule is to run at 2am UTC, the start-date should also be at 2am UTC
```
### Business logic/transformation logic in dag or outside?


Dags are hard to test. Because of the first point I made, I would advice to keep business logic away from the airflow dag configuration which should just import the modules and execute them based on the dependency graph defined.


### Utils,

dates is useful, days ago, parse_date


## Testing

Dags import testing

Testing dags help remove problems around syntax error etc in dags. Things that can be easily test are:
- can all the dags be imported
- verify all the dags that should be on production are the ones that scheduler can see
- there is now way i could figure out testing dag graph logic and retry logic for tasks.
-

Example tests folder
```
import os
from airflow.models import DagBag


def test_airflow_dagbag():
  print(os.getenv('AIRFLOW_HOME'))
  dagbag = DagBag(os.getenv('AIRFLOW_HOME'))
  assert dagbag.size() > 0
  report = dagbag.dagbag_report()
  dag_id_list = ['demo_dag']
  for dag_id in dag_id_list:
    assert dag_id in report
```

## Deployment and Maintenance



2. Log maintenance/cleanup?

Airflow has recently changed their logging module and made a lot of improvements. Give this [apace airflow update](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#logging-update) a quick read to understand the minutae.

3. Kill/Halt tasks when killed in the UI from webserver?

4. DB instance and task maintenance

5. Decoupling code deployment with airflow deployment
