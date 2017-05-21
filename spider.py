#coding=utf-8

import urllib
import requests
import re
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8') # set encoding

def main(html):
    # operate the file
    fout = open("info.txt", "a")

    soup = BeautifulSoup(html)

    # 1. find the links which jump to the detail page
    # contents = soup.select('#8995')[0].contents[0].strings
    contents = soup.select('record')

    links = []
    for content in contents:
        idx = content.contents[0].find('href')
        if idx > 0:
            end = len(content.contents[0])
            # find the link's end
            linkEnd = content.contents[0].find("'", idx + 6, end)
            links.append(content.contents[0][idx + 7 : linkEnd ])

    for j in links:
        # concat the link
        link = "http://cgb.yantai.gov.cn/" + j

        # 2. open the link and get the infos which is needed
        ftemp = urllib.urlopen(link)
        htmltemp = ftemp.read()
        souptemp = BeautifulSoup(htmltemp)

        # init the var
        buyName = 'NULL'             # 项目名称
        publishDate = 'NULL'         # 发布日期
        dealDate = 'NULL'            # 开标日期
        buyWay = 'NULL'              # 采购方式
        companyName = 'NULL'         # 供应商名称
        money = 'NULL'               # 中标金额

        # new
        companyAddress = 'NULL'      # 供应商地址
        buyProxy = 'NULL'            # 采购代理机构

        # locate to td
        taglist = souptemp.select('td[class="title02"]')

        try:
            for tdtag in taglist:

                if tdtag.string == u'中标情况':
                    curtag = tdtag.nextSibling.nextSibling   # 定位到右边的td

                    ptags = curtag.select('p')
                    for ptag in ptags:
                        if ptag.get_text().find(u'项目名称') >= 0:
                            buyName = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                        if ptag.get_text().find(u'发布日期') >= 0:
                            publishDate = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                        if ptag.get_text().find(u'开标日期') >= 0:
                            dealDate = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                        if ptag.get_text().find(u'采购方式') >= 0:
                            buyWay = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                        if ptag.get_text().find(u'代理机构') >= 0:
                            buyProxy = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]

                    # ca!!!
                    indextags = curtag.select('tr')[0].select('td')

                    index = 0
                    while (index < len(indextags)):
                        if indextags[index].get_text().find(u'名称') >= 0:
                            companyName = curtag.select('tr')[1].select('td')[index].get_text()
                        if indextags[index].get_text().find(u'金额') >= 0:
                            money = curtag.select('tr')[1].select('td')[index].get_text()
                        if indextags[index].get_text().find(u'地址') >= 0:
                            companyAddress = curtag.select('tr')[1].select('td')[index].get_text()
                        index = index + 1

        except Exception:
            pass



        # print (u'采购项目名称: %s'%(buyName))
        # print (u'招标公告发布日期: %s'%(publishDate))
        # print (u'开标日期: %s'%(dealDate))
        # print (u'采购方式: %s'%(buyWay))
        # print (u'供应商名称: %s'%(companyName))
        # print (u'中标金额: %s'%(money))
        # print "---"

        # infos =  "\t" + buyName + "\t" + publishDate + "\t" + dealDate + "\t" + buyWay + "\t" + companyName + "\t" + money + "\n"

        # 3. print the infos
        fout.write(u"采购项目名称: " + buyName + "\n")
        fout.write(u"招标公告发布日期: " + publishDate + "\n")
        fout.write(u"开标日期: " + dealDate + "\n")
        fout.write(u"采购方式: " + buyWay + "\n")
        fout.write(u"供应商名称: " + companyName + "\n")
        fout.write(u"代理机构: " + buyProxy + "\n")
        fout.write(u"供应商地址: " + companyAddress + "\n")
        fout.write(u"中标金额: " + money + "\n---------------------------\n")

    fout.close()

if __name__ == '__main__':
    i = 1
    while i < 2901:
        url='http://cgb.yantai.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=' + str(i) + '&endrecord='+ str((i+149) > 2901 and 2901 or (i+149)) + '&perpage=50'
        values={'col':'1', 'appid':'1', 'webid':'89', 'path':'/', 'columnid':'5805', 'sourceContentType':'3', 'unitid':'8995', 'webname':'烟台市政府采购网', 'permissiontype':'0'}

        # print url

        html = requests.post(url, data=values)

        # print return_data.text

        # transport the information
        main(html.text)
        i = i + 150
