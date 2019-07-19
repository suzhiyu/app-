from App import HomePage,MinePage,SitTester,SettingPage
from App.PageObject.Steps import *
import unittest
from App.TestCase.conftest import testcase
from App.Driver import Driver,scroll
from App.TestCase.conftest import debug_case,BaseTest
import random


register_user = None


class TestSitSuite(BaseTest):

    @testcase(reruns=2)
    def test_01_sign_up(self,username=None):
        """  注册  """
        if username is None:
            username = create_iphone_no()
        HomePage().mine_view.click()
        LoginPage().register_view.click()
        sign_up_steps(Driver.d,username)
        Driver.d(text="跳过").click()
        global register_user
        register_user = username
        print("注册用户:", register_user)
        Driver.screenshot()
        Driver.d(text="先去逛逛").click()
        time.sleep(1)

    @testcase(reruns=3)
    def test_02_openacc(self):
        """  徽商开户  """
        HomePage().click_mine_view()
        MinePage().setting_view.click()
        SettingPage().open_account_view.click()
        open_account_steps(Driver.d, name="李一")
        if Driver.d(description='徽商出借人电子账户开户成功').exists(timeout=4) \
                or Driver.d(text='徽商出借人电子账户开户成功').exists(timeout=4):
            assert True
        else:
            assert False
        Driver.screenshot()
        elements = [Driver.d(description='完成'),Driver.d(text='完成')]
        for ele in elements:
            if ele.exists(timeout=3):
                ele.click()
                break

    @testcase(reruns=2)
    def test_03_set_password(self,name=None,id_no=None):
        """  设置交易密码  """
        HomePage().click_mine_view()
        MinePage().recharge_view.click()
        """判断是否开户"""
        if Driver.d(text='徽商存管开户提醒').exists(timeout=4):
            time.sleep(4)
            Driver.d('确定').click()
            open_account_steps(Driver.d, name="李一")
            elements = [Driver.d(description='完成'), Driver.d(text='完成')]
            for ele in elements:
                if ele.exists(timeout=3):
                    ele.click()
                    break
            MinePage().recharge_view.click()
        #todo:充值steps
        Driver.d(text="请输入充值金额").set_text("100")
        # d(text='确定').click()
        Driver.d.click(0.862, 0.856)
        Driver.d(text='立即充值').click()
        if Driver.d(text=u"身份信息验证", className="android.views.View").exists(timeout=3):
            Driver.d(resourceId="realname").set_text(name)
            Driver.d(resourceId="id_no").set_text(id_no)
            Driver.d(resourceId="btn_send").click()
            Driver.d(resourceId="valide_code").set_text('888888')
            Driver.d(resourceId="btn_next").click()
        time.sleep(2)
        elements = [Driver.d(description=u"确定"), Driver.d(text='确定')]
        for ele in elements:
            if ele.exists:
                ele.click()
                break
        time.sleep(2)

    @testcase(reruns=2)
    def test_04_recharge(self, amount=None):
        """  充值  """
        global recharge_amount
        recharge_amount = amount or random.randrange(1,50000)
        print('充值金额{}'.format(recharge_amount))
        HomePage().click_mine_view()
        MinePage().recharge_view.click()
        if Driver.d(text='徽商存管开户提醒').exists(timeout=4):
            time.sleep(4)
            Driver.d.click('确定')
            open_account_steps(Driver.d, name="李一")
            elements = [Driver.d(description='完成'), Driver.d(text='完成')]
            for ele in elements:
                if ele.exists(timeout=3):
                    ele.click()
                    break
            MinePage().recharge_view.click()
        Driver.d(resourceId="com.nonoapp:id/et_recharge_amount").set_text(recharge_amount)
        Driver.d.click(0.862, 0.856)
        Driver.d(resourceId="com.nonoapp:id/btn_recharge_next").click()
        time.sleep(3)
        elements = [Driver.d(description=u"确定"), Driver.d(text='确定')]
        for ele in elements:
            if ele.exists(timeout=4):
                ele.click()
                break
        time.sleep(4)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_05_transaction_records_recharges(self):
        """充值记录"""
        HomePage().click_mine_view()
        SitTester().click("交易记录").click("充值").sleep(2)
        assert Driver.d(resourceId="com.nonoapp:id/tv_finance_desc").get_text()=="充值"
        amout_text = Driver.d(resourceId="com.nonoapp:id/tv_finance_actual_amount").get_text()
        print(amout_text)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_06_invest_accredition(self):
        """  智能出借授权  """
        HomePage().click_mine_view()
        MinePage().setting_view.click()
        Driver.d(text=u"智能出借授权").click()
        Driver.d(resourceId="btn_next").click()
        elements = [Driver.d(description='确定'), Driver.d(text='确定')]
        for ele in elements:
            if ele.exists(timeout=4):
                ele.click()
                break
        if Driver.d(description=u"您的徽商存管智能出借开通成功！").exists(timeout=4) \
                or Driver.d(text=u"您的徽商存管智能出借开通成功！").exists(timeout=4):
            assert True
        else:
            assert False
        elements = [Driver.d(description='完成'), Driver.d(text='完成')]
        for ele in elements:
            if ele.exists:
                ele.click()
                break
        assert Driver.d(text='已开通').exists(timeout=5)
        print("------开通智能出借授权------")

    @testcase(reruns=2)
    def test_07_risk_evaluation(self):
        """  风险评测  """
        HomePage().click_mine_view()
        MinePage().setting_view.click()
        SettingPage().risk_evaluation_view.click()
        risk_evaluation_steps(Driver.d)
        assert Driver.d(text="已测评").exists(timeout=4)
        print("------完成风险评测------")
        text = Driver.d(resourceId="com.nonoapp:id/tv_evaluating_result").get_text(timeout=4)
        print(f"风险等级:{text}")


    @testcase(reruns=2)
    def test_08_check_my_welfare(self):
        """  新手福利发放  """
        HomePage().click_mine_view()
        scroll('up').click(resourceId="com.nonoapp:id/iv")
        assert Driver.d(text="新客福利（不可叠加）").exists(timeout=3)
        assert Driver.d(text="立即使用").exists(timeout=3)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_09_logout(self):
        """  退出登录  """
        logout(Driver.d)

    @testcase(reruns=2)
    def test_10_login(self, username=None):
        """  登录  """
        if username is None:
            username = register_user
        login(Driver.d, username)
        Driver.d(text=u"跳过").click_exists(timeout=2)
        print("登录成功")
        Driver.d(text=u"先去逛逛").click_exists(timeout=3)


if __name__ == "__main__":
    register_user = 17691529151
    d = Driver.init_dirver('192.168.32.145')
    SitTester.watcher(resourceId="com.nonoapp:id/iv_close")
    #get_text不加timeout参数报错问题
    unittest.main()
    # d(resourceId='bank').click()

