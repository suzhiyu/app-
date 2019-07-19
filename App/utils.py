from smtplib import SMTP
from email.mime.text import MIMEText
import time
from aip import AipOcr
from App.Driver import Driver
from os import system
import re
import os
from threading import Thread

host = 'smtp.qq.com'
port = 25
username = '1810420645@qq.com'
password = 'qhacwnvodwskcbaf'

OCR_CONFIG = {'appId': '14397002',
              'apiKey': 'L4M3793VBPAgcTmx3e8m8p5G',
              'secretKey': '3V5V9t1nMBut4irDy7Nwssi2cxUXx7r6 '}


# todo: ocr单例模式 PageObject staticmethod
class BaiduOcr(AipOcr):
    __instance = None

    def __init__(self):
        if not OCR_CONFIG:
            raise Exception(
                "请先设置OCR_CONFIG:-----------\n\n"
                "from uirunner.utils import OCR_CONFIG\n"
                "OCR_CONFIG = {'appId':'你的appId','apiKey':'你的apiKey','secretkey':'你的secretKey'}")
        super(BaiduOcr, self).__init__(**OCR_CONFIG)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

#todo: 单例模式暂不支持多线程


def ocr(
        text=None,
        textContains=None,
        startWith=None,
        endWith=None,
        high_precision=False):
    class _Ocr:
        __instance = None

        def __init__(self, high_precision=False, **kwargs):
            self._text = kwargs.get("text", None)
            self._textContains = kwargs.get("textContains", None)
            self._startWith = kwargs.get("startWith", None)
            self._endWith = kwargs.get("endWith", None)
            self._hight_precision = high_precision
            self.client = BaiduOcr()
            self.general = self.client.general
            self.accurate = self.client.accurate
            self._center = None

        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = object.__new__(cls)
            return cls.__instance

        def _requests(self):
            Driver.screenshot("ocr.png")
            with open("ocr.png", 'rb')as f:
                image = f.read()
            return self.accurate(
                image) if self._hight_precision else self.general(image)

        def _get_center(self,):
            words_result = self._requests().get("words_result", [])
            if len(words_result) == 0:
                return None
            for word_result in words_result:
                words = word_result["words"]
                #todo:条件判断放到循环外面
                if self._text:
                    if not self._text == words:
                        continue
                    x = word_result.get("location").get(
                        "left") + word_result.get("location").get("width") / 2
                    y = word_result.get("location").get(
                        "top") + word_result.get("location").get("height") / 2
                    self._center = (x, y)
                    return self._center

                elif not self._textContains or self._textContains and self._textContains in words:
                    if self._startWith and not words.startswith(
                            self._startWith) or self._endWith and not words.endswith(
                            self._endWith):
                        continue
                    x = word_result.get("location").get(
                        "left") + word_result.get("location").get("width") / 2
                    y = word_result.get("location").get(
                        "top") + word_result.get("location").get("height") / 2
                    self._center = (x, y)
                    return self._center

            return None

        def click(self, timeout=6, retry=False):
            if self._center:
                Driver.d.click(*self._center)
                return True
            start_time = time.time()
            while time.time() - start_time < timeout:
                point = self._get_center()
                if point is None:
                    continue
                elif self._center is None:
                    self._center = point
                    continue
                elif self._center == point:
                    Driver.d.click(*point)
                    return True
                else:
                    self._center = point
            if self._center:
                Driver.d.click(*self._center)
                return True
            if retry:
                return False
            raise Exception('BaiduOcr: <{}> element could not found '.format(
                self._text or self._textContains or self._startWith or self._endWith))

        def input(self, words, timeout=6):
            self.click(timeout=timeout)
            Driver.d(focused=True).set_text(words)

        def click_exists(self,timeout=1):
            start_time = time.time()
            while time.time()-start_time<timeout:
                if self.exists:
                    self.click()


        @property
        def exists(self,):
            obj = self
            class Exists:

                def __bool__(self):
                    if obj._get_center():
                        return True
                    return False

                def __call__(self, timeout=0):
                    if timeout:
                        start = time.time()
                        while time.time() - start < timeout:
                            if bool(self):
                                return True
                        return False

            return Exists()
        # todo:scroll('up').click()
    return _Ocr(
        text=text,
        textContains=textContains,
        startWith=startWith,
        endWith=endWith,
        high_precision=high_precision)



def create_iphone_no():
    '''生成手机号'''
    return "176" + ''.join(str(time.time()).split('.'))[-8:]


def sent_email(to: str, msg: str, msg_type='plain'):
    with SMTP(host, port) as smtp:
        smtp.login(username, password)
        msg = MIMEText(msg, msg_type, 'utf-8')
        smtp.sendmail(from_addr=username, to_addrs=to, msg=msg.as_string())


def watcher(element):
    def _click(element):
        while True:
            if element.exists(timeout=1):
                element.click()
            time.sleep(2)
    thread = Thread(target=_click, args=(element,))
    thread.setDaemon(True)
    thread.start()


def adb_screenshot(serial, name=None):
    name = name or 'adb_screenshot.png'
    system("adb -s {} shell screencap  -p > {}".format(serial, name))


def adb_start_atx_agent():
    system("adb shell chmod 755 /data/local/tmp/atx-agent")
    system("adb shell /data/local/tmp/atx-agent  version")
    system("adb shell /data/local/tmp/atx-agent  server -d")

# todo:page


def adb_page():
    pass


def is_a_url(addr):
    regx = re.compile(r'https?://\w+(\.\w+)+(:\d+)?[/\w%-_]*')
    result = regx.match(addr)
    if result:
        return True

# todo install_app  安装测试失败


def install_app(d, url_or_path):
    if url_or_path.startswith('http'):
        d.app_install(url_or_path)
    elif os.path.isfile(url_or_path):
        apk_name = os.path.basename(url_or_path)
        d.push(url_or_path, "/sdcard/app/")
        response = d.shell("pm  install -r /sdcard/app/%s" % apk_name)
        if not response.exit_code == 0:
            raise Exception('install app error: {}'.format(url_or_path))
        print(response.output)
    else:
        raise Exception("install_app arg should be a url or a file path")


def xml2json():
    pass


# todo: watcher 1.弹窗，2.程序异常退出tosat
if __name__ == '__main__':
    # todo: 异常捕获，防御代码的编写思路
    d = Driver.init_dirver('192.168.33.5')
    ocr(text="查看更多").click()


