from App.Driver import Driver
import time


class HomePage:
    @property
    def mine_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_home_tab_title", text=u"我的")

    @property
    def invest_view(self):
        return Driver.d(text=u"出借")

    @property
    def discover_view(self):
        return Driver.d(text="发现")

    @property
    def firstpage_view(self):
        return Driver.d(text="首页")

    def click_mine_view(self):
        self.mine_view.click()
        time.sleep(4)