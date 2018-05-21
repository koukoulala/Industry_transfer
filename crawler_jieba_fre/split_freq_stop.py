import os
import jieba
import logging

def set_stop(stop_path):
    stop_list=[]
    fp=open(stop_path,"r",encoding="UTF-8")
    lines=fp.readlines()
    for line in lines:
        line=line.strip().split()
        #print(line)
        for t in line:
            #print(t)
            stop_list.append(t)
    print(stop_list)
    return stop_list

def split_freq_stop(data_path,freq_path,stop_list):
    catelist = os.listdir(data_path)  # 获取所有子目录
    # 获取每个目录（类别）下所有的文件
    for mydir in catelist:
        class_path = data_path + mydir + "/"  # 拼出子目录的路径
        fre_dir = freq_path + mydir + "/"  # 拼出统计词频后存贮的对应目录路径如：
        if not os.path.exists(fre_dir):  # 是否存在词频目录，如果没有则创建该目录
            os.makedirs(fre_dir)

        file_list = os.listdir(class_path)  # 获取未统计词频语料库中所有文本
        for file_path in file_list:  # 遍历类别目录下的所有文件
            fullname = class_path + file_path  # 拼出文件名全路径如：data/xiuxiu/hou.txt
            word_list = []
            key_list = []
            for line in open(fullname):  # 是需要分词统计的文档
                item = line.strip('\n')
                tags=list(jieba.cut(item)) #用jieba分词对每行内容处理成一个个单词
                for t in tags:
                    if t not in stop_list:
                        word_list.append(t)
                    #else:
                        #print(t)

            print("分词+去除停用词结束")

            word_dict = {}
            with open(fre_dir + file_path, 'w') as wf2:  # 词频存储进文件
                for item in word_list:
                    if item not in word_dict:  # 统计数量
                        word_dict[item] = 1
                    else:
                        word_dict[item] += 1
                orderList = list(word_dict.values())
                orderList.sort(reverse=True)
                print(orderList)

                for i in range(len(orderList)):
                    for key in word_dict:
                        if word_dict[key] == orderList[i]:
                            try:
                                wf2.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
                                key_list.append(key)
                                word_dict[key] = 0
                            except BaseException as e:
                                logging.error( str(e))

            print(fre_dir + file_path,"完成")


if __name__ == "__main__":
    stop_list=set_stop("./hlt_stop_words.txt")
    split_freq_stop("./data/", "./data_fre/",stop_list)