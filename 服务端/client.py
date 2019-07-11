#-*- coding: UTF-8 -*-
"""
模拟客户端请求，测试服务端3个API功能.
"""

from __future__ import print_function, division
import requests

################################################################################
#函数入口
################################################################################
if __name__ == '__main__':
    # 配置信息
    configuration = {
        'min_support': 0.003, 'min_confidence' : 0.2,
        'min_lift' : 3, 'max_length' : 5,
        'num' : 10,
        'data_num': 7500, 'data_max_length': 20
    }

    # 上传文件信息
    files = {
        'file' : open('Music_Recommendation.csv', 'rb')
    }

    # 测试自定义文件请求API
    # results = requests.post('https://www.ponma.cn:5000/custom', \
    #                              data = configuration,
    #                              files = files)

    # 测试上传文件请求API
    # results = requests.post('https://www.ponma.cn:5000/upload',
    #                         files = files)

    # 测试随机文件请求API
    results = requests.get("https://www.ponma.cn:5000/random", params = configuration)

    # 显示结果
    results = results.json()
    for k, v in results.items():
        print(k, ' ', v)
