rethinkdb_port=8090
atx_server_port=8000

function checkServer(){
    echo -e "\n检查"$1"服务状态:"
 result=$( ps -ef | grep  $1 | grep -v grep | wc -l )
if [ $result -gt 0 ];then
    echo $1 "正在运行..."
    return 0;
else
    echo    $1 "----服务尚未启动----"
    return 1;
fi
}

function startRethinkDB()
    {
        # checkServer rethinkdb
    if !( command -v rethinkdb >/dev/null );then
        if !( command -v brew >/dev/null );then
            installBrew
        fi
        echo '安装rethinkdb...'
        brew update && brew install rethinkdb
    fi
    echo '----启动rethinkdb服务----'
    rethinkdb --http-port ${rethinkdb_port} &
    sleep 6
    }


function startAtxServer(){
    # checkServer atx-server
    project_dir=~/go/src/github.com/openatx/atx-server
    if !(command -v go > /dev/null);then
        if !( command -v brew >/dev/null );then
            installBrew
        fi
        echo '安装golang...'
        brew update && brew install go
    fi
    if test -d ${project_dir};then
            echo 'atx-server dir exists...'

    else
        echo 'go get atx-server project ...'
        go get -v github.com/openatx/atx-server
    fi
    cd  $project_dir
    #go build                      #build failed...
    chmod +x ./atx-server
    echo '----启动axt-server服务----'
     ./atx-server --port ${atx_server_port} &



}

function killAtxServer(){
   pid=$(ps -ef | grep atx-server)

}

function restartAtxServer(){
echo "restart..."

}
function installBrew(){
    echo 'install HomeBrew...'
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

}



function isFreePort(){
echo "check..."

}

#set -x
if [ $(uname) != 'Darwin' ];then
    echo 'this script is for Mac OS'
    exit 1
fi


if [ $1 == start ];then
    startRethinkDB
    startAtxServer
    while true; do
    #statements
    checkServer atx-server
    if [ $? -ne 0 ];then startAtxServer ;fi
    checkServer rethinkdb
    if [ $? -ne 0 ];then startRethinkDB;fi
    echo -e "休眠10秒钟...\n"
    sleep 10
    done
elif [[ $1 == kill ]]; then
        #statements
        pid=$(ps -ef | grep atx-server | grep -v grep | awk '{print $2}')
        if test -z "${pid}";then
            echo -e "atx-server 服务并未启动..."
            exit 0
        fi
        kill -9 ${pid}
        if [ $? -eq 0 ];then
            echo -e "atx-server服务已经停止..."
        fi
        
fi
