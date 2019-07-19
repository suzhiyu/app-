#for i in `seq 1 2`;do

function install(){
    #安装相关工具
    brew update && brew install jq
    pip3 install pipreqs

}


if [[ "$1" == "install" ]];then
    install
    exit 0
fi

if !(test -z "$1");then
    devices=$1
    else
    #从atx-server获取可用设备ip，如果执行entrypoint.sh脚本的时候没有传设备ip，就直接用获取到的设备ip
    ATX_SERVER=http://192.168.28.48:8000/list
    filename=devices.json
    wget -O ${filename} ${ATX_SERVER}
    ip_list=$(jq .[].ip  ${filename} | sed 's/"//g')
    for ip in ${ip_list};do
    devices=${ip}/${devices}
    done

fi
echo ${devices}


# 导出依赖文件
pipreqs --force ./App
#安装自动化项目依赖库
pip3 install  --upgrade -r ./App/requirements.txt
#备份自动化测试报告文件夹
python3 report.py backup
#执行自动化测试
python3 App/TestCase  -d ${devices}
#汇总自动化测试报告
python3 report.py index