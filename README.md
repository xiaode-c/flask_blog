本项目由python flask框架组成

运行本项目前，需要先改config.py中的mysql配置，这里user指mysql用户名,一般是root; password是user的密码;host为主机地址,本地时一般为localhost; dbname为你的数据库名，需要事先建好

**注意：**由于我使用的是多说评论，因此你需要将app/templates/layout.html中的duosuo_short_name改为你自己的，我在文件中已经做了标记

```
virtualenv venv
source venv/bin/active   #linux下激活虚拟环境
pip install -r requirements.txt
pythom manage.py initdb
python manage.py runserver

```


在上面的命令中将自动创建用户: admin 密码为:123456 ,用来登录后台`/admin/login`

