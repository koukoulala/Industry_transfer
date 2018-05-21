# coding=utf-8

from copy import deepcopy
from urllib import parse
from bs4 import BeautifulSoup
import logging
import requests
import json
import time

class TaiMeiTiSearch(object):
    """
    利用搜狗搜索得到的微信文章的结果.
    """

    search_url = "http://www.tmtpost.com/search?q={}"
    search_page_url="http://www.tmtpost.com/ajax/search/get?url=%2Fsearch%2Fquery%2Fgroup&data=if_keyword_highlight%3Dtrue%26subtype%3Dpost%26limit%3D10%26offset%3D{}8%26keyword%3D{}"

    item = {"title": None, "abstract": None, "link": None, "date": ""}

    @staticmethod
    def search(key_word, search_page=5):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.(从第一页到search_page页）
        :return: 返回字典, {}
        """
        result_list = {"result_list": []}
        max_page = search_page
        try:
            key_word_quote = parse.quote(key_word)
            url = TaiMeiTiSearch.search_url.format(key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    bs_obj = BeautifulSoup(r.content, "html.parser")
                    result_links = bs_obj.find("div", class_="part mod-article-list").findAll("li")
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TaiMeiTiSearch.item)
                            title_node = result.find("div", class_="cont")
                            item_ins['link'] = 'http://www.tmtpost.com'+title_node.find("a").get("href")
                            item_ins['title'] = title_node.find("a").get_text()
                            item_ins['abstract'] = result.find("p", class_="intro").get_text()
                            item_ins["date"] = result.find("span", class_="author").get_text()
                            item_ins["date"]=item_ins["date"][-17:]
                            result_list["result_list"].append(item_ins)
                            # 把title和abstract写入文件。其他内容可以留作扩展
                            f = open("data/taimeiti/result.txt", 'a')
                            f.write(item_ins['title'])
                            f.write(item_ins['abstract'])
                        except BaseException as e:
                            logging.error("Parse Taimeiti result error. ErrorMsg: %s" % str(e))
                    next_page = bs_obj.find("p", class_="load-more load-post")
                    if next_page:
                        url = next_page.get("href")
                    else:
                        url = ""
                    failure = 0
                    max_page -= 1
                    if max_page <= 0:
                        break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get Taimeiti search result error. ErrorMsg: %s" % str(e))
        return result_list

    @staticmethod
    def search_page(key_word, page):
        """
        利用关键字进行搜索, 搜索结果返回指定页数,
        :param key_word: 关键字.
        :param search_page: 需要返回几页结果.
        :return: 返回字典, {}
        """
        result_list = {"result_list": []}
        try:
            key_word_quote = parse.quote(key_word)
            url = TaiMeiTiSearch.search_page_url.format(page,key_word_quote)
            failure = 0
            # url用来控是否有下一页, failure 用来控制失败次数
            while len(url) > 0 and failure < 10:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    result_links = json.loads(r.content, encoding='utf-8')['data']['post']
                    for result in result_links:
                        try:
                            item_ins = deepcopy(TaiMeiTiSearch.item)
                            item_ins['link'] = 'http://www.tmtpost.com/' + str(result['guid'])+'.html'
                            item_ins['title'] = result['title']
                            item_ins['abstract'] = result['summary']
                            item_ins["date"] = result['human_time_published']
                            result_list["result_list"].append(item_ins)
                            # 把title和abstract写入文件。其他内容可以留作扩展
                            f = open("data/taimeiti/result.txt", 'a')
                            f.write(item_ins['title'])
                            f.write(item_ins['abstract'])
                        except BaseException as e:
                            logging.error("Parse Taimeiti result error. ErrorMsg: %s" % str(e))
                    break
                else:
                    failure += 2
                    logging.warning('search failed: %s' % r.status_code)
            if failure >= 10:
                logging.warning('search failed: %s' % url)
        except BaseException as e:
            logging.error("Get Taimeiti search result error. ErrorMsg: %s" % str(e))
        return result_list


if __name__ == "__main__":
    #url_list = TaiMeiTiSearch.search("上海", search_page=3)    # 已经测试过了,运行正常
    #print(url_list["result_list"])

    url_list = TaiMeiTiSearch.search_page("北京", page=1)  # 已经测试过了,运行正常
    for t in url_list["result_list"]:
        print(t)
