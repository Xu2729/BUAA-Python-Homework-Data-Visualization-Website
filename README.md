# 运行方法

## Windows

建立虚拟环境

```shell
virtualenv venv
# 如果报错可能是没安装virtualenv，需要用pip install virtualenv先安装
```

进入虚拟环境

```shell
cd venv/Scripts
activate.bat
# 回到原来的目录
cd ../../
```

安装依赖

```shell
pip install -r requirements.txt
# 如果这一步出问题，请手动输入这四条命令
pip install django
pip install pandas
pip install pyecharts
pip install pymysql
# 如果仍有问题，建议利用搜索引擎解决
```

运行服务

```shell
python manage.py runserver
# 之后在浏览器上打开 http://127.0.0.1:8000/index 就能看到效果图了

# 如果想部署在服务器上让别人访问，应该先将 djangoProject1/settings
# 中的第26 行改为 DEBUG = False，然后使用下面的命令
python manage.py runserver 0.0.0.0:8000
# 这样就能通过 <ip>:8000 进行访问了
```

## Linux

建立虚拟环境

```shell
virtualenv venv
# 如果报错可能是没安装virtualenv，需要用pip3 install virtualenv先安装
```

进入虚拟环境

```shell
source venv/bin/activate
```

安装依赖

```shell
pip3 install -r requirements.txt
# 如果这一步出问题，请手动输入这四条命令
pip3 install django
pip3 install pandas
pip3 install pyecharts
pip3 install pymysql
# 如果仍有问题，建议利用搜索引擎解决
```

运行服务

```shell
python3 manage.py runserver
# 之后在浏览器上打开 http://127.0.0.1:8000/index 就能看到效果图了

# 如果想部署在服务器上让别人访问，应该先将 djangoProject1/settings
# 中的第26 行改为 DEBUG = False，然后使用下面的命令
python3 manage.py runserver 0.0.0.0:8000
# 这样就能通过 <ip>:8000 进行访问了
```

## 关于数据库

目前仓库中的 config.yaml 使用的是 ECS 的 MySQL 数据库，可能比较慢，开发用建议修改为本地数据库

首次使用数据库需要先在项目根目录执行以下两条命令建表，当 models.py 文件被修改时同样需要执行该操作

```shell
# 如果在 linux 环境下则是 python3
python manage.py makemigrations
python manage.py migrate
```
