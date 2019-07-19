from uiautomator2 import connect

d = connect()
d.service('uiautomator').stop()
# Maxim正常运行
task = d.shell("CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar "
                    "exec app_process /system/bin tv.panda.test.monkey.Monkey -p com.nonoapp "
                    "--running-minutes 20 --throttle 500 --uiautomatormix --output-directory /sdcard/max-output", stream=True) # stream模式，保证不会timeout导致杀掉，底层上是一个requests库提供的streaming 模式的response
try:
    for line in task.iter_lines():
        print(line)
finally:
    task.close()
print('Done')
d.service('uiautomator').start()
d.press('home')