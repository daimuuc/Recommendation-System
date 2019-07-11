项目名称：
    音乐推荐系统
项目功能：
    基于Apriori算法实现对音乐类型推荐
项目结构：
    |----- uploads（客户端上传文件存储目录）
    |
    |----- apriori.py (实现Apriori算法)
    |
    |----- client.py (模拟客户端请求)
    |
    |----- config.py （配置文件）
    |
    |----- recommendation.py（基于Apriori算法实现推荐功能.）
    |
    |----- server.py（基于Flask的服务端API）
    |
    |----- utils.py（常用工具函数）
项目部署：
--Linux
  1、修改config.py文件（配置ssl）
  2、运行server.py文件
  3、修改client.py文件（配置域名）
--Windows、mac
  1、修改server.py文件（取消ssl配置）
  2、修改clien.py文件（配置域名）
