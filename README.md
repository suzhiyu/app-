### 项目介绍：
  > 目前麦子金服财富`android`自动化项目，基本完成了`sit`回归案例的自动化转化，应用于每周版本发布时`sit`环境自动化的回归。  
  [jenkins自动化构建job地址](http://192.168.28.48:8080/jenkins/view/AUTOTEST-JOB/job/nonoapp-autotest/)  
  采用框架是目前社区较为流行的`atx-uiautomator2`，熟悉`appium`自动化测试工具的童鞋，理解这个工具也比较容易，同`appium`一样该框架也是支持`webdriver`协议，原理是在进行自动化之前，先在手机上安装了一个`http-server`的`apk`，并将这个`http-server`启动起来，他是基于`google`官方的自动化框架`uiautomator`封装而成，将其`api`开放出来供别人调用。对应的`http`请求库是`uiautomator2`，·只有`python`版本，所以目前测试案例的开发语言也是`python3`。
  > 原`ios`项目因为苹果签名限制，暂不能正常使用  
  
  * 手机环境搭建
    > 首先电脑上需要有`python`环境，通过`pip`包管理工具安装好自动化测试库:`pip3 install --pre uiautomator2`  
    然后将手机连上电脑，确保`adb devices`能正常看到测试设备。执行如下命令，将相应的测试依赖安装到手机  
  
     `python3 -m uiautomator2 init `
     
  * 项目基本结构:
  
  	```
  	|--App   
         |-- __init__.py  
            |-- PageObject App页面封装和业务步骤封装
            |-- TestCase   测试案例集文件夹  
                |-- __init__.py  
                |-- __main__.py 案例运行文件
                |-- conftest.py 基础测试类，testcase装饰器  
                |-- 其他测试模块文件
            |-- Driver.py 驱动模块  
            |-- db.py 
            |-- models.py orm  
            |-- utils.py 辅助模块  
            |-- HTMLTestReport.py 案例执行模块  
            |-- requirements.txt 项目依赖  
     |-- entrypoint.sh 项目运行脚本

  	```
 
* 快速运行项目： 

  > 项目目录下提供了一个`entrypoint.sh`脚本文件，可用于直接运行测试案例，脚本具体执行内容可以参看脚本注释。

    ```bash
      #项目clone到本地
      git clone  http://git.nonobank.com/liqiong/nonoapp-android-autotest.git
  		#安装依赖
      pip3 install -r requirements.txt
      #增加脚本执行权限
      chmod +x entrypoint.sh
      #运行测试脚本，多个手机ip可以用/隔开，如果不提供手机ip，则会从atx-server设备管理平台去获取可用设备列表
      ./entrypoint.sh $手机ip
  
      
    
    ```
    
    
    
### 案例维护（*`App/TestCase`*)

   > 初期的测试案例集仅包含`test_sit.py`,`test_sit_main.py`,`test_sit_static.py`三个测试文件，后期会基于功能点进行案例拆分，每个功能点创建一个单独的测试集文件，便于测试案例的横向纵向扩展。如下，该拆分任务目前在`testcase`分支进行。
   
 * 案例集

 	* `test_01_open_account.py` 开户
 	* `test_03_recharge.py` 充值
 	* `test_04_withdraw.py` 提现
 	* `test_05_invest.py` 投资

  
  
 * **`App/TestCase/conftest.py`文件**:主要提供测试`Hook机制`，案例失败重试，案例截图  

	> `conftest.py`文件主要包含测试的一些依赖方法和类：`BaseTest`基础测试类，`testcase`装饰器等。在基础测试类里面对测试的用到的`setUpClass`,`setUp`,`tearDown`,`tearDownClass`方法，具体方法执行内容可以参见方法注释。业务测试类可以集成`BaseTest`，然后只需在里面编写业务测试案例即可。`testcase`装饰器提供了失败重试和错误截图的功能，如果要在对应的测试案例执行的过程添加重试和失败截图功能，需要用`testcase`对其进行装饰，代码如下。
	
	```python
	from App.TestCase.conftest import testcase,BaseTest
	
	Class TestSample(BaseTest):
		
		@testcase
		def test_sample(self):
			pass
	```
 * **`App/TestCase/__main__.py`**:项目运行的入口文件  
 
 	 > `__main__.py`是案例的主要运行逻辑，可以通过`python3 App/TestCase`命令直接运行

 
 
### `PageObject`(*页面封装*)
   > 对于一些常用页面的页面元素已进行封装，编写自动化案例的时候如果要操作到这些页面的元素，可以导入相应的页面类进行调用。已封装的页面：
    
   + **MinePage.py** 我的页面
   + **DiscoverPage.py** 发现页面
   + **InvestPage.py**   出借页面
   + **SettingPage.py**  设置页面
   + **WithdrawPage.py** 提现页面
   + **RechargePage.py** 充值页面
   + **LoginPage.py** 登录页面
   + **OpenAccountPage** 开户页面
   
   ```python
   from App import HomePage,LoginPage
   from App.TestCase.conftest import BaseTest,testcase
   class TestSitSuite(BaseTest):

        @testcase(reruns=2)
        def test_01_sign_up(self,username=None):
            HomePage().mine_view.click()
            LoginPage().register_view.click()
            pass
   ```
    


### utils.py：一些额外功能
> 将一些其他需要的用到的方法、类放在了`utils`模块，主要会用到的`ocr()`方法，是调用百度的`orc`文字识别接口，对页面截图后，识别页面文字并获取到文字对应的中心坐标,然后进行相应的自动化操作，对于某些`webview`页面，控件无法正常解析，但又包含文字的情况,可以采用这种方式，如风险测评页。

```python
from App.utils import ocr

options = ['D.', 'D.', 'D.', 'D.', 'E.', 'E.', 'D.', 'A.']
ocr("开始测评").click()
for index,option in enumerate(options):
    print("{0}/ 8题:".format(index + 1), end='')
    ocr(textContains=option).click()

```

### git分支开发流程:  

 > 1.目前项目的主要两个分支为`master`分支和`dev`分支(开发分支)。其中`master`分支为稳定分支，主要用于每次自动化测试的构建运行。
 如果遇到`App``UI`界面更新或者新业务`case`增加，可以基于`master`分支创建对应版本的业务开发分支如：`v6.0.2`，用于该版本的业务
 `case`开发，开发测试完成，再将该版本分支合并到`master`分支。  
 > 2.`dev`分支为框架开发分支，主要用于框架本身功能的开发更新，在`dev`分支每完成开发一个小功能，测试通过后则可以合并到`master`分支。  
 > 3.当进行多人协作开发的时候，不同的业务童鞋可以将项目`clone`到本地，创建自己的业务开发分支，维护更新自己模块的自动化案例,开发测试完  
 成，可以提交到远程仓库，并申请合并到`master`分支，由项目管理员审核通过后，进行合并。  
 (为避免代码提交混乱，`master`分支可设为保护分支，专门由项目管理员维护。）
 
        
### 	其他自动化服务
* [weditor页面元素解析工具](http://192.168.28.48:17310)
* [atx-server android设备管理平台](http://192.168.28.48:8000)  


### *`TODO List`*：
   
   + `App`安装流程（`Jenkins`）
   + 代码覆盖率收集
   + 判断元素可用状态`clickable=true`
   + 命令行工具：`uirunner-cli` 创建项目结构，生成测试集文件
   + ~~apk需求:获取包名，扫描二维码~~
   + 服务监控平台: `atx`、`jenkins`、`nginx`、`mongodb`、`weditor`
   + `@testcase`的使用暂时需要将测试类导入`__init__.py`文件
   + `monkey`命令执行
   + `ios`环境脚本
   + ~~多机调试~~
   + `git submodule add` 增加 `android`项目 
   + ~~跳过案例~~
   + `atxserver2`支持模拟器的连接
   + `docker machine`使用宿主机`usb`接口
   + 打包默认为`sit`环境
   + `ios`自动安装应用
   + 覆盖安装测试
   + ~~jenkins报告发送~~
   + ~~步骤`invest_pay_steps`换用键盘点击输入~~
   + `ios monkey test`
   + `andorid_monkey_test`


### 其他    
* *问题*
   + 小米`note3` `7.0` webview页面元素无法正常解析
   + ~~华为 `NXT-TL00`   `6.0.1` 安全密码控件确定按钮能正常解析，但点击操作失败（兼容方式）~~
   
* *不稳定案例*
   + 风险测试评，仍沿用ocr功能
   + 诺诺盈散标金额元素被遮挡
   + 债转购买不支持并发
   + ~~开户,密码键盘返回~~
   + 诺诺盈购买闪退
   + `atx-server`小米模拟点击失效
   + 散标购买`crash`问题
   + 主线程是否添加重试机制Exception：`AttributeError` `__main__` `retry`
       


