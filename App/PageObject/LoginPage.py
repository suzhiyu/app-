from App.Driver import Driver


class LoginPage:
    @property
    def username_view(self):
        return Driver.d(resourceId="com.nonoapp:id/et_username")

    @property
    def password_view(self):
        return Driver.d(resourceId="com.nonoapp:id/et_password")

    @property
    def login_view(self):
        return Driver.d(text=u"登录")

    @property
    def switch_env_view(self):
        return Driver.d(text='切换测试环境')

    @property
    def register_view(self):
        return Driver.d(text='注册')