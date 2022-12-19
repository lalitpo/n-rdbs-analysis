from lxml import etree
from jproperties import Properties
import prestodb
import pandas as pd
from sqlalchemy.engine import create_engine
import datetime

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
        if elem.tag == proceedings and ent1.tag in proc_attribute:
            add_elem(ent1, item)
        if elem.tag == inproceedings and ent1.tag in inproc_attribute:
            add_elem(ent1, item)
    if elem.tag == article:
        article_list.append(item)
    if elem.tag == proceedings:
        proc_list.append(item)
    if elem.tag == inproceedings:
        inproc_list.append(item)

print("process start",datetime.datetime.now())
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
inproc_df = (pd.DataFrame.from_dict(dblp[inproceedings]).dropna()).drop_duplicates()
proc_df = (pd.DataFrame.from_dict(dblp[proceedings]).dropna()).drop_duplicates()

DF_dict = {'journal_articles': article_df,
           'conference_articles': inproc_df,
           'conference_proceedings': proc_df}

print("inserting to db",datetime.datetime.now())

engine = create_engine('postgresql://admin:admin@localhost:5432/postgres')
for key in DF_dict:
    DF_dict[key].to_sql(key, engine)


print("inserting to db completed", datetime.datetime.now())
