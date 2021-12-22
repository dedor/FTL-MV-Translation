import os
import fnmatch
import xml.etree.ElementTree as et
import openpyxl as xl



tag_filter = {'text','visitedTooltip','undiscoveredTooltip','title','short','desc','tooltip','power','buttonText'}
xls_cnt=2
def rewrite_seg(node):
    global xls_cnt
    if node.text == None or node.text == '\t': return
    #print(node.text,"->",xls.active[xls_cnt][2].value)
    node.text=xls.active[xls_cnt][2].value
    xls_cnt+=1

def patch_text(root):
    if root.tag in tag_filter: rewrite_seg(root)
    for node in root:
        if node.tag in tag_filter: rewrite_seg(node)

        nodecnt=0
        for children in node:
            patch_text(children)
            nodecnt+=1


def iter_node(root):
    print("attrib:",root.attrib,"\ntext:",root.text,"\ntag:",root.tag,"\n")
    for node in root:
        print("attrib:",node.attrib,"\ntext:",node.text,"\ntag:",node.tag,"\n")

        for children in node:
            iter_node(children)

for file in os.listdir("./xls"):
    if fnmatch.fnmatch(file,"*.xlsx"):
        print(f"parsing {file[:-5]}...")
        xls=xl.load_workbook(filename="./xls/"+file,read_only=True,data_only=True)
        xml=et.parse(f"./orig/{file[:-5]}")
        xml_root = xml.getroot()
        #if fnmatch.fnmatch(file,"events*.xml*"):
        patch_text(xml_root)
        xml.write(f"./targ/{file[:-5]}",encoding='utf-8')   #FIXME: will not keep all the comments!
        print(f"write {file[:-5]}...")

