from datetime import datetime
from airflow import DAG
from utils.alerting.airflow import airflow_callback
from airflow_dbt.operators.dbt_operator import DbtDocsGenerateOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from utils.dbt import default_args_for_dbt_operators
from dbt_sipher.dbt_lineage.static_html import StaticHtml
from utils.common import set_env_value

DAG_START_DATE = set_env_value(
    production=datetime(2023, 10, 26), dev=datetime(2023, 10, 26)
)
DAG_END_DATE = set_env_value(production=None, dev=None)
DAG_SCHEDULE_INTERVAL = set_env_value(production="@once", dev="@once")

INDEX = StaticHtml()

DEFAULT_ARGS = {
    "owner": "vy.pham",
    "start_date": DAG_START_DATE,
    "end_date": DAG_END_DATE,
    "trigger_rule": "all_success",
    "on_failure_callback": airflow_callback,
}
DEFAULT_ARGS.update(default_args_for_dbt_operators)

with DAG(
    dag_id="dbt_lineage",
    default_args=DEFAULT_ARGS,
    schedule_interval=DAG_SCHEDULE_INTERVAL,
    tags=["dbt", "lineage"],
    catchup=False,
) as dag:
    
    # to_dbt_project = BashOperator(
    #     task_id='to_dbt_project',
    #     bash_command= CD_DBT_PROJECT,
    # )

    # dbt_docs_task = DbtDocsGenerateOperator(
    #     task_id='generate_docs',
    # )

    get_static_html = PythonOperator(
        task_id='get_static_html',
        dag=dag,
        provide_context=True,
        python_callable=INDEX.run
    )

    get_static_html