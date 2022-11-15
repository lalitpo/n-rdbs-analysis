from datetime import datetime
from lxml import etree

print("Start Time =", datetime.now().strftime("%H:%M:%S"))

all_tree = etree.iterparse("../../../resources/dblp.xml", events=('start', 'end'), dtd_validation=True, recover=True)
_, parent = next(all_tree)
start_tag = None

dblp = {}


def create_data(elem):
    if elem.tag not in dblp:
        dblp[elem.tag] = {elem.attrib.get('key'): {'mdate': elem.attrib.get('mdate')}}
    else:
        dblp[elem.tag][elem.attrib.get('key')] = {'mdate': elem.attrib.get('mdate')}
    for ent1 in elem.getchildren():
        dblp[elem.tag][elem.attrib.get('key')][ent1.tag] = ent1.text


for event, tree in all_tree:
    if tree.tag in ['article', 'proceedings', 'inproceedings']:
        if event == 'start' and start_tag is None:
            start_tag = tree.tag
            create_data(tree)
        if event == 'end' and tree.tag == start_tag:
            start_tag = None
            parent.clear()

print('Length of article tags:', len(dblp['article']))
print('Length of inproceedings tags:', len(dblp['inproceedings']))
print('Length of proceedings tags:', len(dblp['proceedings']))

print("Finish Time =", datetime.now().strftime("%H:%M:%S"))
