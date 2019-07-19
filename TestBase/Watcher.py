from threading import Thread,Event
from TestBase.UiHelper import UiHelper
import time


class Watcher(Thread,UiHelper):
    def __init__(self,**kwargs):
        super(Watcher,self).__init__()
        self._run_flag = Event()
        self._run_flag.set()
        self._alive_flag = Event()
        self._alive_flag.set()
        self.args = kwargs

    def run(self,):
        while self._alive_flag.isSet():
            self._run_flag.wait()
            self.d(**self.args).click_exists(timeout=1)
            time.sleep(2)

    # def _click(self,):
    #     if self.args.get("text") is not None:
    #         self.d(text=self.args.get("text"), ).click_exists(timeout=1)
    #     elif self.args.get("resourceId") is not None:
    #         self.d(resourceId=self.args.get("resourceId")).click_exists(timeout=1)
    #     elif self.args.get("xpath") is not None:
    #         self.d(xpath=self.args.get("xpath")).click_exists(timeout=1)

    def restart(self):
        self._run_flag.set()

    def pause(self):
        self._run_flag.clear()

    def stop(self):
        self._run_flag.set()
        self._alive_flag.clear()