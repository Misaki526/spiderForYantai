#coding=utf-8

import urllib
import requests
import re
from bs4 import BeautifulSoup
import sys

#reload(sys)
#sys.setdefaultencoding('utf8') # set encoding

def main():
    # operate the file
    fout = open("info.txt", "w")

    # print the title
    # fout.write("\t 采购项目名称 \t 招标公告发布日期 \t 开标日期 \t 采购方式 \t 供应商名称 \t 中标金额")

    # define the url
    url = "http://cgb.yantai.gov.cn/col/col5805/index.html"

    # 57 pages
    page = 0
    while page <= 57:


        # open the link
        f = urllib.urlopen(url)

        # get the html code
        html = f.read()

        soup = BeautifulSoup(html)

        # 1. find the links which jump to the detail page
        contents = soup.select('#8995')[0].contents[0].string
        start = 0
        end = len(contents)

        links = []
        while 1:
            idx = contents.find('href', start, end)
            if idx > 0:
                # find the link's end
                linkEnd = contents.find("'", idx + 6, end)
                links.append(contents[idx + 7 : linkEnd ])
                start = linkEnd
            else:
                break

        for j in links:
            # concat the link
            link = "http://cgb.yantai.gov.cn/" + j

            # 2. open the link and get the infos which is needed
            ftemp = urllib.urlopen(link)
            htmltemp = ftemp.read()
            souptemp = BeautifulSoup(htmltemp)

            # init the var
            buyName = 'NULL'
            publishDate = 'NULL'
            dealDate = 'NULL'
            buyWay = 'NULL'
            companyName = 'NULL'
            money = 'NULL'

            # 先定位到该 td 下
            taglist = souptemp.select('td[class="title02"]')

            try:
                for tdtag in taglist:

                    if tdtag.string == u'中标情况':
                        curtag = tdtag.nextSibling.nextSibling

                        ptags = curtag.select('p')
                        for ptag in ptags:
                            if ptag.get_text().find(u'一、') >= 0:
                                buyName = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                            if ptag.get_text().find(u'三、') >= 0:
                                publishDate = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                            if ptag.get_text().find(u'四、') >= 0:
                                dealDate = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]
                            if ptag.get_text().find(u'五、') >= 0:
                                buyWay = ptag.get_text()[ptag.get_text().find(u'：')+1 : len(ptag.get_text()) ]

                        companyName = curtag.select('td')[7].get_text()
                        money = curtag.select('td')[9].get_text()

            except Exception:
                pass

            #print (u'采购项目名称: %s'%(buyName))
            #print (u'招标公告发布日期: %s'%(publishDate))
            #print (u'开标日期: %s'%(dealDate))
            #print (u'采购方式: %s'%(buyWay))
            #print (u'供应商名称: %s'%(companyName))
            #print (u'中标金额: %s'%(money))
            #print "---"

            # infos =  "\t" + buyName + "\t" + publishDate + "\t" + dealDate + "\t" + buyWay + "\t" + companyName + "\t" + money + "\n"

            # 3. print the infos
            fout.write(u"采购项目名称: " + buyName + "\n")
            fout.write(u"招标公告发布日期: " + publishDate + "\n")
            fout.write(u"开标日期: " + dealDate + "\n")
            fout.write(u"采购方式: " + buyWay + "\n")
            fout.write(u"供应商名称: " + companyName + "\n")
            fout.write(u"中标金额: " + money + "\n--------\n")

    fout.close()

if __name__ == '__main__':
    #main()
    url='http://cgb.yantai.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=751&endrecord=900&perpage=50'
    values={'col':'1', 'appid':'1', 'webid':'89', 'path':'/', 'columnid':'5805', 'sourceContentType':'3', 'unitid':'8995', 'webname':'烟台市政府采购网', 'permissiontype':'0'}
    
    return_data=requests.post(url, data=values)
    print return_data.text
