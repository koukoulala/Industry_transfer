# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import re


class xiaomuchongSearch(object):

    search_page_url="http://muchong.com/bbs/search.php?wd={}&fid=0&search_type=thread&mode=&order=&adfilter=0&page={}"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search_page(key_word, page):
        """
        爬取特定的页面
        :param key_word:
        :param search_page:
        :return:
        """
        result_list = {"result_list": []}
        try:
            #这个的中文编码是gb2312的
            key_word_quote = parse.quote(key_word.encode('gb2312'))
            url = xiaomuchongSearch.search_page_url.format(key_word_quote,page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                if r.status_code == 200:
                    #print(r.text)
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.findAll("tbody")[1:]
                    n=0;
                    for result in result_links:
                        try:
                            item_ins = deepcopy(xiaomuchongSearch.item)
                            title_node = result.find("th",class_="t_new").find("span")
                            item_ins['link'] =title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("div").get_text()
                            item_ins["date"] = bs_obj.findAll("nobr")[n].get_text()
                            item_ins["date"] = re.search(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})", item_ins["date"]).group(0)
                            result_list["result_list"].append(item_ins)
                            n+=1
                            # 把title和abstract写入文件。其他内容可以留作扩展
                            f = open("data/third/guangzhou.txt", 'a')
                            f.write(item_ins['title'])
                            f.write(item_ins['abstract'])
                        except BaseException as e:
                            logging.error("Parse 小木点 result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get 小木点 search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    for i in range(1, 10):
        url_list = xiaomuchongSearch.search_page("广州 服务业 转移", page=i)  # 已经测试过了,运行正常
        # print(url_list["result_list"])
        for t in url_list["result_list"]:
            print(t)
