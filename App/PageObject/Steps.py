import time
from App.Driver import back,Driver,scroll
from App.utils import ocr
from App import (MinePage,
                 HomePage,
                 LoginPage,
                 WelcomePage,
                 MockPage)
from App.PageObject.OpenAccountPage import OpenAccountPage
from App.utils import ocr
from driver.chrome.chromedriver import ChromeDriver
import uiautomator2 as u2


def open_account_steps(d, name='李一'):
    '''开户步骤'''
    OpenAccountPage().real_name_view.set_text(name)
    el = OpenAccountPage().open_account_bank_view
    if el.exists(timeout=3):
        el.click()
    else:
        ocr('开户行').click()
    # todo:兼容优化
    #todo: element = d(a) or d(b)  return find_element()
    time.sleep(5)
    driver = ChromeDriver(u2.connect('192.168.37.24')).driver()
    time.sleep(5)
    driver.find_element_by_xpath('//div[@id="bank_list"]//h4[text()="农业银行"]').click()
    driver.quit()
    print('#######################################')
    # d(description=u"农业银行").click()
    OpenAccountPage().user_mobile_view.set_text('15774180173')
    if d(resourceId="com.nuance.swype.emui:id/keyboardViewEx").exists(timeout=3):
        d.press("back")
    time.sleep(1)
    ele = OpenAccountPage().next_button_view
    if not ele.exists(timeout=2):
        d.press('back')
    time.sleep(1)
    ele.click()
    time.sleep(1)
    MockPage().confirm_button_view.click()


def risk_evaluation_steps(d, use_ocr=True):
    '''风险测评步骤'''
    if d(description=u"重新测评").exists(timeout=3):
        d(description=u"重新测评").click()
    elif d(text=u"重新测评").exists(timeout=3):
        d(text=u"重新测评").click()
    options = ['D.', 'D.', 'D.', 'D.', 'E.', 'E.', 'D.', 'A.']
    if not use_ocr:
        d(description=u"开始测评").click()
        for index,option in enumerate(options):
            print("{0}/ 8题:".format(index+1),end='')
            if d(description=u"{0}/ 8题".format(index+1)).exists(timeout=4):
                d(descriptionContains=option).click()
            print(option)
    else:
        if not ocr("开始测评").click(retry=True):
            ocr("开始测评", high_precision=True).click()
        for index, option in enumerate(options):
            print("{0}/ 8题:".format(index + 1), end='')
            if not ocr(textContains=option).click(retry=True):
                ocr(textContains=option, high_precision=True).click()
            print(option)
    if d(description=u"知道了").exists(timeout=3):
        d(description=u"知道了").click()
    else:
        d(text=u"知道了").click()


def set_password_steps(d, name=None, id_no=None):
    '''设置支付密码步骤'''
    d(resourceId="com.nonoapp:id/et_recharge_amount").set_text("100")
    d(text='确定').click()
    d(text='立即充值').click()
    if d(text=u"身份信息验证", className="android.views.View").exists(timeout=3):
        d(resourceId="realname").set_text(name)
        d(resourceId="id_no").set_text(id_no)
        d(resourceId="btn_send").click()
        d(resourceId="valide_code").set_text('888888')
        d(resourceId="btn_next").click()
    time.sleep(2)
    elements = [d(description=u"确定"),d(text='确定')]
    for ele in elements:
        if ele.exists:
            ele.click()
            break


def sign_up_steps(d, username, password="it789123", code="8888888"):
    '''注册步骤'''
    # d(text="注册").click()
    d(text="请输入手机号").set_text("{}".format(username))
    d(resourceId="com.nonoapp:id/cbox_register_user_protocol").click()#点击协议
    d(text="下一步").click()
    d(resourceId="com.nonoapp:id/gtv_register_phone_vercode").click()
    for i in code:
        d.adb_shell(["input", "text", i])
    d(text=u"下一步").click()
    d(resourceId="com.nonoapp:id/et_register_pwd").set_text(password)
    d(resourceId="com.nonoapp:id/btn_register_finish").click()


def withdraw_steps(d,amount:float):
    '''提现步骤'''
    pass


def recharge_steps(d,amount:float):
    '''充值步骤'''
    pass

def invest_pay_steps(d,amount:str):
    '''投资订单提交步骤'''
    d(resourceId="com.nonoapp:id/et_invest_count").set_text(amount)
    d(text='确定').click()
    d(resourceId="com.nonoapp:id/cb_agree_protocol").click()
    text = d(resourceId="com.nonoapp:id/btn_pay_detail_next").get_text()
    d(resourceId="com.nonoapp:id/btn_pay_detail_next").click()
    if text == u"余额支付":
        d(text="确定").click()
    elif text == '充值支付':
        confirm_button = d(text='确定') if d.device_info['serial'] == "cdc6dc40" else d(description='确定')
        confirm_button.click()




def create_iphone_no():
    '''生成手机号'''
    return "176"+''.join(str(time.time()).split('.'))[-8:]


def register_and_login(d,username=None):
    '''注册并登录'''
    username =  username or create_iphone_no()
    LoginPage().register_view.click()
    d(text="请输入手机号").set_text("{}".format(username))
    d(resourceId="com.nonoapp:id/cbox_register_user_protocol").click()  # 点击协议
    d(text="下一步").click()
    d(resourceId="com.nonoapp:id/gtv_register_phone_vercode").click()
    for i in "8888888":
        d.adb_shell(["input", "text", i])
    d(text=u"下一步").click()
    d(resourceId="com.nonoapp:id/et_register_pwd").set_text("it789123")
    d(resourceId="com.nonoapp:id/btn_register_finish").click()
    d(text='跳过').click()
    return username


def login(d, username, password="it789123"):
    '''登录'''
    HomePage().mine_view.click()
    if d(resourceId="com.nonoapp:id/tv_mine_setting").exists(timeout=2):
        logout(d)
        HomePage().mine_view.click()
    LoginPage().username_view.set_text(username)
    LoginPage().password_view.set_text(password)
    back()
    LoginPage().login_view.click()
    ele = Driver.d(text='验证码登录')
    if ele.exists(timeout=3):
        ele.click()
        d(text=u'获取验证码').click()
        d(text='请输入图形验证码').set_text(text='8888')
        d(text='确定').click()
        d(text='请输入验证码').set_text(text='888888')
        back()
        LoginPage().login_view.click()
    d(text=u"跳过").click_exists(timeout=2)


def logout(d):
    '''退出'''
    HomePage().mine_view.click()
    d(text='先去逛逛').click_exists(timeout=4)
    MinePage().setting_view.click()
    scroll('up').click(text='安全退出')
    d(text='确定').click()


def reset_and_start_nonoapp(d,pkg_name='com.nonoapp'):
    '''重置并重启App'''
    d.app_clear(pkg_name=pkg_name)
    d.app_start(pkg_name=pkg_name)
    print('始终允许,允许...')
    d(textContains='允许', clickable=True).click_exists(timeout=4)
    d(textContains='允许', clickable=True).click_exists(timeout=4)
    WelcomePage().button.click()


def set_env(d, env='sit'):
    '''设置测试环境'''
    d(resourceId="com.nonoapp:id/tv_splash_skip").click_exists(timeout=2)
    HomePage().mine_view.click()
    LoginPage().switch_env_view.click()
    d(text="{}".format(env.upper())).click()
    d(text="确认").click()
    WelcomePage().button.click()


def start_nonoapp(d,pkg_name='com.nonoapp'):
    '''启动App'''
    d.app_stop(pkg_name)
    d.app_start(pkg_name)


if __name__ == '__main__':
    d = Driver.init_dirver('192.168.33.5')
