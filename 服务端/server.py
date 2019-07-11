#-*- coding: UTF-8 -*-
"""
基于Flask的服务端API.
process_random:
    响应随机生成数据请求.
process_custom:
    响应自定义数据请求.
upload_file:
    上传自定义文件
"""

from __future__ import print_function, division
from flask import Flask, request, jsonify
from utils import random_generate_data
from recommendation import recommedation
from werkzeug.utils import secure_filename
import os
import config

# 创建Flask类实例
app = Flask(__name__)

################################################################################
# 响应随机生成数据请求,请求方式为get.
################################################################################
@app.route('/random', methods = ['get'])
def process_random():
    """
     响应随机生成数据请求,以json格式返回结果
    """
    try:
        # 文件位置
        path = './Music_Recommendation_Random.csv'

        # 解析随机生成数据需要的参数
        # 随机生data_num条数据(int)
        data_num = int(request.args['data_num'])
        # 每条数据最多拥有data_max_length个音乐类型(int), data_max_length <= 20.
        data_max_length = int(request.args['data_max_length'])

        # 解析推荐需要的参数
        # 最小关系支持度值(support)(float)
        min_support = float(request.args['min_support'])
        # 最小关系置信度值(confidence)(float).
        min_confidence = float(request.args['min_confidence'])
        # 最小关系提升度值(lift)(float).
        min_lift = float(request.args['min_lift'])
        # 关系最大长度(int).
        max_length = int(request.args['max_length'])
        # 推荐lift得分最高的前num个组合，即推荐个数(int).
        num = int(request.args['num'])

        # 随机生成用户音乐类型数据
        random_generate_data(num=data_num, max_length=data_max_length)

        # 基于Apriori算法实现推荐功能.
        results_json = recommedation(path, min_support=min_support, min_confidence=min_confidence, \
                                     min_lift=min_lift, max_length=max_length, num=num)

        return results_json
    except Exception:
        results_json = {}
        results_json['status'] = 'Failure'
        return jsonify(results_json)

################################################################################
# 响应自定义数据请求,请求方式为post.
################################################################################
@app.route('/custom', methods=['post'])
def process_custom():
    """
    响应自定义数据请求,以json格式返回结果
    """
    try:
        # 解析参数
        # 最小关系支持度值(support)(float)
        min_support = float(request.form['min_support'])
        # 最小关系置信度值(confidence)(float).
        min_confidence = float(request.form['min_confidence'])
        # 最小关系提升度值(lift)(float).
        min_lift = float(request.form['min_lift'])
        # 关系最大长度(int).
        max_length = int(request.form['max_length'])
        # 推荐lift得分最高的前num个组合，即推荐个数(int).
        num = int(request.form['num'])

        # 存储上传文件的目录地址
        UPLOAD_FOLDER = './uploads'

        # 读取并保存上传文件
        file = request.files['file']
        # 判断文件是否存在和格式是否正确
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 文件存储路径
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            # 基于Apriori算法实现推荐功能.
            results_json = recommedation(path, min_support=min_support, min_confidence=min_confidence, \
                                         min_lift=min_lift, max_length=max_length, num=num)
            return results_json
        else:
            raise Exception
    except Exception:
        results_json = {}
        results_json['status'] = 'Failure'
        return jsonify(results_json)

################################################################################
# 上传自定义文件,请求方式为post.
################################################################################
@app.route('/upload', methods=['post'])
def upload_file():
    """
    上传自定义文件,以json形式返回上传状态
    """
    try:
        # 存储上传文件的目录地址
        UPLOAD_FOLDER = './uploads'

        # 读取并保存上传文件
        file = request.files['file']
        # 判断文件是否存在和格式是否正确
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 文件存储路径
            path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(path)

            # 返回结果
            results_json = {}
            results_json['status'] = 'Success'
            return jsonify(results_json)
        else:
            raise Exception
    except Exception:
        results_json = {}
        results_json['status'] = 'Failure'
        return jsonify(results_json)

################################################################################
# 内部函数,判断文件格式是否正确.
################################################################################
def allowed_file(filename):
    """
    判断文件格式是否正确,以boolean形式返回结果
    :param
        filename -- 文件名(str)
    """
    # 文件格式
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

################################################################################
# 函数入口.
################################################################################
if __name__ == '__main__':
    # ssl配置文件地址,可以参考https://blog.csdn.net/robin912/article/details/80698896
    pem = config.pem
    key = config.key

    # 运行程序并设置外部可访问
    app.run(port = 5000, host='0.0.0.0', debug = False, ssl_context = (pem, key))