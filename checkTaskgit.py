import threading
import psycopg2
import os
import sys
import smtplib
import datetime
import gitlogtohtml
from email.mime.text import MIMEText
from email.header import Header
from git import *


def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)



def get_task(gstarttime,gendtime):
    repstrlist = []
    conn = psycopg2.connect(database="stashdb", user="postgres", password="apassword@11", host="10.20.0.8", port="5432")
    cursor = conn.cursor()

    print("==============获取所有项目地址===========")
   
    #获取超时任务
    cursor.execute("SELECT 	p1.\"project_key\" as projectname,r1.\"slug\" as repname  FROM repository r1 LEFT JOIN project p1 ON r1.project_id = p1.\"id\";")
    data1 = cursor.fetchall()

    for row1 in data1:
        repstrlist.append(str(row1[0] + '/' + row1[1]))
    #=======================================================
    conn.close()

    print(repstrlist)
    return repstrlist



def fun_timer():
    sendStr = ""
    print('Hello zy!')
    sendStr =sendStr +  "Hello zy!\n"
    print (sys.getdefaultencoding())
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    add_hour=datetime.datetime.now()+datetime.timedelta(days=-7)
    start =  add_hour.strftime('%Y-%m-%d')

    gitrepolist = get_task(start, end)
    print('==================getgitlog=====================')
    
    for gname in gitrepolist:
        ret = get_gitlog_new(gname, start, end)
    #debug
    #ret = get_gitlog_new("ALG/xzy_alg_sdk", start, end)
        
    print('==================getsvnlog=====================')
    ret = get_svnlog("D:/code/svn/云平台WEB外网",start, end)


    print("conv utf8...")
    gitNameCmd = "cd D:/code/git/_gitlogutf8 && D: && for /r D:/code/git/_gitlog %i in (*.gitlog) do iconv.exe  -t UTF-8//IGNORE %i > %~ni.gitlog"
    nameret = os.popen(gitNameCmd).read()
    print(nameret)


    gitlogtohtml.gitcheck_fileFormat()
    os.system('D:/code/git/_gitloghtml/all.html')
   
    global timer
    timer = threading.Timer(86400, fun_timer)
    timer.start()

def get_gitlog_new(gdir,gstarttime,gendtime):
    localdir = "D:/code/git/" + gdir
    locallogdir = "D:/code/git/_gitlog/"
    locallogpath = locallogdir + gdir.replace("/","-") + '.gitlog'
    if not os.path.exists(localdir):
        os.makedirs(localdir)
    if not os.path.exists(locallogdir):
        os.makedirs(locallogdir)
    # del_file(locallogdir)

    if not os.listdir(localdir):  #判断文件夹是否为空
        os.rmdir(localdir)

        print("empity clone..." + gdir)
        gitNameCmd = "cd {dd} && D: &&git config --global i18n.logoutputencoding gbk  && git clone  " \
                 " http://ZhouYu:4152135347@10.20.0.8:7990/scm/{gitpath}.git ".format(dd=localdir[0:find_last(localdir,"/")], gitpath = gdir.lower())
        nameret = os.popen(gitNameCmd).read()
        print(nameret)

    print("checking pull ..." + gdir)
    gitNameCmd = "cd {dd} && D: &&git config --global i18n.logoutputencoding gbk  && git pull --all".format(dd=localdir)
    nameret = os.popen(gitNameCmd).read()
    print(nameret)


    print("checking log..." + gdir)
    gitNameCmd = "cd {dd} && D: &&git config --global i18n.logoutputencoding gbk  && git log  --all --numstat --after==\"{ss}\" ".format(dd=localdir,ss=gstarttime)
    nameret = os.popen(gitNameCmd).read()
    print(nameret)
    writestr = ""
    if nameret != '':
        lines = nameret.split('\n')
        newline = False
        isDoing = False
        addnum = 0
        remnum = 0
        for line in lines:
            if "Author:" in line:
                newline = True
            print(line)
            subcol = line.split('\t')
            if len(subcol) > 2 and newline is True:
                if subcol[0] != '-':
                    addnum += int(subcol[0])
                if subcol[1] != '-':
                    remnum += int(subcol[1])
                isDoing = True
            elif line == "" and isDoing is True:
                writestr += "codenum: " + str(addnum) + " , " + str(remnum) + " , " + str(remnum+addnum) + "\n"  + "thiscommitisend\n"
                addnum = 0
                remnum = 0
                isDoing = False 
                newline = False
            else:  
                writestr += line + "\n"

    fnOut = open(locallogpath, "w",encoding="gbk")
    fnOut.write(writestr)
    fnOut.flush()
    fnOut.close()
    
    return ""


def get_svnlog(gdir,gstarttime,gendtime):
    resultstr = ""
    print("SVN checking..." + gdir)
    svnNameCmd= "cd D:/code/svn/云平台WEB外网 && D: && D:/devenv/Apache-Subversion-1.10.3/bin/svn.exe log -r {{{ss}}}:{{{ee}}}  -v".format(dd=gdir,ss=gstarttime.replace('-', ''),ee=gendtime.replace('-', ''))
    svnret = os.popen(svnNameCmd).read()
    resultstr += svnret + "\n"
    print(svnret)
    #parse svn log
    writestr = "";
    lines = svnret.split('\n')
    nextisrow = False
    nextdesc = False
    for line in lines:
        if "----------------------------------------------------" in line:
            nextisrow = True
            continue
        if line == '':
            nextdesc = True
            continue
        if nextisrow is True:
            nextisrow = False
            listcol = line.split('|')
            writestr += "commit: " + listcol[0] + "\nMerge: \nAuthor: " + listcol[1] + "\nDate: " + listcol[2] + "\ncodenum: " + listcol[3] + "\n"
        if nextdesc is True:
            nextdesc = False
            writestr += line + "\n" + "thiscommitisend" + "\n"
    print(writestr)
    fnOut = open("D:/code/git/_gitlog/云平台web.gitlog", "w",encoding="gbk")
    fnOut.write(writestr)
    fnOut.flush()
    fnOut.close()
    return resultstr


def get_gitlog(gdir,gstarttime,gendtime):
    resultstr =""
    print("checking..." + gdir)
    resultstr += "checking..." + gdir + "\n"
    gitNameCmd = "cd {dd} && G: &&git config --global i18n.logoutputencoding gbk  && git log  --since =={ss} --until=={ee} " \
                 "  --format='%aN'".format(dd=gdir,ss=gstarttime,ee=gendtime)
    nameret = os.popen(gitNameCmd).read()
    namelist = list(set(nameret.replace('\'', '').split('\n')))
    namelist.sort()
    for name in namelist:  # 循环输出列表值
        if (name is not ''):
            print(name)
            gitStatCmd="cd {dd} && G: &&git config --global i18n.logoutputencoding gbk&& git log --since =={ss} --until=={ee} " \
                   " --author=\"{myname}\"  --pretty=tformat: --numstat ".format(dd=gdir,myname=name,ss=gstarttime,ee=gendtime)
            statret = os.popen(gitStatCmd).read()
            resultstr += statret + "\n"
            print(statret)
    return resultstr


timer = threading.Timer(1, fun_timer)
timer.start()
