Outline

##Dags

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

Log maintenance
Kill/Halt tasks when killed in the UI from webserver
DB instance and task maintenance
Decoupling code deployment with airflow deployment
