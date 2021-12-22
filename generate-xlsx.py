import os
import fnmatch
import xml.etree.ElementTree as et
import openpyxl as xl



tag_filter = {'text','visitedTooltip','undiscoveredTooltip','title','short','desc','tooltip','power','buttonText'}

def write_seg(name,text):
    if text == None or text == '\t': return
    xls.active.append([name,text])

def extract_text(root,segname):
    if root.tag in tag_filter: write_seg(segname,root.text)
    for node in root:
        if 'name' in node.attrib: segname=node.attrib['name']
        if node.tag in tag_filter: write_seg(segname,node.text)

        nodecnt=0
        for children in node:
            extract_text(children,segname+f"_{nodecnt}")
            nodecnt+=1


def iter_node(root):
    print("attrib:",root.attrib,"\ntext:",root.text,"\ntag:",root.tag,"\n")
    for node in root:
        print("attrib:",node.attrib,"\ntext:",node.text,"\ntag:",node.tag,"\n")

        for children in node:
            iter_node(children)

for file in os.listdir("./orig"):
    if fnmatch.fnmatch(file,"*.xml*"):
        print(f"parsing {file}...")
        xls=xl.workbook.Workbook()
        xls.active.append(["name","text"])
        xml=et.parse(f"./orig/{file}")
        xml_root = xml.getroot()
        #if fnmatch.fnmatch(file,"events*.xml*"):
        extract_text(xml_root,"")
        xls.save(filename=f'./xls/{file}.xlsx')
