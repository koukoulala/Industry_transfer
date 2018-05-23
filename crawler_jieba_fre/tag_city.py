import os
import jieba
import re
import logging
import jieba.posseg

def set_stop(stop_path):
    stop_list=[]
    fp=open(stop_path,"r",encoding="UTF-8")
    lines=fp.readlines()
    for line in lines:
        line=line.strip().split()
        for t in line:
            stop_list.append(t)
    return stop_list

def set_city(city_path,stop_list):
    city_list=[]
    '''
    for line in open(city_path):
        item = line.strip('\n')  # 移除字符串头尾指定的字符
        tags = list(jieba.cut(item))  # 用jieba分词对每行内容处理成一个个单词
        for j in range(0, len(tags)):
            if tags[j] not in stop_list:
                city_list.append(tags[j])

    '''
    fp = open(city_path, "r", encoding="UTF-8")
    lines = fp.readlines()
    for line in lines:
        line = line.strip('\n')
        line=re.split(r'[\s\,\[\"\'\"\]]+',line)
        for t in line:
            city_list.append(t)

    return city_list

def set_word(word_path):
    out_word_list = []
    fp = open(word_path, "r", encoding="UTF-8")
    lines = fp.readlines()
    for line in lines:
        line = line.strip().split()
        for t in line:
            out_word_list.append(t)
    return out_word_list

def split_tag_stop(data_path,res_path,stop_list,city_list,out_word):
    catelist = os.listdir(data_path)  # 获取所有子目录
    # 获取每个目录（类别）下所有的文件
    for mydir in catelist:
        if mydir=='.DS_Store':
            continue
        class_path = data_path + mydir + "/"  # 拼出子目录的路径
        res_dir = res_path + mydir + "/"  # 拼出分词后转移到的城市存储路径
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)

        file_list = os.listdir(class_path)  # 获取语料库中所有文本
        for file_path in file_list:  # 遍历类别目录下的所有文件
            if file_path == '.DS_Store':
                continue
            fullname = class_path + file_path  # 拼出文件名全路径如
            word_list = []
            res_city=set()

            for line in open(fullname):  # 是需要分词统计的文档
                flag = 0
                item = line.strip('\n')   #移除字符串头尾指定的字符
                tags=list(jieba.cut(item)) #用jieba分词对每行内容处理成一个个单词
                for j in range(0,len(tags)):
                    if tags[j] not in stop_list:
                        word_list.append(tags[j])
                        if flag==1:
                            if tags[j] in city_list:
                                print(tags[j])
                                res_city.add(tags[j])
                        if tags[j] in out_word:
                            flag=1

            print(res_city)
            print("分词+得到转移后的城市结束")

            with open(res_dir + file_path, 'w') as wf2:  # 城市存储进文件
                for item in res_city:
                    wf2.write(str(item)+'\n')


            print(res_dir + file_path,"完成")


if __name__ == "__main__":
    stop_list=set_stop("stop_city_seg/hlt_stop_words.txt")
    city=set_city("stop_city_seg/city2.txt",stop_list)
    out_word=set_word("stop_city_seg/out_word2.txt")
    #city=['乌鲁木齐','呼和浩特','兰州','哈尔滨']
    #out_word=['转移','转向']
    split_tag_stop("./data/", "./data_res/",stop_list,city,out_word)