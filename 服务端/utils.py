#-*- coding: UTF-8 -*-
"""
常用工具函数
random_generate_data:
    随机生成用户音乐类型数据,以csv文件保存
show_data_info:
    展示random_generate_data函数生成的csv文件相关统计信息
"""

from __future__ import print_function, division
import random
import csv
import pandas as pd

################################################################################
# 随机生成用户音乐类型数据,以csv文件保存,
# 指定保存路径为./Music_Recommendation_Random.csv,
# 文件中每一条记录表示为一个用户近期所听音乐类型.
################################################################################
def random_generate_data(**kwargs):
    """
    随机生成用户音乐类型数据

    :kwargs
        num -- 随机生num条数据(int).
        max_length -- 每条数据最多拥有max_length个音乐类型(int), max_length <= 20.
    """

    # 解析参数
    num = kwargs.get('num', 7500)
    max_length = kwargs.get('max_length', 20)

    # 指定csv文件保存路径
    path = './Music_Recommendation_Random.csv'

    # 音乐种类，共计120种，来源https://www.musicgenreslist.com/
    music = ['Art Punk', 'Alternative Rock', 'Britpunk', 'College Rock', 'Crossover Thrash', 'Crust Punk',
             'Emotional Hardcore',
             'Experimental Rock', 'Folk Punk', 'Goth / Gothic Rock', 'Grunge', 'Hardcore Punk', 'Hard Rock',
             'Indie Rock', 'Lo-fi',
             'Musique Concrète', 'New Wave', 'Progressive Rock', 'Punk', 'Shoegaze', 'Steampunk', 'Anime',
             'Acoustic Blues', 'African Blues',
             'Blues Rock', 'Blues Shouter', 'British Blues', 'Canadian Blues', 'Chicago Blues', 'Classic Blues',
             'Classic Female Blues',
             'Contemporary Blues', 'Contemporary R&B', 'Country Blues', 'Delta Blues', 'Detroit Blues',
             'Electric Blues', 'Folk Blues', 'Gospel Blues',
             'Harmonica Blues', 'Hill Country Blues', 'Hokum Blues', 'Jazz Blues', 'Jump Blues', 'Kansas City Blues',
             'Louisiana Blues', 'Memphis Blues',
             'Modern Blues', 'New Orlean Blues', 'NY Blues', 'Piano Blues', 'Piedmont Blues', 'Punk Blues',
             'Ragtime Blues', 'Rhythm Blues',
             'Soul Blues', 'Lullabies', 'Sing-Along', 'Stories', 'Avant-Garde', 'Ballet', 'Baroque', 'Cantata',
             'Chamber Music', 'Chant', 'Choral',
             'Classical Crossover', 'Concerto', 'Concerto Grosso', 'Contemporary Classical', 'Early Music',
             'Expressionist', 'High Classical', 'Impressionist',
             'Mass Requiem', 'Medieval', 'Minimalism', 'Modern Composition', 'Modern Classical', 'Opera', 'Oratorio',
             'Orchestral', 'Organum', 'Renaissance',
             'Romantic', 'Sonata', 'Symphonic', 'Symphony', 'Wedding Music', 'Novelty', 'Parody Music ',
             'Stand-up Comedy', 'Vaudeville', 'Jingles', 'TV Themes',
             'Alternative Country', 'Americana', 'Australian Country', 'Bakersfield Sound', 'Bluegrass',
             'Blues Country', 'Cajun Fiddle Tunes', 'Christian Country',
             'Classic Country', 'Close Harmony', 'Contemporary Bluegrass', 'Contemporary Country', 'Country Gospel',
             'Country Pop', 'Country Rap', 'Country Rock',
             'Country Soul', 'Cowboy', 'Cowpunk', 'Dansband', 'Honky Tonk', 'Franco-Country', 'Gulf and Western',
             'Hellbilly Music', 'Honky Tonk']
    # 统一格式为'utf-8'
    temp = []
    for val in music:
        temp.append(val.encode('utf-8'))
    music = temp

    # 随机生成用户音乐类型数据.
    out = open(path, 'w', newline='')
    csv_write = csv.writer(out, dialect='excel')
    for i in range(num):
        # 随机生成该条数据拥有音乐类型个数
        length = random.randint(1, max_length)
        # 随机生成含有length个音乐类型的记录
        vals = random.sample(music, length)
        csv_write.writerow(vals)
    out.close()
    print("write over")

################################################################################
#展示random_generate_data函数生成的csv文件相关统计信息.
################################################################################
def show_data_info():
    """
    展示random_generate_data函数生成的csv文件相关统计信息.
    """
    # 文件路径
    path = './Music_Recommendation_Random.csv'

    # 加载数据
    dataset = pd.read_csv(path, names = list(range(0, 20)))

    # 统计文件中每个音乐类型出现的次数
    pairs = {}
    # 统计文件中每个音乐类型出现的次数之和
    total = 0
    for i in range(len(dataset)):
        for j in range(len(dataset.keys())):
            if str(dataset.values[i, j]) != 'nan':
                total += 1
                if dataset.values[i, j] in pairs.keys():
                    pairs[dataset.values[i, j]] += 1
                else:
                    pairs[dataset.values[i, j]] = 1

    # 展示统计结果
    print('统计结果如下')
    for k, v in pairs.items():
        print("%5s%5d" %(k, v))
    print('\n%5s %5d' %('total', total))

################################################################################
#函数入口
################################################################################
if __name__ == '__main__':
    # 随机生成用户音乐类型数据.
    # random_generate_data(num = 7500, max_length = 20)

    # 展示random_generate_data函数生成的csv文件相关统计信息.
    show_data_info()
