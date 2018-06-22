import requests
import os
import time
import sys
from lxml.html import etree
from multiprocessing.dummy import Pool as thread_pool

if getattr(sys, 'frozen', False):
    base = sys._MEIPASS
else:
    base = os.path.dirname(__file__)
print(base)
time.sleep(3)
basePath = os.path.abspath('.') + "/Taxonomic Tree"
if not os.path.exists(basePath):
    os.mkdir(basePath)
time.sleep(3)


def download(url, filename):
    def get_size(filename):
        if not os.path.exists(filename):
            try:
                f = open(filename, 'a+')
                f.close()
            except:
                path = filename.split('\\')
                filename = "/".join(path[:-1]) + '/' + path[-1][-20:]
            return filename, 0
        else:
            return filename, os.path.getsize(filename)

    filename, filesize = get_size(filename)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        'Range': 'bytes=%d-' % filesize
    }
    try:
        web_log = requests.get(url, stream=True, headers=header, timeout=30)
        print(web_log)
        if web_log.status_code == 416:
            print(filename + "下载完成")
            return
        elif web_log.status_code == 404:
            return

        with open(filename, 'ab+') as local_file:
            for chunk in web_log.iter_content(chunk_size=256):
                if chunk:
                    local_file.write(chunk)
                    local_file.flush()

        download(url, filename)

    except Exception as e:
        print(e)
        download(url, filename)


def link_generate():
    tree = etree.HTML(open(base + "/html/index.html", encoding="utf-8").read())
    tp = thread_pool(20)
    for layer1 in tree.xpath('//ul[@class="orders clearfix"]/li'):
        layer1_name = layer1.xpath('./span/a[@class="name"]/text()')[0]
        layer1_path = os.path.join(basePath, layer1_name)
        if not os.path.exists(layer1_path):
            os.mkdir(layer1_path)
        for layer2 in layer1.xpath('.//li'):
            id = layer2.xpath('./@id')[0]
            layer2_name = layer2.xpath('./span/a[@class="name"]/text()')[0]
            layer2_path = os.path.join(layer1_path, layer2_name)
            # print("--" + layer2_name, id)
            if not os.path.exists(layer2_path):
                os.mkdir(layer2_path)
            url = "https://www.hbw.com/bird_taxonomies/ajax/species/" + id[3:] + "/201985"
            try:
                res = requests.post(url)
                tree1 = etree.HTML(res.text)
                for layer3 in tree1.xpath("//li"):
                    href = layer3.xpath("./span/a/@href")[0]
                    layer3_name = href.split("/")[-1]
                    layer3_path = os.path.join(layer2_path, layer3_name)
                    # print("----" + layer3_name)
                    href1 = "https://www.hbw.com" + href

                    if not os.path.exists(layer3_path):
                        os.mkdir(layer3_path)
                        res = requests.get(href1)
                        html_out = open(os.path.join(layer3_path, "base.html"), "wb")
                        html_out.write(res.content)
                        html_out.close()

                    url_detail = "https://www.hbw.com/ibc" + href
                    try:
                        res_detail = requests.get(url_detail)
                        tree3 = etree.HTML(res_detail.content)


                        imgfile = os.path.join(layer3_path, "image")
                        if not os.path.exists(imgfile):
                            os.mkdir(imgfile)

                        videofile = os.path.join(layer3_path, "video")
                        if not os.path.exists(videofile):
                            os.mkdir(videofile)

                        soundfile = os.path.join(layer3_path, "sound")
                        if not os.path.exists(soundfile):
                            os.mkdir(soundfile)

                        for img in tree3.xpath('//a[@class="colorbox"]'):
                            imgurl = img.xpath("./img/@src")[0]
                            tp.apply_async(download,
                                           (imgurl, os.path.join(imgfile, imgurl.split("?")[0].split("/")[-1])))

                        for video in tree3.xpath('//source[@type="video/mp4"]'):
                            videourl = video.xpath("./@src")[0]
                            tp.apply_async(download, (videourl, os.path.join(videofile, videourl.split("/")[-1])))

                        for sound in tree3.xpath('//source[@type="audio/mpeg"]'):
                            soundurl = sound.xpath("./@src")[0]
                            tp.apply_async(download, (soundurl, os.path.join(soundfile, soundurl.split("/")[-1])))
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
    tp.close()
    tp.join()


link_generate()
