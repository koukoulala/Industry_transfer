# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import re


class dsjSearch(object):

    search_page_url="http://www.36dsj.com/page/{}?s={}"

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
            url = dsjSearch.search_page_url.format(page,key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:

                r = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'})
                if r.status_code == 200:
                    #print(r.text)
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    # 如果一个页面的class属性为rb, 则此链接点击进去后不是一个单独的与页面,此处记录一下即可.
                    result_links = bs_obj.find("div", class_="content").findAll("article")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(dsjSearch.item)
                            title_node = result.find("h2")
                            item_ins['link'] =title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("p", class_="note").get_text()
                            item_ins["date"] = result.find("p", class_="info").get_text()
                            item_ins["date"] = re.search(r"(\d{4}-\d{2}-\d{2})", item_ins["date"]).group(0)
                            result_list["result_list"].append(item_ins)
                        except BaseException as e:
                            logging.error("Parse 36大数据 result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get 36大数据 search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    url_list = dsjSearch.search_page("人工智能", page=2)  # 已经测试过了,运行正常
    # print(url_list["result_list"])
    for t in url_list["result_list"]:
        print(t)
