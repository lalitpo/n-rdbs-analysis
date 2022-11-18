from datetime import datetime
from lxml import etree
import pandas as pd

print("Start Time =", datetime.now().strftime("%H:%M:%S"))

all_tree = etree.iterparse("../../resources/dblp.xml", events=('start', 'end'), dtd_validation=True, recover=True)
_, parent = next(all_tree)
start_tag = None

dblp = {}


def create_data(elem):
    for ent1 in elem.getchildren():
        if ((elem.tag == 'article' and ent1.tag in ['title', 'journal', 'volume', 'number', 'year']) or
                (elem.tag == 'proceedings' and ent1.tag in ['title', 'editor', 'volume', 'booktitle', 'year',
                                                            'publisher']) or
                (elem.tag == 'inproceedings' and ent1.tag in ['title', 'author', 'pages', 'booktitle', 'year'])):
            if elem.tag not in dblp:
                dblp[elem.tag] = {elem.attrib.get('key'): {ent1.tag: ent1.text}}
            else:
                dblp[elem.tag][elem.attrib.get('key')] = {ent1.tag: ent1.text}


for event, tree in all_tree:
    if tree.tag in ['article', 'proceedings', 'inproceedings']:
        if event == 'start' and start_tag is None:
            start_tag = tree.tag
            create_data(tree)
        if event == 'end' and tree.tag == start_tag:
            start_tag = None
            parent.clear()

"""article_attribute = set()
inproc_attribute = set()
proc_attribute = set()
for a_key, a_info in dblp['article'].items():
    for key in a_info:
        if key not in article_attribute:
            article_attribute.add(key)

print("article_attribute :", article_attribute)

for i_key, i_info in dblp['inproceedings'].items():
    for key in i_info:
        if key not in inproc_attribute:
            inproc_attribute.add(key)

print("inproc_attribute :", inproc_attribute)

for p_key, p_info in dblp['proceedings'].items():
    for key in p_info:
        if key not in proc_attribute:
            proc_attribute.add(key)

print("proc_attribute :", proc_attribute)"""

