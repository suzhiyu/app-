# -*- coding: utf-8 -*-
from App.Driver import Driver

class SafeKeyboard:
    def click_confirm_button(self):
        if Driver.d.device_info['serial'] == "APU7N16908000390":
            Driver.d.click(0.881, 0.823)
            return
        Driver.d(text='确定').click()


if __name__ == "__main__":
    d = Driver.init_dirver('192.168.33.5')
    d(text='确定').click()
