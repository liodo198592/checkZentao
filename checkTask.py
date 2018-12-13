import threading
import pymysql
import os
import sys
import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

def get_task(gstarttime,gendtime):
    db = pymysql.connect("10.20.0.8", "zentaoread", "123", "zentao", charset='utf8' )
    cursor = db.cursor()
    resultstr =""

    print("==============任务跨度大于3天===========")
    resultstr += "==============任务跨度大于3天===========\n"
    print("====任务编号，任务名称，指派给，任务状态，开始时间，结束时间，任务持续时间===")
    resultstr += "====任务编号，任务名称，指派给，任务状态，开始时间，结束时间，任务持续时间===\n"
    #获取超时任务
    cursor.execute("select sub1.id as '任务编号' "
                   ", sub1.`name` as '任务名称', sub2.realname as '指派给', sub1.`status` as '任务状态' "
                   ", sub1.estStarted as '开始时间', sub1.deadline as '结束时间', sub1.difdays as '任务持续时间'"
                   " from (SELECT"
                   "	id,name,assignedTo,`status`,estStarted,deadline,datediff(t.deadline,t.estStarted) as difdays "
                   "FROM 	zt_task t WHERE 	t.`status` != 'closed' AND t.`status` != 'cancel' AND t.`status` != 'done' "
                   "AND t.`status` != 'pause' AND t.deleted != '1' and (datediff(t.deadline,t.estStarted) is null or datediff(t.deadline,t.estStarted) > "
                   "3) ) sub1 LEFT JOIN zt_user sub2 on sub1.assignedTo = sub2.account")
    data1 = cursor.fetchall()

    for row1 in data1:
        print(row1)
        resultstr = resultstr + "".join(str(row1)) + "\n"

    print("==============延期任务===========")
    resultstr += "==============延期任务===========\n"
    print("===任务ID，任务名称，指派给，任务状态，预期开始，预期结束，延误日期====")
    resultstr += "==============任务ID，任务名称，指派给，任务状态，预期开始，预期结束，延误日期===========\n"
    #获取任务延期
    cursor.execute("SELECT 	id,name,assignedTo,`status`,estStarted,deadline,datediff(t.deadline,t.estStarted) "
                   "FROM zt_task t WHERE t.`status` != 'closed' AND t.`status` != 'cancel'AND t.`status` != 'done' "
                   "AND t.`status` != 'pause' and t.deleted != '1' and (datediff(t.deadline,t.estStarted) is null or "
                   "datediff(t.deadline,t.estStarted) > 3) and t.deadline < '{ss}'".format(ss=gstarttime))
    data2 = cursor.fetchall()
    for row2 in data2:
        print(row2)
        resultstr = resultstr + "".join(str(row2)) + "\n"

    print("==============日报提交情况===========")
    resultstr += "==============日报提交情况===========\n"
    print("====任务ID，任务名称，任务状态，截止日期，填写日期，当天工时，剩余工时，提交人===")
    resultstr += "==============任务ID，任务名称，任务状态，截止日期，填写日期，当天工时，剩余工时，提交人===========\n"
    #获取日报提交情况
    cursor.execute("SELECT s.id AS '任务ID',s.`name` AS '任务名称',s.`status` AS '任务状态',s.deadline AS '截止日期',t.date"
                   " AS '填写日期',	t.consumed AS '当天工时',t.`left` AS '剩余工时',u.realname '提交人'	FROM zt_taskes"
                   "timate t LEFT JOIN zt_task s ON t.task = s.id  	LEFT JOIN zt_user u ON t.account = u.account WHERE "
                   "t.date = '{ss}' ".format(ss=gstarttime.replace('-', '')))
    data3 = cursor.fetchall()
    for row3 in data3:
        print(row3)
        resultstr = resultstr + "".join(str(row3)) + "\n"
    print("==============禅道未更新===========")
    resultstr += "==============禅道未更新===========\n"
    print("==姓名，提交人，当日提交次数===")
    resultstr += "=============姓名，提交人，当日提交次数===========\n"
    # 获取日报提交情况
    cursor.execute("SELECT 	u.realname , sub2.* FROM 	zt_user u  LEFT JOIN ( 	SELECT 		sub1.`提交人`, 		count(1) 	"
                   "FROM (	SELECT	s.id AS '任务ID',	s.`name` AS '任务名称',	s.`status` AS '任务状态',	s.deadline AS "
                   "'截止日期',	t.date AS '填写日期',	t.consumed AS '当天工时',	t.`left` AS '剩余工时',	u.realname"
                   " '提交人'	FROM	zt_taskestimate t	LEFT JOIN zt_task s ON t.task = s.id LEFT JOIN zt_user u"
                   " ON t.account = u.account WHERE 	t.date = '{ss}'	) sub1 GROUP BY 	sub1.`提交人` ) sub2 "
                   "ON u.realname = sub2.`提交人` WHERE 	u.`join` != '0000-00-00'  and u.realname not in "
                   "('admin','周宇','周金明','赵丽','朱旭光','韩祖渊','孙良良','李军','胡成露','韩晓春');".format(ss=gstarttime))
    data4 = cursor.fetchall()
    for row4 in data4:
        print(row4)
        resultstr = resultstr + "".join(str(row4)) + "\n"

    print("==============每个人都有任务===========")
    resultstr += "==============每个人都有任务===========\n"
    print("===姓名，当前任务数，最大任务时间==")
    resultstr += "==============姓名，当前任务数，最大任务时间===========\n"
    #检查是否每个人都有任务
    cursor.execute("select * from (select sub1.realname as '姓名', count(1) as '当前任务数' , MAX(sub1.deadline) as"
                   " '最大任务时间' from (SELECT t1.realname,t2.`name`, t2.id,t2.deadline,t1.`join` from zt_user t1 "
                   "LEFT JOIN (SELECT 	id,name,assignedTo,`status`,deadline FROM 	zt_task t WHERE t.`status` !="
                   " 'cancel' AND t.`status` != 'pause' and t.deadline != '0000-00-00' and t.deadline >= "
                   "DATE_ADD('{ss}',INTERVAL 1 DAY) and t.finishedBy = '' union ALL SELECT	id,name,finishedBy,"
                   "`status`,deadline FROM 	zt_task t WHERE t.`status` != 'cancel' AND t.`status` != 'pause' and t.deadline"
                   " != '0000-00-00' and t.deadline >= DATE_ADD('{ss2}',INTERVAL 1 DAY)  and t.finishedBy != '' )"
                   " t2 on t1.account = t2.assignedTo) sub1 where sub1.`join` != '0000-00-00' GROUP BY sub1.realname ) "
                   "sub2 where sub2.`姓名` not in  ('admin','周宇','周金明','赵丽','朱旭光','韩祖渊','孙良良','李军',"
                   "'胡成露','韩晓春'); ".format(ss=gstarttime,ss2=gstarttime))
    data5 = cursor.fetchall()
    for row5 in data5:
        print(row5)
        resultstr = resultstr + "".join(str(row5)) + "\n"

    #=======================================================
    db.close()
    return resultstr


gitrepolist = [
"G:\\行者易\\code\\大数据\\tranfic_data",
"G:\\行者易\\code\\工具\\服务转发（SRV）\\uitsk_srv_proxy",
"G:\\行者易\\code\\工具\\检修APP\\dev-android-overhaul-tool",
"G:\\行者易\\code\\工具\\检修工具（桌面）\\uits_tool",
"G:\\行者易\\code\\工具\\模拟程序\\uits_tool_sim",
"G:\\行者易\\code\\工具\\数据接入（DBProxy）\\uitsk_db_proxy",
"G:\\行者易\\code\\工具\\在线管理工具（manager）\\uits_tool_manage",
"G:\\行者易\\code\\工具\\自动调试工具\\dev-auto-debugging-tool",
"G:\\行者易\\code\\镇江客流\\web\\uits_web3",
"G:\\行者易\\code\\镇江客流\\web\\后台计算\\dataanalyze",
"G:\\行者易\\code\\镇江客流\\web\\后台计算\\datasync",
"G:\\行者易\\code\\智慧公交云平台\\后台计算\\back_calculate",
"G:\\行者易\\code\\智慧公交云平台\\后台计算\\base",
"G:\\行者易\\code\\智慧公交云平台\\后台计算\\data_access_jni",
"G:\\行者易\\code\\智慧公交云平台\\后台计算\\dataaccess",
"G:\\行者易\\code\\智慧公交云平台\\后台计算\\service_flow_calculate",
"G:\\行者易\\code\\算法\\new\\alg_release",
"G:\\行者易\\code\\算法\\new\\archive_model",
"G:\\行者易\\code\\算法\\new\\bus_documents",
"G:\\行者易\\code\\算法\\new\\door_state_detection_cpp",
"G:\\行者易\\code\\算法\\new\\labeltool",
"G:\\行者易\\code\\算法\\new\\model_executor",
"G:\\行者易\\code\\算法\\new\\ncnn",
"G:\\行者易\\code\\算法\\new\\passenger_statistics_cpp",
"G:\\行者易\\code\\算法\\new\\people_density_cpp",
"G:\\行者易\\code\\算法\\new\\xzy_alg_sdk",
"G:\\行者易\\code\\算法\\new\\xzy_cap",
"G:\\行者易\\code\\算法\\old\\darknet",
"G:\\行者易\\code\\算法\\old\\uits_alg_build",
"G:\\行者易\\code\\算法\\old\\uits_ccp",
"G:\\行者易\\code\\算法\\old\\uits_cnt",
"G:\\行者易\\code\\算法\\old\\uits_od",
"G:\\行者易\\code\\算法\\old\\uits_of",
"G:\\行者易\\code\\算法\\old\\uits_spt",
"G:\\行者易\\code\\嵌入式软件\\uits_apps2",
"G:\\行者易\\code\\嵌入式软件\\uits_drivers",
"G:\\行者易\\code\\嵌入式软件\\uits_linux2",
"G:\\行者易\\code\\嵌入式软件\\uits_stm32",
"G:\\行者易\\code\\嵌入式软件\\uits_sworker",
"G:\\行者易\\code\\嵌入式软件\\uits_tool_pack",
"G:\\行者易\\code\\嵌入式软件\\uitsk_mworker",
"G:\\行者易\\code\\嵌入式软件\\uitsk_rworker",
"G:\\行者易\\code\\嵌入式软件\\uitsk_worker",
"G:\\行者易\\code\\设备管理系统\\devmanage",
"G:\\行者易\\code\\南京地铁\\uits_web_metro",
"G:\\行者易\\code\\预研\\firenet",
"G:\\行者易\\code\\预研\\lpr",
"G:\\行者易\\code\\预研\\movidius"]

def fun_timer():
    sendStr = ""
    print('Hello zy!')
    sendStr =sendStr +  "Hello zy!\n"
    print (sys.getdefaultencoding())
    end = datetime.datetime.now().strftime('%Y-%m-%d')
    add_hour=datetime.datetime.now()+datetime.timedelta(days=-1)
    start =  add_hour.strftime('%Y-%m-%d')
    print('================get zentao task===============')
    sendStr = sendStr + "================get zentao task===============!\n"
    ret = get_task(start, end)
    sendStr = sendStr + ret + '\n'


    #send mail
    sender = 'zy@xingzheyi.com'
    receivers = ['zy@xingzheyi.com']
    message = MIMEText(sendStr, 'plain', 'utf-8')
    message['From'] = Header("周宇", 'utf-8')  # 发送者
    message['To'] = Header("周宇", 'utf-8')  # 接收者

    subject = '每日禅道代码检查' + start
    message['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect("smtp.xingzheyi.com","25")
    smtp.login("zy@xingzheyi.com", "Liodo1985923")
    smtp.sendmail("zy@xingzheyi.com", "zy@xingzheyi.com", message.as_string())
    smtp.quit()
    print("send success")
    global timer
    timer = threading.Timer(86400, fun_timer)
    timer.start()



timer = threading.Timer(1, fun_timer)
timer.start()
