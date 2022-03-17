import os
import fnmatch
import xml.etree.ElementTree as et
import openpyxl as xl
import re

tags=set({'text', 'undiscoveredTooltip', 'power', 'desc', 'visitedTooltip', 'unvisitedTooltip', 'title', 'flavorType', 'short',"header","secretName","secretDescription"})
#NOTE: power에는 숫자 데이터도 있음.


def extract_text(root,segname):
    for node in root:
        if 'name' in node.attrib: segname=node.attrib['name']
        else: segname=''
        if node.text != None and node.text.strip()!="" and len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', node.text)) > 0:
            if node.tag not in tags:
                print(f"{node.tag}:{node.text}")
                tags.add(node.tag)

        nodecnt=0
        for children in node:
            extract_text(children,segname+f"_{nodecnt}")
            nodecnt+=1

for file in os.listdir("./kor"):
    if fnmatch.fnmatch(file,"*.xml*"):
        print(f"parsing {file}...")
        try:
            xml=et.parse(f"./kor/{file}")
            xml_root = xml.getroot()
            extract_text(xml_root,"")
        except et.ParseError as e:
            print(f"cannot parse {file}: {e.msg}")
            xls=None

print(tags)