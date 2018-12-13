import threading
import psycopg2
import os
import sys
import smtplib
import datetime
import gitlogtohtmlZhima
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
    repstrlist.append("fengshuo/zhima-android")
    repstrlist.append("xuliang/zhima-ios")
    repstrlist.append("root/zhima-new")
    repstrlist.append("root/zhima-web")

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

    print("conv utf8...")
    gitNameCmd = "cd D:/code/zhimacode/_gitlogutf8 && D: && for /r D:/code/zhimacode/_gitlog %i in (*.gitlog) do iconv.exe  -t UTF-8//IGNORE %i > %~ni.gitlog"
    nameret = os.popen(gitNameCmd).read()
    print(nameret)
    
    print('==================getsvnlog=====================')
    gitlogtohtmlZhima.gitcheck_fileFormat()
        
    print('==================getsvnlog=====================')
    os.system('D:/code/zhimacode/_gitloghtml/all.html')
    # ret = get_svnlog("G:\\行者易\\code\\智慧公交云平台\\web\\cloudPlatformWeb",start, end)


   
    global timer
    timer = threading.Timer(86400, fun_timer)
    timer.start()

def get_gitlog_new(gdir,gstarttime,gendtime):
    localdir = "D:/code/zhimacode/" + gdir
    locallogdir = "D:/code/zhimacode/_gitlog/"
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
                 " http://zhouyu:zhouyu@111.231.133.198:8080/git/{gitpath}.git ".format(dd=localdir[0:find_last(localdir,"/")], gitpath = gdir.lower())
        nameret = os.popen(gitNameCmd).read()
        print(nameret)

    print("checking pull ..." + gdir)
    gitNameCmd = "cd {dd} && D: &&git config --global i18n.logoutputencoding gbk  && git pull --all".format(dd=localdir)
    nameret = os.popen(gitNameCmd).read()
    print(nameret)

    print("checking log..." + gdir)
    gitNameCmd = "cd {dd} && D: &&git config --global i18n.logoutputencoding gbk  && git log  --all --after==\"{ss}\" " \
                 " > {logpath}".format(dd=localdir,ss=gstarttime,logpath = locallogpath)
    nameret = os.popen(gitNameCmd).read()
    print(nameret)
    namelist = list(set(nameret.replace('\'', '').split('\n')))
    namelist.sort()

    

    # for name in namelist:  # 循环输出列表值
    #     if (name is not ''):
    #         print(name)
    #         gitStatCmd="cd {dd} && G: &&git config --global i18n.logoutputencoding gbk&& git log --since =={ss} --until=={ee} " \
    #                " --author=\"{myname}\"  --pretty=tformat: --numstat ".format(dd=gdir,myname=name,ss=gstarttime,ee=gendtime)
    #         statret = os.popen(gitStatCmd).read()
    #         print(statret)
    return ""


def get_svnlog(gdir,gstarttime,gendtime):
    resultstr = ""
    print("SVN checking..." + gdir)
    svnNameCmd= "cd {dd} && G: && C:\\\"Program Files (x86)\"\\Subversion\\bin\\svn.exe log -r {{{ss}}}:{{{ee}}}  -v".format(dd=gdir,ss=gstarttime.replace('-', ''),ee=gendtime.replace('-', ''))
    svnret = os.popen(svnNameCmd).read()
    resultstr += svnret + "\n"
    print(svnret)
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
