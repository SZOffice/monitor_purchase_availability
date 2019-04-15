# -*- coding: utf-8 -*-
import logging
import time
import sys, os
 
class mylog(object):
    def __init__(self, logger_name):
 
        #创建一个logger
        self.logger= logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
 
 
        #设置日志存放路径，日志文件名
        #获取本地时间，转换为设置的格式
        rq = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
        #设置所有日志和错误日志的存放路径
        baseDir = sys.path[0]
        print('baseDir: %s' % baseDir)
        all_log_path = os.path.join(baseDir,'logs/all_logs/')
        if not os.path.exists(all_log_path):
            baseDir = os.path.join(baseDir, "../")
        all_log_path = os.path.join(baseDir, 'logs/all_logs/')
        error_log_path = os.path.join(baseDir, 'logs/error_logs/')
        #设置日志文件名
        all_log_name = all_log_path + rq +'.log'
        error_log_name = error_log_path + rq +'.log'
 
        #创建handler
        #创建一个handler写入所有日志
        fh = logging.FileHandler(all_log_name)
        fh.setLevel(logging.INFO)
        #创建一个handler写入错误日志
        eh = logging.FileHandler(error_log_name)
        eh.setLevel(logging.ERROR)
        #创建一个handler输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
 
        #定义日志输出格式
        #以时间-日志器名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #以时间-日志器名称-日志级别-文件名-函数行号-错误内容
        error_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s  - %(lineno)s - %(message)s')
        #将定义好的输出形式添加到handler
        fh.setFormatter(all_log_formatter)
        ch.setFormatter(all_log_formatter)
        eh.setFormatter(error_log_formatter)
 
 
        #给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(eh)
        self.logger.addHandler(ch)
 
    def getlog(self):
        return self.logger
        
if __name__ == "__main__":
    logger = mylog('test').getlog()
    try:
        logger.info('开始测试...')
        r = 10/0
        logger.info('result:',r)
    except ZeroDivisionError as e:
        logger.error('tests',exc_info=1)
    logger.info('end')