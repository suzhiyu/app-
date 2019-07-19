# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import time
import zipfile
from jinja2 import Environment, FileSystemLoader
from fire import Fire
import shutil

__dir__ = os.path.dirname(os.path.abspath(__file__))
test_report_dirname = 'TestReport'
test_report_path = os.path.join(__dir__,test_report_dirname)
report_filename = 'testreport.html'

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(__dir__, )),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(*args,filename="自动化测试报告.html"):
    name = os.path.join(os.path.join(__dir__,test_report_dirname),filename)
    urls = args
    context = {
        'urls': urls
    }
    with open(name, 'w', encoding="utf-8") as f:
        html = render_template('index.html', context)
        f.write(html)




def get_device_report_info(report_file):
    '''根据运行设备的数量生成统计报告，路径为
    ./TestReport/自动化测试报告.html'''
    result = {}
    with open(report_file, 'r', encoding='utf-8') as f:
        html = f.read()
        res_str = re.findall("测试结果(.+%)", html)
        if res_str:
            res = re.findall(r"\d+", res_str[0])
            result['name'] = re.search('<h1.*>(.*?)</h1>',html).group(1)
            result["sum"] = res[0]
            result["pass"] = res[1]
            result['fail'] = res[2]
            result['error'] = res[3]
            result['passrate'] = re.findall('通过率 = (.+%)', res_str[0])[0]
            result['duration'] = re.search("<strong>合计耗时 : </strong> (.*?)</p>", html).group(1)
    result['urls'] = report_file
    return result


def backup_report():
    if not os.path.exists(test_report_path):
        print(test_report_path,'不存在...,无需备份')
        return

    '''备份旧报告 TestReport文件夹'''
    test_report_backup_path = os.path.join(__dir__,"TestReport_backup")

    backup_date_dir_name = os.path.join(test_report_backup_path,time.strftime('%Y%m%d', time.localtime()))
    if not os.path.exists(backup_date_dir_name):
        os.makedirs(backup_date_dir_name)
    back_time = time.strftime('%H%M%S',time.localtime())
    if os.listdir(test_report_path):
        os.rename(test_report_path,os.path.join(backup_date_dir_name,'Back_up_'+back_time))
        print('备份成功')



def zip_report():
    '''压缩TestReport文件夹'''
    name = 'TAX-Report ' + time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
    startdir = "./TestReport"  # 要压缩的文件夹路径
    file_news = './' + name + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            # z.write(os.path.join(dirpath, filename))
    z.close()
    print('Generate zip_report file %s completed........ ' % file_news)


def main():
    dirs = os.listdir(test_report_path)
    os.chdir(test_report_path)
    report_info_list = []
    for dir in dirs:
        device_report_path = os.path.join(test_report_path, dir)
        if os.path.isdir(device_report_path):
            report_file = os.path.join(os.path.join('.', dir), report_filename)
            report_info = get_device_report_info(report_file)
            report_info_list.append(report_info)

    create_index_html(*report_info_list)


#todo class Report
class Report:
    def backup(self):
        backup_report()

    def index(self):
        main()


if __name__ == "__main__":
    Fire(Report)


