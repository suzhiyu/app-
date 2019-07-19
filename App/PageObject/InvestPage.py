from App.Driver import Driver

class InvestPage:

    def to_nny_invest(self):
        Driver.d(text='散标').click()
        # Driver.d(text='优选单标').click()

    def to_txzt_invest(self):
        Driver.d(text='工具').click()
        Driver.d(text='贴心智投').click()

    def to_debt_invest(self):
        Driver.d(text='债转').click()

    def to_yys_invest(self):
        Driver.d(text='工具').click()
        Driver.d(text='月月升智投').click()

    def click_txzt_invest_button(self):
        Driver.d(resourceId="com.nonoapp:id/tv_invest_product").click()

