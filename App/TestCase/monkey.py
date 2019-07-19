from uiautomator2 import connect
from App import WelcomePage

username = "15012340008"
password = "it789123"


def set_env(d):
    d(text='始终允许').click_exists(timeout=4)
    d(text='始终允许').click_exists(timeout=4)
    WelcomePage().button.click_exists(timeout=8)
    d(text='我的').click()
    d(text="切换测试环境").click()
    d(text="SIT").click()
    d(text="确认").click()
    d(text="立即注册领1888新手福利").click()


def login(d):
    d(text='我的').click()
    d(resourceId="com.nonoapp:id/et_username").set_text(f"{username}")
    d(resourceId="com.nonoapp:id/et_password").set_text(f"{password}")
    d.press('back')
    d(text='登录').click()
    ele = d(text='验证码登录')
    if ele.exists(timeout=3):
        ele.click()
        d(text='获取验证码').click()
        d(text='请输入图形验证码').set_text(text='8888')
        d(text='确定').click()
        d(text='请输入验证码').set_text(text='888888')
        d.press('back')
        d(text='登录').click()


def monkey_run(d):
    '''
    /system/framework/monkey.jar
    :param d:
    :return:
    '''
    monkey_command = 'monkey -p com.nonoapp -v -v 50000 ' \
                     '--throttle 500' \
                     '--pct-touch   --pct-motion'
    d.shell(monkey_command)


def main():
    d = connect('192.168.33.25')
    print(d.info)
    d.app_clear('com.nonoapp')
    d.app_start('com.nonoapp')
    set_env(d)
    login(d)
    monkey_run(d)


if __name__ == '__main__':
    d = connect('192.168.33.25')
    print(d.adb_shell('pwd'))

