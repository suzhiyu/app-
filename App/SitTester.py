from TestBase import UiHelper
from App import (HomePage,WelcomePage)

import time


class SitTester(UiHelper):

    @classmethod
    def set_driver(cls, adr=None):
        return UiHelper.set_driver(adr)

    @classmethod
    def set_env(cls):
        WelcomePage().button.click_exists(timeout=8)
        time.sleep(3)
        HomePage().mine_view.click()
        # LoginPage().switch_env_steps(env)
        cls.d(text="切换测试环境").click()
        cls.d(text="SIT").click()
        cls.d(text="确认").click()
        cls.d(text="立即注册领1888新手福利").click()
        # WelcomePage().click_button()

    @classmethod
    def before_test(cls,set_waitout=15.0):
        print('Waiting for all runs done........ ')
        cls.start_app(reset=True)
        print('始终允许,允许...')
        cls.d(text='允许').click_exists(timeout=4)
        cls.d(textContains='允许').click_exists(timeout=4)
        cls.d(textContains='允许').click_exists(timeout=4)
        if cls.d.device_info.get("model") == "SM705":
            time.sleep(15)
        cls.set_env()

        cls.set_waitout(timeout=set_waitout)

    def loading_wait(self):
        pass

    def login(self,username,password="it789123"):
        self.click("我的")
        self.d(resourceId="com.nonoapp:id/et_username").set_text(f"{username}")
        self.d(resourceId="com.nonoapp:id/et_password").set_text(f"{password}")
        self.back()
        self.click('登录')
        ele = self.d(text='验证码登录')
        if ele.exists(timeout=3):
            ele.click()
            self.click('获取验证码')
            self.d(text='请输入图形验证码').set_text(text='8888')
            self.click('确定')
            self.d(text='请输入验证码').set_text(text='888888')
            self.back()
            self.click('登录')
        return self

    def logout(self):
        self.click("我的")
        time.sleep(4)
        setting_button = self.d(resourceId="com.nonoapp:id/iv_setting")
        setting_button.click()
        self.scroll_up_click("安全退出").click("确定").sleep(2)
        return self


if __name__ == "__main__":
    pass

