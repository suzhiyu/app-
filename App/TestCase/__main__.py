import os
import sys
#todo:python path文件
sys.path.append(os.getcwd())
from App import SitTester
from App.TestCase import SIT_SUITE
import unittest
from App.Driver import Driver
from App.HTMLTestReport import HTMLTestRunner
from urllib.parse import urljoin
import requests
import argparse
from multiprocessing import Pool
from App.utils import install_app,watcher

__dir__ = os.path.dirname(os.path.abspath(__file__))
test_report_dirname = 'TestReport'
DEFAULT_TEST_SUITE = SIT_SUITE
ATX_SERVER_URL = 'http://192.168.28.48:8000'
DEVICES_LIST = ['192.168.33.5','192.168.32.145']

def get_test_suite(suite_path):
    testsuite = unittest.TestSuite()
    py_files = unittest.defaultTestLoader.discover(start_dir=suite_path)
    for py_file in py_files:
        testsuite.addTests(py_file)
    return testsuite

def get_devices():
    url = urljoin(ATX_SERVER_URL,'list')
    response = requests.get(url)
    device_data = response.json()

def run(device):
    d = Driver.init_dirver(device)
    device_path = d.device_info['model'].replace(" ", "_")
    print(device_path)
    if not os.path.exists(device_path):os.mkdir(device_path)
    os.chdir(device_path)
    print('-'*10,'\n',d,'-'*10,'\n')
    el = d(resourceId="com.nonoapp:id/iv_close")
    watcher(el)
    with open('testreport.html', 'wb') as file:
        runner = HTMLTestRunner(stream=file, title=d.device_info['model'] + '自动化测试报告', description='用例执行情况：')
        runner.run(DEFAULT_TEST_SUITE)

if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("-d", "--device", help="device ip for connect")
    argparse.add_argument("-a", "--app", help="app path or url")
    args = argparse.parse_args()
    devices = [device for device in args.device.split('/') if device]
    app = args.app
    success = []
    for device in devices:
        try:
            d = Driver.init_dirver(device)
            if app:
                app_path = os.path.abspath(app)
                install_app(d,app)
            success.append(device)
        except Exception as e:
            print("失败设备{},\n{}\n".format(device,e))
    if not success:
        print('没有成功安装App的设备')
        sys.exit(-1)
    if not os.path.exists(test_report_dirname):
        os.mkdir(test_report_dirname)
    os.chdir(test_report_dirname)
    pool = Pool(len(success))
    print(success)
    #todo: 单个进程抛错无法被捕获
    pool.map(run,success)







