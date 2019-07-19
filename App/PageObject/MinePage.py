from App.Driver import Driver


class MinePage:

    @property
    def setting_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_mine_setting")

    @property
    def withdraw_view(self):
        return Driver.d(text=u"提现")

    @property
    def recharge_view(self):
        return Driver.d(resourceId = "com.nonoapp:id/tv_recharge")
        # return Driver.d(text=u"充值")

    @property
    def txzt_text_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_principal_plan")

    @property
    def yys_text_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_principal_yys")

    @property
    def nny_text_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_principal_nny")

    @property
    def debt_text_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_principal_debt")

    @property
    def user_balance_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_available_balance")

    @property
    def user_blance_show_view(self):
        return Driver.d(resourceId="com.nonoapp:id/iv_mine_eye")

    @property
    def transaction_records_view(self):
        return Driver.d(text=u"交易记录")

    def get_user_balance_amount(self):
        text = self.user_balance_view.get_text()
        if text == "****":
            Driver.d(resourceId="com.nonoapp:id/iv_eye").click()
            text = self.user_balance_view.get_text()
        balance_amount = ''.join(text.split(','))
        return balance_amount

    def recharge_steps(self, amount="100"):
        self.recharge_view.click()
        Driver.d(resourceId="com.nonoapp:id/et_recharge_amount").set_text(amount)
        Driver.d(resourceId="com.nonoapp:id/btn_recharge_next").click()

        """  密码校验  """
        Driver.d(text=u"确定").click()


if __name__ == "__main__":
    pass
