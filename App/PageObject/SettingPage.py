from App.Driver import Driver


class SettingPage:

    @property
    def risk_evaluation_view(self):
        return Driver.d(text='风险评测')

    @property
    def logout_view(self):
        return Driver.d(resourceId="com.nonoapp:id/btn_setting_logout",text=u"安全退出")

    @property
    def open_account_view(self):
        return Driver.d(text=u"徽商存管管理")

    @property
    def back_view(self):
        return Driver.d(resourceId="com.nonoapp:id/btn_titlebar_back")
