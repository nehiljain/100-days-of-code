Outline

#TODO:

1. Check for jargons and definitions
2. Thing of adding why it matters for each point

The more experience I gain with airflow, the more I feel the need to consolidate and share the nuances of airflow with other developers who might benefit from it. In this post I write about some gotcha’s that consumed more than a couple hours during my time engineering data pipelines and workflows with Apache Airflow. This is a list of issues where the airflow system behaves differently than what you might expect or some tips which are beneficial to achieve long term success with airflow. You can read this like a selection of stackoverflow style posts where I pose a question and try to answer it with external links or code examples.


#### 1. Python Version for my project - py3 or py2?

Airflow is written for python 3 compatibility. It is a smooth ride if you can write your business logic in python 3 as well. It is not a strict requirement but it makes your life easier as a developer. For example, after you `import airflow` in your code, all the python 2 relevant functions are overwritten to python 3 counterparts as described in [Python Future Library Docs](http://python-future.org/standard_library_imports.html#standard-library-imports). The file in airflow codebase where this happens is [airflow/configuration.py](https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py#L35). Below is a code example to demonstrate this.

```
import sys

import math
print("Python Version {}".format(sys.version_info))
print("Math ceil function is built in: {} and returns {}".format(math.ceil, type(math.ceil(3.6))))

from airflow.models import DAG

print("Math ceil function is overridden {} and returns {}".format(math.ceil, type(math.ceil(3.6))))

```

#### 2. How to create different patterns found in workflows?

There are various types of workflows that can are common while writing airflow dags. Here I am sharing some code snippets to facilitate writing dags easily. I took slides from [Slides for DEVELOPING ELEGANT WORKFLOWS with Apache Airflow @ Europython 2017](https://ep2017.europython.eu/media/conference/slides/developing-elegant-workflows-in-python-code-with-apache-airflow.pdf) for inspiration.


The most common one is **sequential source to destination** dag.
![Dag Example1](https://i.imgur.com/s9xGkL6.png) Source: [Slides No 12](https://ep2017.europython.eu/media/conference/slides/developing-elegant-workflows-in-python-code-with-apache-airflow.pdf)

 <<code>>

**Tributaries** pattern
![Dag Example1](https://i.imgur.com/s9xGkL6.png) Source: [Slides No 12](https://ep2017.europython.eu/media/conference/slides/developing-elegant-workflows-in-python-code-with-apache-airflow.pdf)
 <<code>>

**Distributaries** pattern
![Dag Example1](https://i.imgur.com/s9xGkL6.png) Source: [Slides No 12](https://ep2017.europython.eu/media/conference/slides/developing-elegant-workflows-in-python-code-with-apache-airflow.pdf)
 <<code>>

### Should start date dynamic or static?

I started creating dags with static dates as prescribed by [documention on airflow](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#less-forgiving-scheduler-on-dynamic-start_date). This led to my dags having non-sensical start dates like `start_date: datetime(2016, 3, 20)`  but reading more examples with days_ago made me realise the benifits and how start dates work. The main concept to note is that Dag starts executing at start_date + schedule_interval.


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

dates : is useful, days ago, parse_date
apply_defaults : operator code
json : https://github.com/apache/incubator-airflow/blob/master/airflow/utils/json.py


## Testing

It is important to remind ourselves that the best practice is to keep Dags very light, i.e, keep the busniess logic away frmo airflow internals in their own module. This way they can be easily tested. For testing Dags and the config, following smoke tests and checks should provide reasonable reliability.
- Check if scheduler can import all the dags and parse them.
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

- Check that every dag has a owner that is not root and exists on the system
<< code required >>

- Check that dag files load fast enough else this will slow down scheduler heartbeat.
<< code required>>

- set DAG timeouts and SLA targets to be alerted if your DAGs run too slowly in production
- Also have tests done in different environements. Development is really small, just to see if it runs the way you expect, Test to take a representative sample of your data to do first sanity checks, Acceptance is a carbon copy of Production (if you have resources)

https://gist.github.com/criccomini/2862667822af7fae8b55682faef029a7

Example tests folder


## Deployment and Maintenance



2. Log maintenance/cleanup?

Airflow has recently changed their logging module and made a lot of improvements. Give this [apace airflow update](https://github.com/apache/incubator-airflow/blob/master/UPDATING.md#logging-update) a quick read to understand the minutae.

3. Kill/Halt tasks when killed in the UI from webserver?

4. DB instance and task maintenance

5. Deployements to airflow in production

The initial setup of required to get distributed airflow running in production was described in my previous blog. Give [this]() a read if you haven't.

First it is important to separate your code and logic from dags. This can be done by creating new operators, hooks and sensors. If that is not enough, create libraries that can be imported by code running on airflow.

Second separate deployment of Airflow infrastructure from code deployment. You do not need to redeploy airflow containers (assuming you have containerized deployments/services), this way your scheduler, webserver and workers can keep doing their work and new code can be dynamically added. To push update to your code and business logic used by airflow, I would recommend using shared file system mounted on the Airflow Container. I have been working in AWS cloud, so I would recomment using [AWS EFS](https://aws.amazon.com/blogs/aws/amazon-elastic-file-system-shared-file-storage-for-amazon-ec2/). It is easy to setup and mount to your server (ec2-instance). I will be writing a separate post with terraform code to describe the details of this.
[Gtoonstra's Article](https://gtoonstra.github.io/etl-with-airflow/deployments.html) on airflow also has some really great info. You should give it a read.


