from App import InvestPage,SitTester
from App.PageObject.MockPage import MockPage
import unittest
from App.TestCase.conftest import testcase,debug_case
from functools import wraps
from App.TestCase.conftest import BaseTest
from App.PageObject.Steps import *
from App.Driver import Driver,swipe_up,scroll
import random
withdraw_user = "15012340009"
withdraw_amount = 0.0
debt_transfer_reason = None

def withdraw_login(username,):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            HomePage().click_mine_view()
            if not Driver.d(text="登录").exists(timeout=1):
                logout(Driver.d)
                login(Driver.d,username=username)
            else:
                LoginPage().username_view.set_text(username)
                LoginPage().password_view.set_text("it789123")
                back()
                LoginPage().login_view.click()
            Driver.d(text=u"跳过").click_exists(timeout=1)
            result = func(*args,**kwargs)
            return result
        return wrapper
    return decorator

def str_to_no(text):
    return "".join(text.split(","))

class TestSitMain(BaseTest):

    @classmethod
    def setUpClass(cls):
        # super(TestSitMain,cls).setUpClass()
        pass


    @testcase(reruns=2)
    def test_01_invest_txzt_first(self, product_pattern='3个月',amount=None):
        """  贴心智投  """
        amount = amount if amount is not None else random.randint(1,10)*1000
        HomePage().invest_view.click()
        InvestPage().to_txzt_invest()
        Driver.d(textContains=product_pattern).click()
        Driver.d(text="授权出借").click()
        ele = Driver.d(text='进行风险评测')
        if ele.exists(timeout=4):
            ele.click()
            risk_evaluation_steps(Driver.d)
            Driver.d(text="授权出借").click()
        invest_pay_steps(d = Driver.d,amount="{}".format(amount))
        Driver.d(text=u"知道啦").click_exists(timeout=5)
        Driver.d(resourceId='com.nonoapp:id/btn_titlebar_right').click()
        info = Driver.d(resourceId="com.nonoapp:id/tv_first_des").get_text()
        print(info)
        Driver.d(text="完成").click()
        time.sleep(2)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_02_invest_yys_first(self, amount="100"):
        """  月月升投资  """
        HomePage().invest_view.click()
        InvestPage().to_yys_invest()
        Driver.d(text='授权出借').click()
        ele = Driver.d(text='进行风险评测')
        if ele.exists(timeout=5):
            ele.click()
            risk_evaluation_steps(Driver.d)
            Driver.d(text="授权出借").click()
        invest_pay_steps(Driver.d,amount)
        Driver.d(resourceId="com.nonoapp:id/btn_titlebar_right").click()
        info = Driver.d(resourceId="com.nonoapp:id/tv_first_des").get_text()
        print(info)
        Driver.d(resourceId="com.nonoapp:id/tv_titlebar_text_right").click()
        time.sleep(2)
        Driver.screenshot()

    @testcase(reruns=1)
    def test_03_buy_debt(self):
        """ 债转购买--首次购买 """
        HomePage().invest_view.click()
        InvestPage().to_debt_invest()
        Driver.d(text=u"受让债权").click()
        Driver.d(resourceId="com.nonoapp:id/cb_agree_protocol").click()
        text = Driver.d(resourceId="com.nonoapp:id/btn_pay_detail_next").get_text()
        Driver.d(resourceId="com.nonoapp:id/btn_pay_detail_next").click()
        if text == u"余额支付":
            Driver.d(text="确定").click()
            for ele in [Driver.d(description='确定'), Driver.d(text='确定')]:
                if ele.exists(timeout=5):
                    ele.click()
                    break
        elif text == '充值支付':
            for ele in [Driver.d(description='确定'), Driver.d(text='确定')]:
                if ele.exists(timeout=5):
                    ele.click()
                    break
            time.sleep(1)
        assert Driver.d(description="出借成功").exists(timeout=4)
        Driver.d(resourceId="btn_next").click()
        Driver.screenshot()
        time.sleep(3)

    @testcase(reruns=1)
    def test_04_debt_transfer(self, reason="低价贱卖", discount="90"):
        """ 债权转让 """
        global debt_transfer_reason
        debt_transfer_reason = reason
        HomePage().click_mine_view()
        scroll('up').click(text="债转")
        Driver.d(text=u"收款中").click()
        Driver.d(text=u"转让").click()
        Driver.d(resourceId="com.nonoapp:id/et_creditor_right_transfer_reason").set_text(reason)
        Driver.d(resourceId="com.nonoapp:id/et_creditor_right_transfer_discount").set_text(discount)
        Driver.d.press("back")
        Driver.d(text=u"确定转让").click()
        Driver.d(text=u"确定").click()
        time.sleep(3)

    @testcase(reruns=1)
    def test_05_debt_transfer_records(self):
        """债权转让记录"""
        global debt_transfer_reason
        HomePage().click_mine_view()
        # MinePage().debt_text_view.click()
        scroll('up').click(text='债转')
        Driver.d(text=u"转让记录").click()
        assert Driver.d(text=u"3天后下架").exists(timeout=5)
        assert Driver.d(text=debt_transfer_reason).exists(timeout=5)
        Driver.screenshot()

    @testcase(reruns=3)
    def test_06_invest_nny_first(self, amount="200",):
        """  散标  """
        #todo: 红米note安全键盘元素大概无法定位
        HomePage().invest_view.click()
        InvestPage().to_nny_invest()
        # scroll('up',duration=0.2).click(textContains="万")
        el = Driver.d(textContains="万")
        for _ in range(10):
            if el.exists(timeout=2):
                el.click()
                break
            swipe_up()
        Driver.d(text="立即投标").click()
        Driver.d(resourceId="com.nonoapp:id/et_invest_count").click()
        for i in list(amount):
            Driver.d(text=i).click()
        Driver.d(text='确定').click()
        Driver.d(resourceId="com.nonoapp:id/cb_agree_protocol").click()
        text = Driver.d(resourceId="com.nonoapp:id/btn_pay_detail_next").get_text()
        Driver.d(resourceId="com.nonoapp:id/btn_pay_detail_next").click()
        if text == u"余额支付":
            Driver.d(text="确定").click()
        elif text == '充值支付':
            confirm_button = Driver.d(text='确定') if Driver.d.device_info['serial'] == "cdc6dc40" else Driver.d(description='确定')
            confirm_button.click()

        MockPage().confirm_button_view.click()
        assert Driver.d(description="支付成功，等待满标").exists(timeout=5)
        Driver.d(resourceId="btn_next").click()
        Driver.screenshot()



    @testcase(reruns=1)
    @withdraw_login(username=withdraw_user)
    def test_07_withdraw(self, amount=None):
        """  提现  """
        HomePage().click_mine_view()
        text = MinePage().user_balance_view.get_text()
        if text == "****":
            Driver.d(resourceId="com.nonoapp:id/iv_mine_eye").click()
            text = MinePage().user_balance_view.get_text()
        balance = str_to_no(text)
        MinePage().withdraw_view.click()
        if Driver.d(text="冻结余额").exists(timeout=4):
            Driver.d(text="继续交易").click()
        else:
            global withdraw_amount
            withdraw_amount = random.randrange(3, 10000) or amount
            print("余额:{},\n提现:{}".format(balance,withdraw_amount))
            Driver.d(resourceId="com.nonoapp:id/et_withdraw_amount").set_text(withdraw_amount)
            back()
            Driver.d(text='确认提现').click()
            Driver.d(text='确定').click()
        MockPage().confirm_button_view.click()
        text = MinePage().user_balance_view.get_text()
        balance_new = str_to_no(text)
        assert float(balance) - float(balance_new) == float(withdraw_amount)
        print('提现后剩余金额:{}'.format(balance_new))
        Driver.screenshot()

    @testcase(reruns=1)
    def test_08_withdraw_records(self):
        """提现记录"""
        HomePage().click_mine_view()
        MinePage().withdraw_view.click()
        Driver.d(text=u"提现记录").click()
        text= Driver.d(resourceId="com.nonoapp:id/tv_wallet_record_amount").get_text()
        records = str(withdraw_amount-2 if withdraw_amount <20000 else withdraw_amount -3)
        assert records in text
        print('提现记录:{}'.format(text))
        assert Driver.d(resourceId="com.nonoapp:id/tv_wallet_record_status").get_text() == "提现成功"

    @testcase(reruns=2)
    def test_09_transaction_records_withdraw(self):
        """交易记录--提现"""
        HomePage().click_mine_view()
        SitTester().click("交易记录").click("提现").sleep(2)
        text = Driver.d(resourceId="com.nonoapp:id/tv_finance_actual_amount").get_text()
        records = str(withdraw_amount - 2 if withdraw_amount < 20000 else withdraw_amount - 3)
        assert records in text
        print('提现记录:{}'.format(text))
        assert Driver.d(resourceId="com.nonoapp:id/tv_finance_desc").get_text() == "提现"
        Driver.d(resourceId="com.nonoapp:id/tv_finance_desc").click()
        time.sleep(3)
        Driver.screenshot()


if __name__ == "__main__":
    d = Driver.init_dirver('192.168.32.145')
    from App.utils import watcher
    el = d(resourceId="com.nonoapp:id/iv_close")
    watcher(el)
    debug_case(7,8,9)





