from App.Driver import Driver


class FirstPage:

    def click_invest_button(self):
        Driver.d(u"立即投资").click()

    def click_sign_up_button(self):
        Driver.d(resourceId="com.nonoapp:id/btn_home_register").click()

    def click_txzt_button(self):
        Driver.d(resourceId="com.nonoapp:id/btn_home_hot_cake_invest").click()
