#!/usr/bin/env python

"""
@Time     : 2017/7/18 11:34
@Author   : Danxiyang
@File     : test_os.py
@Software : PyCharm
"""
import requests
import json
import pandas as pd
from lxml.html import etree
from multiprocessing import Pool
from multiprocessing.dummy import Pool as thread_pool
import time
from queue import Queue

q = Queue()

def write_file(values):
    with open("chedai_1.csv", 'a+') as f:
        for value in values:
            f.write(",".join(value))
            f.write('\n')

def down_1(*args):
    global q
    model_id, brand_text_1, brand_text_2, serial_text_1, serial_text_2, s, p= args
    detail_url = "http://jr.pcauto.com.cn/choose/r297/m" + str(model_id) + "-c0-s" + str(s) + "-p" + str(p) + '/'
    res = requests.get(detail_url)
    if res.status_code == 404:
        return
    else:
        tree = etree.HTML(res.content)
        price1 = tree.xpath('//div[@class="centersj"]/em/text()')[0]
        price2 = tree.xpath('//div[@class="rightsj"]/em/text()')[0]
        price3 = tree.xpath('//div[@class="leftsj"]/em/text()')[0]
        for div in tree.xpath('//div[@class="tblist clearfix"]'):
            yhps = div.xpath('.//div[@class="yhtps"]/span/text()')[0]
            for em in div.xpath('./div[@class="yhlistri"]/em'):
                list00 = em.xpath('./div[@class="listt01 listt00"]/text()')[0]
                list01 = em.xpath('./div[@class="listt01 listt02"]/p/i/text()')[0]
                list02 = em.xpath('./div[@class="listt01 listt02"]/p/text()')[2][4:]
                list03 = "|".join(em.xpath('./div[@class="listt01 listt03"]/p/text()'))
                list04 = "|".join(em.xpath('./div[@class="listt01 listt04"]/p/i/text()'))
                q.put((
                    brand_text_1, brand_text_2, serial_text_1, serial_text_2, price1, price2, price3, yhps, str(s),
                    str(p),
                    list00, str(list01), list02, list03, list04))


def down(*args):
    result = []
    global q
    tp = thread_pool(20)
    brand_id, brand_text_1 = args
    serial_url = "http://price.pcauto.com.cn/api/hcs/select/serial_json_chooser?bid=" + str(
        brand_id) + "&status=1&type=2&callback=chexi"
    serial = requests.get(serial_url)
    serial_json = json.loads(serial.text[6:-1])
    brand_text_2 = ''
    for serial_infos in serial_json["firms"]:
        if len(serial_infos) == 6:
            brand_text_2 = serial_infos["name"]
        else:
            serial_id = serial_infos["id"]
            serial_text_1 = serial_infos["name"]
            model_url = "http://price.pcauto.com.cn/api/hcs/select/model_json_chooser?sgid=" + str(
                serial_id) + "&status=1&type=2"
            model = requests.get(model_url)
            model_json = json.loads(model.text[9:-1])
            model_info = pd.DataFrame(model_json["cars"])
            model_info = model_info.loc[model_info["caption"].isnull(), ["id", "title"]]
            for model_id, serial_text_2 in model_info.values:
                print(serial_text_2, time.asctime(time.localtime()))
                for s in [20, 30, 40, 50, 60]:
                    for p in [12, 18, 24, 36]:
                        tp.apply_async(down_1, (model_id, brand_text_1, brand_text_2, serial_text_1, serial_text_2, s, p))
    tp.close()
    tp.join()
    while not q.empty():
        result.append(q.get())
    print(result)
    return result


if __name__ == "__main__":
    pool = Pool(4)
    brand = pd.read_csv("brand.csv", encoding='gbk')
    for brand_id, brand_text_1 in brand.values:
        pool.apply_async(down,
                         (brand_id, brand_text_1),
                         )
    pool.close()
    pool.join()