from App.Driver import Driver


class WithdrawPage:

    @property
    def withdraw_input_view(self):
        return Driver.d(resourceId="com.nonoapp:id/et_withdraw_amount")

    @property
    def withdraw_button_view(self):
        return Driver.d(resourceId="com.nonoapp:id/btn_withdraw")

    @property
    def withdraw_records_view(self):
        return Driver.d(text=u"提现记录")

    @property
    def user_balance_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_user_balance")
