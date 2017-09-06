# -*-coding:utf-8-*-
import sys
import traceback
import shutil
from PackFunction import *
from ObjectAction import *

if len(sys.argv) == 1:
    print 'no argument found!'
    raise SystemExit

# 读取参数，作为绝对路径
initConfig(sys.argv[1])  # 程序入口立即读取配置
os.system("taskkill -f /im IEDriverServer.exe")

# 加载oracle驱动
import decimal

# tmpPath = CONFIG['ora_path'] + '\\oraocci11.dll'
# if os.path.exists(tmpPath):
#     print 'cx_Oracle add success!'
#     os.environ['PATH'] = CONFIG['ora_path'] + ';' + os.environ['PATH']
#     os.environ['TNS_ADMIN'] = CONFIG['ora_path']
#     os.environ['ORACLE_HOME'] = CONFIG['ora_path']
#     os.environ['NLA_LANG'] = "SIMPLIFIED CHINESE_CHINA.UTF8"
#     # os.environ['NLA_LANG']="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"
#     # time.sleep(1)
#     import cx_Oracle
#     import MySQLdb
# else:
#     print 'cx_Oracle not added'

# 清理图片
os.system("if exist " + CONFIG['path'] + "\\pic\\*.jpg del " + CONFIG['path'] + "\\pic\\*.jpg")
os.system("if exist " + CONFIG['path'] + "\\pic\\*.png del " + CONFIG['path'] + "\\pic\\*.png")

# 初始化
if CONFIG["logFile"] == "y":
    logging.basicConfig(level=CONFIG["logLevel"], format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename=CONFIG["path"] + "\\selenium.log", filemode="a")
else:
    logging.basicConfig(level=CONFIG["logLevel"], format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

if str.lower(CONFIG['debug']) == 'n':
    # ------------------------------------------------------------
    # 执行公共参数初始化
    # ------------------------------------------------------------
    global EX
    EX = ExecuteDb()
    print '>>>>>>>>>hello,welcome to Aissm-autotest<<<<<<<<<<'
    # 更改
    plan_batch_id = EX.get_PlanBatchId()
    templan_batch_id = EX.gettemp_PlanBatchId()

    # 增加自定义的debug级别15
    logging.addLevelName(15, "DEBUG")
    logging.info("config path in < " + CONFIG['path'] + " >")
    # 修改动态参数，用例执行转台pass为error，为方便失败循环执行的首次执行

    CONFIG["CaseStatus"] = "empty"  # 动态参数
    # 增加视频录制选项
    if CONFIG["capScreen"] == "y":
        tmpPath = "java -jar " + CONFIG['path'] + '\\video\\screen_recorder.jar ' + CONFIG['path'] + '\\video\\temp.cap'
        # print 'py_path:'+tmpPath
        # 需要异步启动录制屏幕
        subprocess.Popen(tmpPath, shell=True)
        logging.info("Screen is being captured,shell='" + tmpPath + "'")

    # ---------------------------------------------------------------
    # 判断如果是复测，先读取上次结果
    # ---------------------------------------------------------------
    lastResult = []
    if len(sys.argv) == 3 and sys.argv[2] == 'restart':
        with open(CONFIG['path'] + '\\result.txt', 'rb') as tmpV:
            for i in tmpV.readlines():
                if i.strip() != '':
                    lastResult.append(i)

    # ----------------------------------------------------------------
    # 读取配置文件判断运行模式，1是自定义命令模式，2是原声python脚本模式
    # ----------------------------------------------------------------
    if CONFIG['executeMode'] == 1:
        # 不支持
        print 'not support executeMode=1'
        raise SystemExit

    # ---------------------------------------------------------------
    # 导入执行列表
    # ---------------------------------------------------------------
    # 列入执行计划进行时
    EX.insert_Plan_Exec()
    # 导入前清理上次执行目录
    tmpPath = CONFIG['path'] + '\\temp\\'
    for script in os.listdir(tmpPath):
        if 'AT_SCRIPT' in script:
            os.remove(tmpPath + script)
    casespath = CONFIG['path'] + '\\cases\\'
    EX.plan_Import_Cases(casespath, tmpPath)

    # ----------------------------------------------------------------
    # 获取批量文件名并排序
    # ----------------------------------------------------------------
    tmpRun = os.listdir(tmpPath)
    runList = []
    for i in range(0, len(tmpRun)):
        if 'AT_SCRIPT_' in tmpRun[i]:
            runList.append(tmpRun[i])
    # 将列表中的元素（用例名称）按照'_'分割，取最后一个元素按升序排列
    runList.sort(key=lambda obj: obj.split('_')[-1], reverse=False)

    # -----------------------------------------------------------------
    # 执行前置处理器
    # -----------------------------------------------------------------
    tmpPath = CONFIG['path'] + '\\temp\\AT_BEFORE_TEST.py'
    try:
        with open(tmpPath, 'rb') as f0:
            tmpV = f0.read()
        tmpV.decode('utf-8')
    except UnicodeDecodeError:
        with codecs.open(tmpPath, 'rb', 'gbk') as f1:
            tmpText = f1.read()
        with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
            f2.write(tmpText)
    execfile(tmpPath)

    # ------------------------------------------------------------------
    # 执行前置函数
    # ------------------------------------------------------------------
    tmpPath = CONFIG['path'] + '\\temp\\AT_BEFORE_TEST_FUNC.py'
    try:
        with open(tmpPath, 'rb') as f0:
            tmpV = f0.read()
        tmpV.decode('utf-8')
    except UnicodeDecodeError:
        with codecs.open(tmpPath, 'rb', 'gbk') as f1:
            tmpText = f1.read()
        with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
            f2.write(tmpText)
    execfile(tmpPath)

    # ------------------------------------------------------------------
    # 更新计划执行进度
    # ------------------------------------------------------------------
    EX.update_Plan_Exec()

    # 判断如果重测场景，判断上次测试数量与本次测试数量是否一致，（正常情况下，这个判断应该不会满足，之前有处理过result.txt）
    if len(sys.argv) == 3 and sys.argv[2] == "restart" and len(lastResult) != len(runList) and len(lastResult) > 0:
        print 'lastResult:' + str(len(lastResult))
        print 'runList:' + str(len(runList))
        logging.info('上次结果数量与本次测试数量不等，不能重测，程序退出！'.decode('utf-8').encode('gbk'))
        # ******************/更新计划执行进度/失败*********************
        EX.update_Plan_Exec(4)
        # ******************/更新计划执行进度/失败*********************
        raise SystemExit
    if len(lastResult) == 0:
        logging.info('上次测试结果数量为0，重测过程将执行全量测试'.decode('utf-8').encode('gbk'))

    # 执行前清空结果文件，结果文件用户记录执行完毕后输出测试结果
    tmpPath = CONFIG['path'] + '\\result.txt'
    with open(tmpPath, 'w') as f1:
        f1.write('')

    # 这步try是为了测试文件编码，文件是utf-8的话则直接执行，否则转换
    iCountResult = 0
    for iFile in runList:
        tmpPath = CONFIG['path'] + '\\temp\\' + iFile
        CONFIG['curCaseFile'] = iFile
        global ResInfo
        ResInfo = {}
        caseid = str(int(iFile[-7:-3]))
        tmpsql = "select loop_number from tbl_plan_case_rel where plan_id='" + EX.plan_id + "' and case_id='" + caseid + "' and nodefunc_type='CASE'"
        loop_number = EX.DB.getSqlFirst(tmpsql)
        try:
            with open(tmpPath, 'rb') as f0:
                tmpV = f0.read()
            tmpV.decode('utf-8')
        except UnicodeDecodeError:
            with codecs.open(tmpPath, 'rb', 'gbk') as f1:
                tmpText = f1.read()
            with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
                f2.write(tmpText)
        # 开始流程判断
        if CONFIG["stopOnError"] == "y":
            execfile(CONFIG['path'] + "\\temp\\AT_BEFORE_CASE.py")
            execfile(CONFIG['path'] + '\\temp\\' + iFile)
            execfile(CONFIG['path'] + "\\temp\\AT_AFTER_CASE.py")
            endCase(CONFIG['CaseNumber'], 1)
        else:
            # 传入参数为restart，并且上次结果为pass，本次脚本不执行，如果执行
            if len(sys.argv) == 3 and sys.argv[2] == "restart" and len(lastResult) > 0 and lastResult[iCountResult][
                                                                                          0:4] == 'pass':
                # 复测流程，不执行任何代码
                pass
            else:
                # 单个用例失败重执行，取值循环次数
                CONFIG["CaseNumber"] = "caseid"
                CONFIG["CaseStatus"] = "empty"
                for i in range(int(loop_number)):
                    if CONFIG["CaseStatus"] == "pass":
                        break
                    else:
                        try:
                            if i == 0:
                                logging.info("get batch_id  - before before_case...")
                                # 首次执行需要获取batch_id
                                batch_id = EX.get_BatchId(caseid)
                                logging.info("caseid:"+caseid+"-"+"batch_id:"+batch_id)

                            else:
                                logging.info("update DataResult status:2  - before before_case...")
                                # 循环执行时需要执行状态
                                EX.update_DataResult(False)

                            try:
                                errflag = False
                                tmpsql = "select stream_attr from tbl_case_def where project_id='"+EX.project_id+"' and eparchy_code='"+EX.eparchy_code+"' and case_id='"+caseid+"'"
                                stream_attr = EX.DB.getSqlFirst(tmpsql)
                                if stream_attr == "0":# 0:正常流，但需要获取数据，有后台校验
                                    logging.info("get data resource begin...")
                                    ResInfo = EX.DB.getByCase(caseid)
                                    logging.info("data resource:" + str(ResInfo))
                                    logging.info("get data resource end ...")

                                elif stream_attr == "1":# 1:正常流，但需获取数据，无后台校验
                                    logging.info("get data resource begin...")
                                    ResInfo = EX.DB.getByCase(caseid)
                                    logging.info("data resource:" + str(ResInfo))
                                    logging.info("get data resource end ...")

                                elif stream_attr =="2":# 2:正常流，无需获取数据，有后台校验
                                    logging.info("Do not need to get data resource...continue")

                                elif stream_attr =="3":# 3:正常流，无需获取数据，无后台校验
                                    logging.info("gDo not need to get data resource...continue")

                                elif stream_attr =="4":# 4:异常流，需获取数据，无后台校验
                                    logging.info("get data resource begin...")
                                    ResInfo = EX.DB.getByCase(caseid)
                                    logging.info("data resource:" + str(ResInfo))
                                    logging.info("get data resource end ...")

                            except Exception, e:
                                logging.exception(e)
                                errflag = True
                            finally:
                                if stream_attr in ('0','1','4') and ResInfo == {}:
                                    CONFIG["CaseStatus"] = "fail"
                                    begin_time = EX.getCurrentTime()
                                    if errflag == False:
                                        errinfo = '读取资源池数据为空<失败>'
                                    else:
                                        errinfo = '读取资源池数据出现异常<失败>'
                                    tempsql = "insert into tbl_fk_weblogs values('" + plan_batch_id + "','" + batch_id + "','" + caseid + "','0','读取资源池数据','" + errinfo + "','" + begin_time + "','" + begin_time + "','0','" + EX.log_type + "','" + EX.project_id + "','" + EX.eparchy_code + "','" + EX.extend_col + "')"
                                    logging.info(tempsql.decode('utf-8').encode('gbk'))
                                    EX.DB.dbwSql(tempsql)
                                    logging.info(
                                        "用例".decode('utf-8').encode('gbk') + caseid + errinfo.decode('utf-8').encode(
                                            'gbk') + "，请检查".decode('utf-8').encode('gbk'))
                                    # raise e
                                else:
                                    execfile(CONFIG['path'] + "\\temp\\AT_BEFORE_CASE.py")
                                    execfile(tmpPath)
                        except Exception, e:
                            # 设置case状态为error，并判断执行流程
                            logging.exception(e)
                            tmpPathErr = str(e)
                            CONFIG["CaseStatus"] = "error"
                            # setOutput(tmpPathErr)
                            endVideo()
                            logging.info("config value of 'stopOnError' is 'n',process continue")
                            tempath = CONFIG['path'] + '\\temp\\AT_ERROR_CASE.py'
                            execfile(tempath)
                        try:
                            execfile(CONFIG['path'] + "\\temp\\AT_AFTER_CASE.py")
                        except Exception, e:
                            logging.exception(e)
                            logging.info("run AT_AFTER_CASE error!")
                        if CONFIG["CaseStatus"] != "pass":
                            endCase(CONFIG['CaseNumber'], {}, 1)
                        if errflag == True:
                            break
        iCountResult += 1

elif str.lower(CONFIG['debug']) == 'y':
    tmpPath = CONFIG['path'] + '\\temp\\'
    # ******************/导入执行列表/*********************
    # 导入前清理上次执行目录
    for script in os.listdir(tmpPath):
        if 'AT_SCRIPT' in script:
            os.remove(tmpPath + script)
    casespath = CONFIG['path'] + '\\cases\\'
    # ******************/导入执行列表/*********************
    for script in os.listdir(casespath):
        if 'AT_SCRIPT' in script:
            shutil.copyfile(casespath + script, tmpPath + script)

    tmpRun = os.listdir(tmpPath)
    runList = []
    for i in range(0, len(tmpRun)):
        if 'AT_SCRIPT_' in tmpRun[i]:
            runList.append(tmpRun[i])
    runList.sort()

    # 执行前置处理器
    tmpPath = CONFIG['path'] + '\\temp\\AT_BEFORE_TEST.py'
    try:
        with open(tmpPath, 'rb') as f0:
            tmpV = f0.read()
        tmpV.decode('utf-8')
    except UnicodeDecodeError:
        with codecs.open(tmpPath, 'rb', 'gbk') as f1:
            tmpText = f1.read()
        with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
            f2.write(tmpText)
    execfile(tmpPath)
    # 编译封装函数
    tmpPath = CONFIG['path'] + '\\temp\\AT_BEFORE_TEST_FUNC.py'
    try:
        with open(tmpPath, 'rb') as f0:
            tmpV = f0.read()
        tmpV.decode('utf-8')
    except UnicodeDecodeError:
        with codecs.open(tmpPath, 'rb', 'gbk') as f1:
            tmpText = f1.read()
        with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
            f2.write(tmpText)
    execfile(tmpPath)
    # 执行前清空结果文件，结果文件用户记录执行完毕后输出测试结果
    tmpPath = CONFIG['path'] + '\\result.txt'
    with open(tmpPath, 'w') as f1:
        f1.write('')

    # 这步try是为了测试文件编码，文件是utf-8的话则直接执行，否则转换
    iCountResult = 0
    for iFile in runList:
        tmpPath = CONFIG['path'] + '\\temp\\' + iFile
        CONFIG['curCaseFile'] = iFile
        # caseid=str(int(iFile[-7:-3]))
        try:
            with open(tmpPath, 'rb') as f0:
                tmpV = f0.read()
            tmpV.decode('utf-8')
        except UnicodeDecodeError:
            with codecs.open(tmpPath, 'rb', 'gbk') as f1:
                tmpText = f1.read()
            with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
                f2.write(tmpText)
        # 开始流程判断
        if CONFIG["stopOnError"] == "y":
            execfile(CONFIG['path'] + "\\temp\\AT_BEFORE_CASE.py")
            execfile(CONFIG['path'] + '\\temp\\' + iFile)
            execfile(CONFIG['path'] + "\\temp\\AT_AFTER_CASE.py")
            endCase(CONFIG['CaseNumber'], 1)
        else:
            # 传入参数为restart，并且上次结果为pass，本次脚本不执行，如果执行
            if len(sys.argv) == 3 and sys.argv[2] == "restart" and len(lastResult) > 0 and lastResult[iCountResult][
                                                                                           0:4] == 'pass':
                # 复测流程，不执行任何代码
                pass
            else:
                # 单个用例失败重执行，取值循环次数
                CONFIG["CaseNumber"] = "caseid"
                CONFIG["CaseStatus"] = "empty"
                if CONFIG["CaseStatus"] == "pass":
                    break
                else:
                    pass
                try:
                    execfile(CONFIG['path'] + "\\temp\\AT_BEFORE_CASE.py")
                    execfile(tmpPath)
                except Exception, e:
                    # 设置case状态为error，并判断执行流程
                    logging.exception(e)
                    tmpPathErr = str(e)
                    #                        if type(tmpPathErr)!=gbk and type(tmpPathErr)!=unicode:
                    #                             tmpPathErr.decode('utf-8')
                    #                         print tmpPathErr
                    CONFIG["CaseStatus"] = "error"
                    # setOutput(tmpPathErr)
                    # endVideo()
                    logging.info("config value of 'stopOnError' is 'n',process continue")
                    tempath = CONFIG['path'] + '\\temp\\AT_ERROR_CASE.py'
                try:
                    execfile(CONFIG['path'] + "\\temp\\AT_AFTER_CASE.py")
                except Exception, e:
                    logging.exception(e)
                    logging.info("run AT_AFTER_CASE error!")

        iCountResult += 1

# 结束测试后关闭录像
endVideo()

# 判断是否转换图片
if CONFIG['ConvertJpg'] == "y":
    tmpPath = CONFIG['path']
    os.system("if exist " + tmpPath + "\\pic\\*.jpg del " + tmpPath + "\\pic\\*.jpg")
    os.system(tmpPath + "\\ocr\\nconvert -D -quiet -out jpeg " + tmpPath + "\\pic\\*.png")

# 转换结果文件为gbk编码，否则excel获取乱码，传入参数为web，则不需要转换
tmpPath = CONFIG['path'] + '\\result.txt'
if len(sys.argv) == 2:
    try:
        with codecs.open(tmpPath, 'rb', 'utf-8') as f1:
            tmpText = f1.read()
        with codecs.open(tmpPath, 'wb', 'gbk') as f2:
            f2.write(tmpText)
    except Exception, e:
        print 'encode not needed'
elif len(sys.argv) == 3 and sys.argv[2] == "restart" and len(lastResult) > 0 and len(lastResult) == len(runList):
    # 仅在上次测试数量和本次测试数量一致的情况下，才合并上次和本次的测试结果
    nowResult = []
    f1 = open(tmpPath, 'rb')
    for i in f1.readlines():
        if i.strip() != '':
            nowResult.append(i)
    nowResult.reverse()
    for i in range(len(lastResult)):
        if lastResult[i][0:4] != 'pass':
            lastResult[i] = nowResult.pop()
    f1.close()
    f1 = open(tmpPath, 'wb')
    # print lastResult
    f1.write(''.join(lastResult))
    f1.close()

# 执行后置处理器
tmpPath = CONFIG['path'] + '\\temp\\AT_AFTER_TEST.py'
try:
    with open(tmpPath, 'rb') as f0:
        tmpV = f0.read()
    tmpV.decode('utf-8')
except UnicodeDecodeError:
    with codecs.open(tmpPath, 'rb', 'gbk') as f1:
        tmpText = f1.read()
    with codecs.open(tmpPath, 'wb', 'utf-8') as f2:
        f2.write(tmpText)
execfile(tmpPath)
if str.lower(CONFIG['debug'])=='n':
    # ******************/更新计划执行进度/*********************
    EX.update_Plan_Exec(3)
    # ******************/更新计划执行进度/*********************

# 启动复测
if CONFIG['restartOnError'] != 0:
    tmpStr = os.popen('tasklist |findstr "TestServer.exe" |find /v "" /c').read().strip()
    if tmpStr == '1':
        logging.info("test restart after 5s")
        sendGet("http://127.0.0.1:1414/restart")
    else:
        logging.info("server not exist")
