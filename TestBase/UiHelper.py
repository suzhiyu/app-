from __future__ import absolute_import
import time
import uiautomator2 as u2
import threading
from pprint import pprint
import atexit
import six
from selenium import webdriver
import psutil as pt
import os
import sys
# from App.Driver import Driver

if six.PY3:
    import subprocess
    from urllib.error import URLError
else:
    # from urllib2 import URLError
    import subprocess32 as subprocess
# u2.DEBUG = True


class UiHelper:
    d = None

    @classmethod
    def set_driver(cls, adr):
        cls.d = u2.connect(adr)
        if not cls.d.agent_alive:
            print("atx-agent is not alive ,please check : {} ".format(adr))
            sys.exit(-1)
        return cls.d


    @classmethod
    def get_driver(cls):
        return cls.d

    @classmethod
    def set_waitout(cls, timeout=30.0):
        cls.d.wait_timeout = timeout

    @classmethod
    def start_app(cls, pkg_name="com.nonoapp", reset=False):
        if reset:
            cls.d.app_clear(pkg_name)
        cls.d.app_stop(pkg_name)
        cls.d.app_start(pkg_name)
        time.sleep(1)

    @classmethod
    def reset_app(cls, pkg_name="com.nonoapp"):
        cls.d.app_clear(pkg_name)

    @classmethod
    def get_device_info(cls):
        pass

    @classmethod
    def current_app(cls):
        app = cls.d.current_app()
        print(app)
        return app

    @classmethod
    def current_activity(cls):
        activity = cls.d.current_app().get("activity")
        print(activity)
        return activity

    @classmethod
    def watcher(cls,looptime=3.0,**kwargs):
        thread = threading.Thread(target=UiHelper()._watcher_click,args=(looptime,),kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()

    def _watcher_click(self, loop_time=3, **kwargs):
        while True:
            self.click_exists(timeout=1.0, **kwargs)
            time.sleep(float(loop_time))

    def click_exists(self,timeout=3.0,**kwargs):
        self.d(**kwargs).click_exists(timeout=timeout)
        return self

    def click_element(self,wait=1,**kwargs):
        time.sleep(wait)
        self.d(**kwargs).click()
        return self

    def click(self,text,waittime=1):
        time.sleep(waittime)
        self.d(text=text).click()
        return self

    def xpath(self,element):
        return self.d.xpath(element)

    def scroll_up_click(self,text):
        element = self.d(text=text)
        for i in range(10):
            if element.exists(timeout=2):
                element.click()
                return self
            self.swipe_up()

    def scroll_up_click_element(self,**kwargs):
        element = self.d(**kwargs)
        for i in range(10):
            if element.exists(timeout=2):
                element.click()
                return self
            self.swipe_up()

    def click_point(self,x,y):
        self.d.click(x,y)
        return self

    def sleep(self,seconds):
        time.sleep(seconds)
        return self

    def text(self,words,wait,**kwargs):
        if wait:
            time.sleep(wait)
        self.d(**kwargs).set_text(words)
        return self

    def type(self,text):
        self.d.set_fastinput_ime(True)
        self.d.send_keys(text)
        self.d.set_fastinput_ime(False)
        return self

    def back(self):
        self.d.press('back')
        time.sleep(1)
        return self

    def scroll_down_click(self,text):
        element = self.d(text=text)
        for i in range(10):
            if element.exists(timeout=2):
                element.click()
                return self
            self.swipe_down()

    def scroll_down_click_element(self,**kwargs):
        element = self.d(**kwargs)
        for i in range(10):
            if element.exists(timeout=2):
                element.click()
                return self
            self.swipe_down()

    def swipe_up(self, x=None, steps=1):

        # w, h = self._get_window_size()
        toY = 0.3
        fromY = 0.7
        const = 0.5
        if x is not None:
            const = float(x)
        self.d.swipe(const, fromY, const, toY, steps)

    def swipe_down(self, x=None, steps=1):

        # w, h = self._get_window_size()
        fromY = 0.3
        toY = 0.7
        const = 0.5
        if x is not None:
            const = float(x)
        self.d.swipe(const, fromY, const, toY, steps)

    def swipe_left(self,y=None, steps=1):
        # w, h = self._get_window_size()
        toX,fromX = 0.3,0.7
        const = 0.5
        if y is not None:
            const = float(y)
        self.d.swipe(fromX, const, toX, const, steps)

    def swipe_right(self, y=None, steps=1):
        # w, h = self._get_window_size()
        fromX,toX = 0.3,0.7
        const = 0.5
        if y is not None:
            const = float(y)
        self.d.swipe(fromX, const, toX, const, steps)

    def get_toast_message(self):
        message = self.d.toast.get_message(cache_timeout=5, wait_timeout=5)
        self.d.toast.reset()
        return message

    def set_chromedriver(self, ):
        from atx.ext.chromedriver import ChromeDriver
        return ChromeDriver(self.d).driver()

    @classmethod
    def screenshot(cls,name=None):
        if name is None:
            date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            name = cls.__qualname__ + '-' + date_time + '.PNG'
        cls.d.screenshot(name)
        print('IMAGE:' + name)

    def _get_window_size(self):
        window = self.d.window_size()
        x = window[0]
        y = window[1]
        return x, y

    @classmethod
    def watch_device(cls):
        '''wacther devices 如果存在元素则自动点击'''
        cls.u.watchers.watched = False
        cls.d.watcher("ALERT").when(text="我的").click(text="我的")
        cls.d.watcher("允许").when(text="注册").click(text="注册")
        print(cls.d.watchers)
        cls.d.watchers.run()
        time.sleep(30)

    @classmethod
    def page(cls):
        cls.set_driver()
        xml = cls.d.dump_hierarchy()
        pprint(xml)
        return xml


def get_pid_by_name(Str):
    pids = pt.process_iter()
    pidList = []
    for pid in pids:
        if pid.name() == Str:
            pidList.append(int(pid.pid))
    return pidList


class ChromeDriver(object):
    def __init__(self, d, port=9515):
        self._d = d
        self._port = port

    def _launch_webdriver(self):
        print("start chromedriver instance")
        p = subprocess.Popen(['./chromedriver', '--port=' + str(self._port)])
        try:
            p.wait(timeout=2.0)
            return False
        except subprocess.TimeoutExpired:
            return True

    def driver(self, device_ip=None, package=None, attach=True, activity=None, process=None):
        app = self._d.current_app()
        capabilities = {
            'chromeOptions': {
                'androidDeviceSerial': device_ip or self._d.serial,
                'androidPackage': package or app['package'],
                'androidUseRunningApp': attach,
                'androidProcess': process or app['package'],
                'androidActivity': activity or app['activity'],
            }
        }

        try:
            dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)
        except URLError:
            self._launch_webdriver()
            dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)
        # always quit driver when done
        atexit.register(dr.quit)
        return dr

    @staticmethod
    def kill():
        # # for windows
        # pid = getPidByName('chromedriver.exe')
        # for i in pid:
        #     os.popen('taskkill /PID %d /F' % i)
        # for mac
        pid = get_pid_by_name('chromedriver')
        for i in pid:
            os.popen('kill -9 %d' % i)
        print('All chromedriver pid killed')


if __name__ == '__main__':
    d = UiHelper.set_driver(None)
    UiHelper().swipe_up()


