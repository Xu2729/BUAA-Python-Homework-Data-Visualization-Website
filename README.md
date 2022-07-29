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
```

运行服务

```shell
python manage.py runserver
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
```

运行服务

```shell
python3 manage.py runserver
```