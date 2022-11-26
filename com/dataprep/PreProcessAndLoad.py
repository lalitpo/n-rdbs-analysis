from lxml import etree
from jproperties import Properties
import prestodb
import pandas as pd

start = 'start'
end = 'end'
all_tree = etree.iterparse("../../resources/dblp.xml", events=(start, end), dtd_validation=True, recover=True)
_, parent = next(all_tree)
start_tag = None

article = 'article'
proceedings = 'proceedings'
inproceedings = 'inproceedings'
article_list = []
inproc_list = []
proc_list = []

configs = Properties()
with open('../../resources/nrdbs.properties', 'rb') as read_prop:
    configs.load(read_prop)

article_attribute = configs.get("journal_article_tags").data
proc_attribute = configs.get("conf_proc_tags").data
inproc_attribute = configs.get("conf_article_tags").data


def add_elem(ent1, item):
    if ent1.tag in item.keys() and ent1.text is not None:
        item[ent1.tag] = item.get(ent1.tag) + "," + ent1.text
    else:
        item[ent1.tag] = ent1.text


def create_data(elem):
    item = dict()
    item['key'] = elem.attrib.get('key')
    for ent1 in elem.getchildren():
        if elem.tag == article and ent1.tag in article_attribute:
            add_elem(ent1, item)
            article_list.append(item)
        if elem.tag == proceedings and ent1.tag in proc_attribute:
            add_elem(ent1, item)
            proc_list.append(item)
        if elem.tag == inproceedings and ent1.tag in inproc_attribute:
            add_elem(ent1, item)
            inproc_list.append(item)


for event, tree in all_tree:
    if tree.tag in [article, inproceedings, proceedings]:
        if event == start and start_tag is None:
            start_tag = tree.tag
            create_data(tree)
        if event == end and tree.tag == start_tag:
            start_tag = None
            parent.clear()

dblp = {article: article_list, proceedings: proc_list, inproceedings: inproc_list}

article_df = (pd.DataFrame.from_dict(dblp[article]).dropna()).drop_duplicates()
inproc_df = (pd.DataFrame.from_dict(dblp[inproceedings])).drop_duplicates()
proc_df = (pd.DataFrame.from_dict(dblp[proceedings])).drop_duplicates()

DF_dict = {'journal_articles': article_df,
           'conference_articles': inproc_df,
           'conference_proceedings': proc_df}

presto_db_conn = prestodb.dbapi.connect(host='localhost',
                                        port=8080,
                                        user='lalit',
                                        catalog='postgres',
                                        schema='public')
cur = presto_db_conn.cursor()

exception_str = "Exception occurred because of query : "


def create_table(df_name, df_records):
    create_table_sql = ""
    try:
        create_table_sql = "CREATE TABLE " + df_name + " ( " + ', '.join(
            [s + " varchar" for s in df_records.columns.tolist()]) + ")"
        cur.execute(create_table_sql)
        cur.fetchone()
    except:
        print(exception_str, create_table_sql)


def insert_dframe_records(df_name, df_records):
    insert_sql = ""
    try:
        cols = ", ".join([str(i) for i in df_records.columns.tolist()])
        for i, record in df_records.iterrows():
            insert_sql = "INSERT INTO " + df_name + "(" + cols + ") VALUES " + "( " + ', '.join(
                ["'" + s.replace("'", "''") + "'" for s in tuple(record)]) + ")"
            cur.execute(insert_sql)
            cur.fetchone()
    except:
        print(exception_str, insert_sql)


for key in DF_dict:
    create_table(key, DF_dict[key])
    insert_dframe_records(key, DF_dict[key])
