from App.Driver import Driver


class WelcomePage:

    @property
    def button(self):
        return Driver.d(resourceId="com.nonoapp:id/btn",text='立即注册领1888新手福利')
