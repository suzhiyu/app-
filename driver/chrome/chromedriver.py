#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import atexit
import six
import configparser
import sys
import subprocess
from selenium import webdriver

if six.PY3:
    import subprocess
    from urllib.error import URLError
else:
    from urllib2 import URLError
    import subprocess32 as subprocess


class ChromeDriver(object):
    def __init__(self, d, port=9515):
        self._d = d
        self._port = port

    def _launch_webdriver(self):
        print("start chromedriver instance")
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        if sys.platform in ('darwin', 'Darwin'):
            os_dir = '/mac'
        elif sys.platform in ('linux', 'linux2'):
            os_dir = '/linux'
        else:
            os_dir = '/win'
        webview = subprocess.Popen('adb shell dumpsys package com.google.android.webview | grep versionName',
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        webview = webview.communicate()[0]
        version = bytes.decode(webview).strip().split('=')[1]
        version = version.split('.')[0]
        cf = configparser.ConfigParser()
        cf.read(cur_dir + '/' + 'chromedriver.conf')
        driver_version = cf.get(version, 'chromedriver')
        driver_path = cur_dir + os_dir + '/' + driver_version + '/chromedriver'
        print(driver_path)
        p = subprocess.Popen([driver_path, '--port='+str(self._port)])
        try:
            p.wait(timeout=2.0)
            return False
        except subprocess.TimeoutExpired:
            return True

    def driver(self, device_ip=None, package=None, attach=True, activity=None, process=None):
        """
        Args:
            - package(string): default current running app
            - attach(bool): default true, Attach to an already-running app instead of launching the app with a clear data directory
            - activity(string): Name of the Activity hosting the WebView.
            - process(string): Process name of the Activity hosting the WebView (as given by ps).
                If not given, the process name is assumed to be the same as androidPackage.

        Returns:
            selenium driver
        """
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
        self._launch_webdriver()
        dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)
        dr.implicitly_wait(30)
        # always quit driver when done
        atexit.register(dr.quit)
        return dr

    def windows_kill(self):
        subprocess.call(['taskkill', '/F', '/IM', 'chromedriver.exe', '/T'])


if __name__ == '__main__':
    # import atx
    # d = atx.connect()
    # driver = ChromeDriver(d).driver()
    # elem = driver.find_element_by_link_text(u"登录")
    # elem.click()
    # driver.quit()
    import uiautomator2 as u2
    driver = ChromeDriver(u2.connect('192.168.37.27')).driver()


