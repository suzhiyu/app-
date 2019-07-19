import time
from App.PageObject.Steps import reset_and_start_nonoapp,set_env
from functools import wraps
from App.Driver import Driver
from unittest import TestCase
import re
from App.PageObject.Steps import start_nonoapp
import subprocess
from pprint import pprint


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        reset_and_start_nonoapp(Driver.d)
        set_env(Driver.d)



    def setUp(self):
        start_nonoapp(d=Driver.d)
        Driver.d(resourceId="com.nonoapp:id/tv_splash_skip").click_exists(timeout=2)
        Driver.d(resourceId="com.nonoapp:id/ib_close").click_exists(timeout=2)
        Driver.d(resourceId = "com.nonoapp:id/iv_close").click_exists(timeout=5)
        """ loading等待 """
        for i in range(0, 10):
            if Driver.d(resourceId="com.nonoapp:id/progress_image").exists:
                time.sleep(3)
            else:
                break

    def tearDown(self):
        subprocess.Popen('ps -ef | grep \'chromedriver\' | grep -v \'grep\' | awk \'{print $2}\' | xargs kill -9',
                         shell=True)

    @classmethod
    def tearDownClass(cls):
        subprocess.Popen('ps -ef | grep \'chromedriver\' | grep -v \'grep\' | awk \'{print $2}\' | xargs kill -9',
                         shell=True)
        Driver.d.app_stop('com.nonoapp')

def testcase(reruns:int,exceptions=Exception):
    '''

    :param exceptions:
    :param reruns:
    :return:
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            module = __import__('App.TestCase',fromlist=['TestCase'])
            classname = func.__qualname__.split('.')[0]
            cls = getattr(module,classname)
            total = reruns
            while total>=0:
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except exceptions as e:
                    date = time.strftime('%Y%m%d-%H%M%S', time.localtime())
                    name = func.__qualname__ + date + '.PNG'
                    Driver.screenshot(name)
                    if total == 0:
                        raise e
                    total -= 1
                    time.sleep(1)
                    print("failed,try again....\n failed reason:\n{}".format(e))
                    cls().setUp()
        return wrapper
    return decorator


def debug_case(*args:int):
    func_list = []
    self  = None
    module = __import__('__main__')
    for item in dir(module):
        cls = getattr(module, item)
        if isinstance(cls,type) and issubclass(cls,TestCase):
            self = cls()
            for item in dir(self):
                func = getattr(self,item)
                if item.startswith('test') and hasattr(func,'__call__'):
                    func_list.append(func)
    if args:
        args = list(map(lambda x:str(x)if x>=10 else "0"+str(x),sorted(args)))
        #func命名格式test_01_...
        test_func_list = [func for func in func_list if re.search('(\d+)',func.__name__).group(1) in args]
    else:
        test_func_list = func_list
    first_test = re.search('(\d+)',test_func_list[0].__name__).group(1)
    setUpClass = getattr(self,'setUpClass',None)
    setUp = getattr(self, 'setUp',None)
    tearDown = getattr(self, 'tearDown',None)
    tearDownClass = getattr(self, 'tearDownClass',None)
    if first_test in ['01','1'] and setUpClass is not None:
        setUpClass()
    for func in test_func_list:
        if setUp is not None:
            setUp()
            print('test :-->{}'.format(func.__name__))
            func()
        if tearDown is not None:
            tearDown()
    if tearDownClass is not None:
        tearDownClass()


def before_test():
    '''
    1.安装App
    2.设置测试环境
    3.watcher()
    :return:
    '''


if __name__ == "__main__":
    pass