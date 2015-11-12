# encoding: utf-8

import sys
import libxml2
import url_utils
import logging

reload(sys)
sys.setdefaultencoding('utf8')

PARSE_OPTIONS = libxml2.HTML_PARSE_RECOVER + libxml2.HTML_PARSE_NOERROR + libxml2.HTML_PARSE_NOWARNING

def __makeUrl__(url_part):
    if 'http:' not in url_part:
        url_part = 'http:' + url_part
        return url_part

def resolveTotalPageNum(html):
    doc = libxml2.htmlReadDoc(html,None,'utf8',PARSE_OPTIONS)
    try:
        pgtxt = doc.xpathEval('//span[@class="fp-text"]/i')[0].content
        page_num = int(pgtxt)
        return page_num
    finally:
        doc.freeDoc()

def resolveProductListFromPage(html):
    product_list = []
    try:
        doc = libxml2.htmlReadDoc(html,None,'utf8',PARSE_OPTIONS)
        sku_docs = doc.xpathEval('//div[@data-sku]')
        for sku in sku_docs:
            #if True:
            try:
                sku_doc = libxml2.htmlReadDoc('%s'%sku,None,'utf8',PARSE_OPTIONS)

                sku_id = int(sku_doc.xpathEval('//@data-sku')[0].content)
                # 判断是否是JD自营
                if sku_id > 99999999:
                    # 非自营商品
                    continue

                #print '%s' %sku

                sku_url = sku_doc.xpathEval('//div[@class="p-img"]/a/@href')[0].content
                try:
                    sku_thumnail_url = sku_doc.xpathEval('//div[@class="p-img"]/a/img/@data-lazy-img')[0].content
                except:
                    sku_thumnail_url = sku_doc.xpathEval('//div[@class="p-img"]/a/img/@src')[0].content

                sku_title = ""
                try:
                	sku_title = sku_doc.xpathEval('//div[@class="p-name"]/a/@title')[0].content
                except:
                    pass

                if len(sku_title)==0:
					sku_title = sku_doc.xpathEval('//div[@class="p-name"]/a/em')[0].content
                comment_count = int(sku_doc.xpathEval('//div[@class="p-commit"]/strong/a')[0].content)

                sku_icon_url = ""
                icon_doc = sku_doc.xpathEval('//div[@class="p-img"]/a/div/@style')
                if len(icon_doc)>0:
                    sku_icon_url = url_utils.getStringBetween(icon_doc[0].content,'url("','")')

                is_global = is_free_gift = is_pay_on_delivery = 0
                price_items = sku_doc.xpathEval('//div[@class="p-price"]/div/i')
                for pitem in price_items:
                    txt = pitem.content
                    if '全球购' in txt:
                        is_global = 1
                    elif '货到付款' in txt:
                        is_pay_on_delivery = 1
                    elif '赠品' in txt:
                        is_free_gift = 1
                    else:
                        print 'new-mark found:'
                        print txt

                sku_stock = -1
                try:
                    sku_stock = int(sku_doc.xpathEval('//div[@data-stock_v]/@data-stock_v')[0].content)
                except:
                    pass

                sku_url = __makeUrl__(sku_url)
                sku_thumnail_url = __makeUrl__(sku_thumnail_url)

                tp = (sku_id,sku_title,sku_url,sku_thumnail_url,sku_stock,comment_count,is_global,is_pay_on_delivery,is_free_gift,sku_icon_url)
                product_list.append(tp)

            except Exception as e:
                logging.error('resolveProductListError: %s, error = %s') %(sku,e)
                continue
            finally:
                sku_doc.freeDoc()

        return product_list
    finally:
        doc.freeDoc()


if __name__ == "__main__":

    html = ""
    print resolveTotalPageNum(html)
    print resolveProductListFromPage(html)