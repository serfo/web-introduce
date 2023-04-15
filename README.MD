运行项目：在该目录下执行python manage.py命令

文件说明：
mysql.py为数据库连接文件
requirements.txt为python依赖库，可根据内容自行pip install -r requirements.txt
games存放游戏的python代码
static存放静态文件：avatar用户头像、bootstrapUI框架、jqueryJS框架、layuiUI框架
，avatar/default文件夹中存放默认头像，最多可以放6个
templates存放网页文件：frame根页面(所有父页的继承)、index个人介绍、games游戏主界面
，games文件夹存放单个游戏页面
，content文件夹存放avatar头像编辑框、comment评论区、login登录框、setting设置框、zone个人空间
数据示例文件：以'_'开头的文件，可以通过数据表Import方式导入数据库，数据仅用于开发展示，用不到可以删除
