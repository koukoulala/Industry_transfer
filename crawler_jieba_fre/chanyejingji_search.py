# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import re


class chanyeSearch(object):

    search_page_url="http://www.cinic.org.cn/index.php?m=search&c=index&a=init&typeid=53&siteid=1&q={}&page={}"

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
            key_word_quote = parse.quote(key_word)
            url = chanyeSearch.search_page_url.format(key_word_quote,page)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                if r.status_code == 200:
                    #print(r.text)
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("ul", class_="imgtxtList3").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(chanyeSearch.item)
                            title_node = result.find("h3")
                            item_ins['link'] =title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("span").get_text()
                            item_ins["date"] = result.find("span", class_="sp2").get_text()
                            result_list["result_list"].append(item_ins)
                            # 把title和abstract写入文件。其他内容可以留作扩展
                            f = open("data/chanyejingji/result.txt", 'a')
                            f.write(item_ins['title'])
                            f.write(item_ins['abstract'])
                        except BaseException as e:
                            logging.error("Parse 产业经济 result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get 产业经济 search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = chanyeSearch.search_page("转移", page=2)  # 已经测试过了,运行正常
    # print(url_list["result_list"])
    for t in url_list["result_list"]:
        print(t)
