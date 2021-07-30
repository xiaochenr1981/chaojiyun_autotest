from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
import math
import operator
from functools import reduce
import os
import logging
from logging import handlers
import shutil


# import logging
# from logging import handlers
#
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


# if __name__ == '__main__':
#     log = Logger('all.log',level='debug')
#     log.logger.debug('debug')
#     log.logger.info('info')
#     log.logger.warning('警告')
#     log.logger.error('报错')
#     log.logger.critical('严重')
#     Logger('error.log', level='error').logger.error('error')

def pil_image_similarity(filepath1, filepath2):
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
    #    image1 = get_thumbnail(img1)
    #    image2 = get_thumbnail(img2)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return rms


def movefile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.move(srcfile, dstfile)  # 移动文件
        print("move %s -> %s" % (srcfile, dstfile))


browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
browser.get("https://cloud.chaojidun.com/login")
browser.maximize_window()
# print(browser.page_source)
# browser.close()

# 登录
name_box = browser.find_element_by_class_name("el-input__inner")
name_box.send_keys("13858182517")
time.sleep(1)
name_box.send_keys(Keys.TAB)
time.sleep(1)
s_box = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/input")
s_box.send_keys("Super000")
login_button = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div/div[2]/div[2]/div[1]/div/button[1]")
login_button.click()
time.sleep(2)
chanpinAndfuwu = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div/ul[1]/li")
chanpinAndfuwu.click()
time.sleep(3)

# 记录日志
log = Logger('./test/all.log', level='debug')
err = Logger('./test/err.log', level='debug')
err_dir = "./picture_test_err"
# log.logger.info('首页测试正常')
# err.logger.error('测试异常')

# step1比较首页
picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
picture_dir = "./case_picture/" + picture_time + ".png"
picture_url = browser.get_screenshot_as_file(picture_dir)

check_reslut = pil_image_similarity('./case_picture/HomePage.png', picture_dir)
if check_reslut < 100:
    log.logger.info('首页登录成功')
    # movefile(picture_dir, err_dir)
    os.remove(picture_dir)
else:
    err.logger.error('首页登录失败')
    movefile(picture_dir, err_dir)

# step2热门产品  //*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[1]/ul/li[1]/span
chanpinAndfuwu = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[1]/ul/li[1]/span")
chanpinAndfuwu.click()
time.sleep(1)
# ecs   //*[@id="app"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[1]
# 购买 //*[@id="app"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[2]/div[1]/span
element = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[1]")
ActionChains(browser).move_to_element(element).perform()
chanpinAndfuwu = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[2]/div[1]/span")
chanpinAndfuwu.click()
time.sleep(1)

# step2  //*[@id="app"]/div/div[2]/div[1]/div/ul[1]/li/span
#        //*[@id="app"]/div/div[2]/div[1]/div/ul[1]/li/span
chanpinAndfuwu = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/ul[1]/li/span")
chanpinAndfuwu.click()
time.sleep(1)
# 数据库   //*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[1]/ul/li[3]
element = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[1]/ul/li[3]")
ActionChains(browser).move_to_element(element).perform()
# 云数据   //*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[1]
element = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[1]")
ActionChains(browser).move_to_element(element).perform()
# 购买 //*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[2]/div[1]
chanpinAndfuwu = browser.find_element_by_xpath(
    "//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div/section/div/div[3]/div[2]/div[1]/div/ul/li[1]/div/div[2]/div[1]")
chanpinAndfuwu.click()
time.sleep(1)

# browser.quit()
