from App import HomePage, DiscoverPage
from App.TestCase.conftest import testcase
from App.TestCase.conftest import BaseTest,debug_case
from App.Driver import Driver,scroll,back
import time
username = ''
password = ''


class TestSitStatic(BaseTest):

    @classmethod
    def setUpClass(cls):
        pass

    @testcase(reruns=2)
    def test_01_page_check(self):
        """  发现页元素检查  """
        HomePage().discover_view.click(timeout=20)
        assert Driver.d(text='普通会员').exists(timeout=3)
        assert Driver.d(text='每日签到').exists(timeout=3)
        assert Driver.d(text='翻翻乐').exists(timeout=3)
        assert Driver.d(text='活动中心').exists(timeout=3)
        assert Driver.d(text='做任务 拿奖励').exists(timeout=3)
        assert Driver.d(text='我的任务').exists(timeout=3)
        assert Driver.d(text='邀请好友').exists(timeout=3)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_02_sign_in(self):
        """ 每日签到 """
        HomePage().discover_view.click(timeout=20)
        DiscoverPage().sign_in_view.click()
        if Driver.d(text='签到成功').exists(timeout=3):
            Driver.d(text='确定').click()
        assert Driver.d(text='恭喜你签到成功').exists(timeout=3)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_03_activity_center(self):
        """ 活动中心 """
        HomePage().discover_view.click(timeout=20)
        DiscoverPage().activity_center_view.click()
        Driver.screenshot()
        back()
        Driver.screenshot()


    @testcase(reruns=3)
    def test_04_invite_friends(self):
        """  邀请好友 - 取消 """
        HomePage().discover_view.click(timeout=20)
        DiscoverPage().invite_friends_view.click()
        if Driver.d(description="邀请好友 ").exists(timeout=4):
            Driver.d(description="邀请好友 ").click()
        else:
            Driver.d(text="邀请好友 ").click()
        assert Driver.d(text='微信').exists(timeout=3)
        assert Driver.d(text='朋友圈').exists(timeout=3)
        assert Driver.d(text='QQ').exists(timeout=3)
        assert Driver.d(text='短信').exists(timeout=3)
        Driver.d(text='取消').click()
        Driver.screenshot()

    @testcase(reruns=2)
    def test_05_check_my_task(self):
        """  检查我的任务页面  """
        time.sleep(3)#显式的等待...
        HomePage().discover_view.click(timeout=20)
        scroll('up').click(text='我的任务')
        if Driver.d(description='去邀请').exists(timeout=3):
            assert True
        elif Driver.d(text='去邀请').exists(timeout=3):
            assert True
        else:
            assert False
        if Driver.d(description='我的福利').exists(timeout=3):
            Driver.d(description='我的福利').click()
        else:
            Driver.d(text='我的福利').click()
        # assert self.d(description='去出借').exists(timeout=3)
        assert Driver.d(text='抵用券').exists(timeout=3)
        assert Driver.d(text='补贴券').exists(timeout=3)
        assert Driver.d(text='特权本金').exists(timeout=3)
        Driver.screenshot()

    @testcase(reruns=2)
    def test_06_check_shopping(self):
        """  检查会员商城页面  """
        time.sleep(3)
        HomePage().discover_view.click(timeout=20)
        scroll('up').click(text='会员商城')
        scroll('up').click(text='查看更多')
        assert Driver.d(text='会员商城').exists(timeout=3)
        assert Driver.d(text='兑换记录').exists(timeout=3)
        assert Driver.d(text='会员专区').exists(timeout=3)


if __name__ == "__main__":
    Driver.init_dirver('192.168.33.5')
    import unittest
    unittest.main()




