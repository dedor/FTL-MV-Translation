import os
import fnmatch
import xml.etree.ElementTree as et
import openpyxl as xl



tag_filter = {'text', 'undiscoveredTooltip', 'power', 'desc', 'visitedTooltip', 'unvisitedTooltip', 'title', 'flavorType', 'short',"header","secretName","secretDescription","class"}

def write_seg(name,text,tag,attrib):
    if text == None or text.strip() == "" or text.isnumeric(): return ""#exclude numbers and blanks
    if tag not in tag_filter: return ""   #filter by tags

    if 'name' in attrib: name=attrib['name']
    else: name=''
    xls.active.append([text,"",name])   #["source","target","context","comments"]
    #print(text,name)
    return name

def extract_text(root,segname):
    segname = write_seg(segname,root.text,root.tag,root.attrib)
    for node in root:
        #print(f"{node.tag} : {node.text}")
        segname = write_seg(segname,node.text,node.tag,node.attrib)

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
        xls.active.append(["source","target","context","comments"])
        try:
            xml=et.parse(f"./orig/{file}")
            xml_root = xml.getroot()
            #if fnmatch.fnmatch(file,"events*.xml*"):
            #iter_node(xml_root)
            extract_text(xml_root,"")
            if xls.active.max_row > 1:
                xls.save(filename=f'./xls/{file}.xlsx')
            else:
                print(f"WARNING: no texts in {file}, did not write xlsx.")
        except et.ParseError as e:
            print(f"ERROR: cannot parse {file}: {e.msg}")
            xls=None

