from uiautomator2 import connect
from TestBase import UiHelper
import time
import sys


class Driver:
    d = None

    @classmethod
    def init_dirver(cls, ip_or_serial=None):
        cls.d = connect(ip_or_serial)
        if not cls.d.agent_alive:
            raise Exception("atx-agent is not alive ,please check : {}".format(ip_or_serial))
        UiHelper.d = cls.d
        return cls.d

    @classmethod
    def get_driver(cls,d=None):
        if d is not None:
            cls.d = d
        return cls.d

    @classmethod
    def screenshot(cls, name=None):
        if name is None:
            datetime = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            name = cls.__qualname__ + datetime + '.PNG'
        cls.d.screenshot(name)
        print('IMAGE:' + name)

    #todo: 获取toast信息
    @classmethod
    def get_toast(cls):
        pass

    def swipe_up(self,x=0.5):
        self.d.swipe(x, 0.7, x, 0.3, steps=1)


def scroll(direction: str,duration=1.0):
    '''
    example:
        scroll('up').click(text='登录')
        scroll('down').input('scroll',resourceId='id')
        scroll('left').input('password',text='请输入密码')
        scroll('right').click(description='我的')
    '''

    class _Scroll:
        def __init__(self, direction: str,duration:float):
            self._direction = direction
            self._duration = duration
            module = __import__('App.Driver', fromlist=['Driver'])
            try:
                self._swipe = getattr(module, 'swipe_' + self._direction.lower())
            except AttributeError:
                raise AttributeError('wrong direction,usage : [ up | down | left | right ]')

        def click(self, timeout=15,**kwargs):
            start_time = time.time()
            ele = Driver.d(**kwargs)
            while time.time()-start_time < timeout:
                if ele.exists(timeout=1):
                    ele.click()
                    return
                self._swipe(duration=self._duration)
            raise Exception ("{} element could not found".format(kwargs))

        def input(self, words,timeout=20,**kwargs):
            if kwargs:
                Driver.d(**kwargs).set_text(words,timeout=timeout)
    return _Scroll(direction,duration)


def swipe_up( x=None,duration=1.0):
    toY = 0.3
    fromY = 0.7
    const = 0.5
    if x is not None:
        const = float(x)
    Driver.d.swipe(const, fromY, const, toY, duration)


def swipe_down(x=None, duration=1.0):
    # w, h = self._get_window_size()
    fromY = 0.3
    toY = 0.7
    const = 0.5
    if x is not None:
        const = float(x)
    Driver.d.swipe(const, fromY, const, toY, duration)


def swipe_left(y=None, duration=1.0):
    toX, fromX = 0.3, 0.7
    const = 0.5
    if y is not None:
        const = float(y)
    Driver.d.swipe(fromX, const, toX, const, duration)


def swipe_right( y=None, duration=1.0):
    fromX, toX = 0.3, 0.7
    const = 0.5
    if y is not None:
        const = float(y)
    Driver.d.swipe(fromX, const, toX, const, duration)


def back():
    Driver.d.press('back')


def home():
    Driver.d.press('home')


def watcher():
    pass


def window_size()->tuple:
    w,h = Driver.d.window_size()
    return w, h


def set_timeout(timeout):
    Driver.d.wait_timeout = timeout


def current_app():
    app = Driver.d.current_app()
    print(app)
    return app


if __name__ == '__main__':
    Driver.init_dirver('192.168.33.5')
    print(window_size())