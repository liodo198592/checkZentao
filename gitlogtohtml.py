'''
Created on 2016-1-25
 
@author: Mr.YF
'''
import os
import sys



def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position

 
def header():
    headerHtml = "<!DOCTYPE HTML PUBLIC -//W3C//DTD HTML 4.01 Transitional//EN \"http://www.w3.org/TR/html4/loose.dtd\"> \
        <html><head><title>Statistics Report for gitcheck.</title> \
        <meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\"> \
        <style type=text/css><!-- \
        body { \
         font-family: arial, helvetica, sans-serif; \
         font-size: 12px; \
         font-weight: normal;\
         color: black;\
         background: white;\
        }\
        th,td {\
         font-size: 10px;\
        }\
        h1 {\
         font-size: x-large;\
         margin-bottom: 0.5em;\
        }\
        h2 {\
         font-family: helvetica, arial;\
         font-size: x-large;\
         font-weight: bold;\
         font-style: italic;\
         color: #6020a0;\
         margin-top: 0em;\
         margin-bottom: 0em;\
        }\
        h3 {\
         font-family: helvetica, arial;\
         font-size: 16px;\
         font-weight: bold;\
         color: #b00040;\
         background: #e8e8d0;\
         margin-top: 0em;\
         margin-bottom: 0em;\
        }\
        li {\
         margin-top: 0.25em;\
         margin-right: 2em;\
        }\
        .hr {margin-top: 0.25em;\
         border-color: black;\
         border-bottom-style: solid;\
        }\
        .in    {color: #6020a0; font-weight: bold; text-align: left;}\
        .frontend {background: #e8e8d0;}\
        .s   {background: #e0e0e0;}\
        .a0  {background: #FF99CC; font-weight: bold;}\
        .a1  {background: #CCFF99;}\
        .a2  {background: #CCFFFF;}\
        .a3  {background: #CCCCFF;}\
        .a4  {background: #66CCCC;}\
        .a5  {background: #CCFF66;}\
        .a6  {background: #FFCC99;}\
        .maintain {background: #c07820;}\
        .rls      {letter-spacing: 0.2em; margin-right: 1px;}\
 \
        a.px:link {color: #ffff40; text-decoration: none;}\
        a.px:visited {color: #ffff40; text-decoration: none;}\
        a.px:hover {color: #ffffff; text-decoration: none;}\
        a.lfsb:link {color: #000000; text-decoration: none;}\
        a.lfsb:visited {color: #000000; text-decoration: none;}\
        a.lfsb:hover {color: #505050; text-decoration: none;}\
 \
        table.tbl { border-collapse: collapse; border-style: none;}\
        table.tbl td { text-align: right; border-width: 1px 1px 1px 1px; border-style: solid solid solid solid; padding: 2px 3px; border-color: gray; white-space: nowrap;}\
        table.tbl td.ac { text-align: center;}\
        table.tbl th { border-width: 1px; border-style: solid solid solid solid; border-color: gray;}\
        table.tbl th.pxname { background: #b00040; color: #ffff40; font-weight: bold; border-style: solid solid none solid; padding: 2px 3px; white-space: nowrap;}\
        table.tbl th.empty { border-style: none; empty-cells: hide; background: white;}\
        table.tbl th.desc { background: white; border-style: solid solid none solid; text-align: left; padding: 2px 3px;}\
 \
        table.lgd { border-collapse: collapse; border-width: 1px; border-style: none none none solid; border-color: black;}\
        table.lgd td { border-width: 1px; border-style: solid solid solid solid; border-color: gray; padding: 2px;}\
        table.lgd td.noborder { border-style: none; padding: 2px; white-space: nowrap;}\
        u {text-decoration:none; border-bottom: 1px dotted black;}\
        -->\
        </style></head><body><h1>GitCheck Center</h1><hr><h3>> General git information</h3>\
        <table border=0>"
    return headerHtml
 
def footer():
    footHtml = "</table></body></html>"
    return footHtml
 
def row():
    rowHtml = "<tr class=a%d><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
    return rowHtml
 
def indexMainRow():
    rowHtml = "<tr class=a0><td>ID</td><td>branch git log info.</td></tr>"
    return rowHtml
 
def indexRow():
    rowHtml = "<tr class=a%d><td>%d</td><td><a href=\"gitinfo/%s\">%s</a></td></tr>"
    return rowHtml
 
def tdClassId(pageId):
    pageId += 1
    if pageId >= 7:
        pageId = 1
    return pageId
 
def gitcheck(inFileName="gitcheck.in", outFileName="gitcheck.out.html"):
    fn = open(inFileName, "r",encoding="utf-8")
    fnOut = open(outFileName, "w",encoding="utf-8")
 
    fnOut.write(header())
    fnOut.write(row() % (0,"commit","Merge","Author","Date", "Comment","projectname","codenum"))
    lines = fn.readlines()
    beginTag = False
    pageId = 1
    goodLine = {0:"",1:"",2:"",3:"",4:"",5:inFileName[find_last(inFileName,"/")+1:inFileName.find(".")],6:""}
    for line in lines:
        if len(line) <= 2:
            continue
        if line.startswith("commit"):
            beginTag = True
            goodLine[0] = line[6:]
            pageId = tdClassId(pageId)
            continue
        if beginTag:
            if line.startswith("Merge: "):
                goodLine[1] = line[7:]
            elif line.startswith("Author: "):
                goodLine[2] = line[8:]
            elif line.startswith("Date: "):
                goodLine[3] = line[6:]
            elif line.startswith("codenum:"):
                goodLine[6] = line[8:]
            else :
                goodLine[4] = line
                beginTag = False
                fnOut.write(row() % (pageId,goodLine[0],goodLine[1],goodLine[2],goodLine[3],goodLine[4],goodLine[5],goodLine[6]))
                goodLine = {0:"",1:"",2:"",3:"",4:"",5:inFileName[find_last(inFileName,"/")+1:inFileName.find(".")],6:""}
    fn.close()
    fnOut.write(footer())
    fnOut.flush()
    fnOut.close()


def gitcheck_fileFormat():
    rootdir = 'D:/code/git/_gitlogutf8'
    fnOut = open("D:/code/git/_gitloghtml/all.html", "w",encoding="utf-8")
    fnOut.write(header())
    fnOut.write(row() % (0,"commit","Merge","Author","Date", "Comment","projectname","codenum")) 
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isfile(path):
            #你想对文件的操作
            fn = open(path, "r",encoding="utf-8")
            gitcheck_infile(fn,fnOut,path.replace("\\","/"))
            fn.close()
    fnOut.write(footer())
    fnOut.flush()
    fnOut.close()


def gitcheck_infile(fn,fnOut,inFileName):
    lines = fn.readlines()
    beginTag = False
    pageId = 1
    goodLine = {0:"",1:"",2:"",3:"",4:"",5:inFileName[find_last(inFileName,"/")+1:inFileName.find(".")],6:""}
    for line in lines:
        if "thiscommitisend" in line:
            beginTag = False
            fnOut.write(row() % (pageId,goodLine[0],goodLine[1],goodLine[2],goodLine[3],goodLine[4],goodLine[5],goodLine[6]))
            goodLine = {0:"",1:"",2:"",3:"",4:"",5:inFileName[find_last(inFileName,"/")+1:inFileName.find(".")],6:""}
        if len(line) <= 2:
            continue
        if line.startswith("commit"):
            beginTag = True
            goodLine[0] = line[6:]
            pageId = tdClassId(pageId)
            continue
        if beginTag:
            if line.startswith("Merge: "):
                goodLine[1] = line[7:]
            elif line.startswith("Author: "):
                goodLine[2] = line[8:]
            elif line.startswith("Date: "):
                goodLine[3] = line[6:]
            elif line.startswith("codenum:"):
                goodLine[6] = line[8:]
            else :
                goodLine[4] = line
               
 
def lsHtmls(dirName="gitinfo"):
    htmlFiles = []
    allFile = os.listdir(dirName)
    for f in allFile:
        if f.endswith(".html"):
            htmlFiles.append(f)
            print (f)
    return htmlFiles
 
def createIndex(dirName):
    files = lsHtmls(dirName)
    if len(files) > 0:
        fnOut = open("index.html", "w",encoding="utf-8")
        fnOut.write(header())
        fnOut.write(indexMainRow())
        pageId = 1
        ii = 1
        for f in files:
            fnOut.write(indexRow() % (ii, pageId, f, f))
            ii = tdClassId(ii)
            pageId += 1
        fnOut.write(footer());
        fnOut.close()
 
if __name__ == '__main__':
    # if len(sys.argv) >= 3:
    #     gitcheck(sys.argv[1], sys.argv[2])
    # elif len(sys.argv) >= 2:
    #     createIndex(sys.argv[1])
    gitcheck_fileFormat()