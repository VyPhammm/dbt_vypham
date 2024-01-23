import json
import os

PATH_DBT_PROJECT = "dags/dbt_sipher"

class StaticHtml():

    def __init__(self):
        self.search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'

    def run(self):
        with open(os.path.join(PATH_DBT_PROJECT, 'dbt_lineage','dbt_lineage.html'), 'r') as a:
            content_index = a.read()
            print(content_index)
        with open(os.path.join(PATH_DBT_PROJECT, 'target' , 'manifest.json'), 'r') as b:
            json_manifest = json.loads(b.read())
        with open(os.path.join(PATH_DBT_PROJECT, 'target' , 'catalog.json'), 'r') as c:
            json_catalog = json.loads(c.read())
        with open(os.path.join(PATH_DBT_PROJECT, 'dbt_lineage', 'dbt_lineage.html'), 'w') as f:
            new_str = "o=[{label: 'manifest', data: "+json.dumps(json_manifest)+"},{label: 'catalog', data: "+json.dumps(json_catalog)+"}]"
            new_content = content_index.replace(self.search_str, new_str)
            f.write(new_content)

    @classmethod
    def airflow_callable(cls):
        ins = cls()
        ins.run()