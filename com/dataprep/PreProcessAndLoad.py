from lxml import etree
from jproperties import Properties

start = 'start'
end = 'end'
all_tree = etree.iterparse("../../resources/dblp.xml", events=(start, end), dtd_validation=True, recover=True)
_, parent = next(all_tree)
start_tag = None

article = 'article'
proceedings = 'proceedings'
inproceedings = 'inproceedings'
article_attribute = []
inproc_attribute = []
proc_attribute = []
article_list = []
inproc_list = []
proc_list = []

configs = Properties()
with open('../../resources/nrdbs.properties', 'rb') as read_prop:
    configs.load(read_prop)

prop_view = configs.items()

for prop in prop_view:
    if 'journal' in prop[0]:
        article_attribute = prop[1].data
    if 'conf_proc' in prop[0]:
        proc_attribute = prop[1].data
    if 'conf_article' in prop[0]:
        inproc_attribute = prop[1].data


def create_data(elem):
    item = dict()
    item['key'] = elem.attrib.get('key')
    for ent1 in elem.getchildren():
        if elem.tag == article and ent1.tag in article_attribute:
            item[ent1.tag] = ent1.text
            article_list.append(item)
        if elem.tag == proceedings and ent1.tag in proc_attribute:
            item[ent1.tag] = ent1.text
            proc_list.append(item)
        if elem.tag == inproceedings and ent1.tag in inproc_attribute:
            item[ent1.tag] = ent1.text
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

"""
article_attribute = set()
inproc_attribute = set()
proc_attribute = set()
for entries in article_list:
    for key, value in entries.items():
        if key not in article_attribute:
            article_attribute.add(key)

print("article_attribute :", article_attribute)

for entries in inproc_list:
    for key, value in entries.items():
        if key not in inproc_attribute:
            inproc_attribute.add(key)

print("inproc_attribute :", inproc_attribute)

for entries in proc_list:
    for key, value in entries.items():
        if key not in proc_attribute:
            proc_attribute.add(key)

print("proc_attribute :", proc_attribute)
"""
