# websrcnn-fastdfs
基于SRCNN(超分辨率卷积神经网络)的图片超分辨率系统，同时图片相关信息放在fastdfs图片服务器上
# 使用教程
## 安装要求
1，一台fastdfs图片服务器
2，Python 3
3，Tensorflow
4，Numpy
5，Scipy
6，Opencv 3
7，h5py
8，Flask
9，Flask-SQLAlchemy，Flask-Script，Flask-Migrate
10，fdfs-client-py
## 安装步骤
### 数据库表的安装
```
1，cd 该项目的路径
2，打开configs.py
3，修改数据库的ip，端口，数据库名称，用户名称，密码
4，分别运行以下三条命令
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
```
### 图片服务器的连接
```
1，cd 该项目的路径/fastdfs
2，打开client.conf
3，修改base_path属性，改为你电脑上的存在的路径
4，修改tracker_server，改为你的fastdfs的tracker服务的ip以及对应端口
```
### 项目启动
```
python runserver.py
```
运行结果如下
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582351529269_BE6FC83BEB3DEFCE9F752AD1599DC7AC "图片标题") 
## 项目功能及使用
### 图片上传
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582351974103_A8A6004111D282A88624F8BEB080B45A "图片标题") 
### 图片细节展示
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352296246_A4DB16B6A8A055782206934569E9EFE1 "图片标题") 
### 图片超分辨率处理
点击超分辨率处理
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352342678_4E8D414B797197D51BD9557DCD960575 "图片标题") 
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352396726_EB2E6DC07D167FB363CA939EF3096B77 "图片标题") 
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352413676_CF39AFB474428058BCBE8A2D32A3FF4F "图片标题") 
生成一张相对于原图更加清晰(锐度较原图较高，边缘部分加深)的图片
### 图片放大
可放大两倍和三倍，这里以放大两倍为例
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352566845_18B2327B9CE99F8F14C0D544F7CF8454 "图片标题") 
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352607015_8C2DED2E058B5D8394F84191DBBF4EA6 "图片标题") 
点击2x
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352640457_FC11DFB1E11CC07DD22DD89ED26A6FD4 "图片标题") 
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352681047_2B1DA0F9405E6A30DF235BFD7D4C76C6 "图片标题") 
### SRCNN和传统方法的对比
![图片说明](https://uploadfiles.nowcoder.com/images/20200222/893848252_1582352718051_BEB1EB8CF1C9F60269D1ED5FFB2FD0EA "图片标题") 
![图片说明](https://uploadfiles.nowcoder.com/compress/mw1000/images/20200222/893848252_1582352744697_1355D961F91319D7057A4246332DE612 "图片标题") 
# 参考
1.[Dong, C., Loy, C.C., He, K., Tang, X.: Learning a Deep Convolutional Network for Image Super-Resolution.](http://mmlab.ie.cuhk.edu.hk/projects/SRCNN.html) 
2. [tegg89/SRCNN-Tensorflow](https://github.com/tegg89/SRCNN-Tensorflow)
# 作者
程从越/[chengcongyuegithub](https://github.com/chengcongyuegithub)
张雨萌/[zym1175098466](https://github.com/zym1175098466)  

