***基于角色权限控制的通用管理后台***  

****

# 环境
## 服务器
ubuntu

## 前置服务
### redis服务
安装命令：apt install redis-server

### mysql服务
安装命令：apt install mysql-server


## python
### python版本
python3.6

### python包
见requirements.txt，执行 ”pip install -r requirements.txt” 命令，安装所有依赖包

# 部署
## 初始化数据库
执行“python bin/mysql_init.py”，初始化数据库

## 修改fastapi源码
规定默认的返回数据格式为：{'code':'', 'msg':'', 'data':{}, 'extra':{}}，而fastapi中默认raise HttpException后返回的数据格式为{'detail': {}}，这与自定义的返回数据格式风格不一致，所以需要修改fastapi的源码，fastapi/exception_handlers.py中的http_exception_handler方法，新增以下代码：
```
if isinstance(exc.detail, dict):
    detail = exc.detail
else:
    detail = {"detail": exc.detail}
```

## 运行服务
### 方式一，通过uvicorn启动
命令：uvicorn main:app --host '0.0.0.0' --port 8000 --reload  
其中：
* '0.0.0.0'是要运行的主机ip
* 8000是要指定的端口

### 方式二，通过supervisor启动
1. 安装supervisor，“apt install supervisor”
2. 配置supervisor，一般在/etc/supervisor/conf.d目录下，新建一个 xx.conf的文件，命令介绍：
```
[program:x]：配置文件必须包括至少一个program，x是program名称，必须写上，不能为空
command：包含一个命令，当这个program启动时执行
directory：执行子进程时supervisord暂时切换到该目录
user：账户名
startsecs：进程从STARING状态转换到RUNNING状态program所需要保持运行的时间（单位：秒）
redirect_stderr：如果是true，则进程的stderr输出被发送回其stdout文件描述符上的supervisord
stdout_logfile：将进程stdout输出到指定文件
stdout_logfile_maxbytes：stdout_logfile指定日志文件最大字节数，默认为50MB，可以加KB、MB或GB等单位
stdout_logfile_backups：要保存的stdout_logfile备份的数量
```
3. 通过配置文件启动supervisor服务，“supervisord -c supervisor.conf”
4. supervisor基本命令（后四个命令可以省略“-c supervisor.conf”）
```commandline
supervisord -c supervisor.conf                       通过配置文件启动supervisor
supervisorctl -c supervisor.conf status              查看状态
supervisorctl -c supervisor.conf reload              重新载入配置文件
supervisorctl -c supervisor.conf start [all]|[x]     启动所有/指定的程序进程
supervisorctl -c supervisor.conf stop [all]|[x]      关闭所有/指定的程序进程 
```
5. 运行服务
```commandline
sudo supervisorctl start 服务名
```

# 改动
## 数据库改动所引起的改动
执行bin/models_db_mysql_update.py，重新加载数据表信息到models/db_mysql.py中

# 注意
t_permission权限表，不可人为改动，即不开放添加、修改、删除等功能给用户，只能展示。因为所有功能需要通过代码鉴权，如果修改了权限，可能会导致代码鉴权失败。  
即使一定要开放给用户，也只能增不能删，且修改时不可修改code字段
