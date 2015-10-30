# encoding: utf-8
import sys
import libxml2
import logging
import re
import url_utils

PARSE_OPTIONS = libxml2.HTML_PARSE_RECOVER + libxml2.HTML_PARSE_NOERROR + libxml2.HTML_PARSE_NOWARNING

def resolve_Properties(html):
    property_map = {}
    doc = libxml2.htmlReadDoc(html,None,'utf8',PARSE_OPTIONS)
    tr_docs = doc.xpathEval('//div[@id="product-detail-2"]/table/tr')
    for tr in tr_docs:
        td_doc = libxml2.htmlReadDoc('%s'%tr,None,'utf-8',PARSE_OPTIONS)
        td_docs = td_doc.xpathEval('//td')
        if len(td_docs)<2:
            continue
        pkey = td_docs[0].content
        pvalue = td_docs[1].content
        property_map[pkey] = pvalue
        td_doc.freeDoc()
    if len(property_map)==0:
        div_docs = doc.xpathEval('//div[@id="product-detail-2"]/div')
        try:
            text = '%s' %div_docs[0]
            text = url_utils.removeHTMLTags(text,' ')
            text = text.replace('\n',' ')
            text = text.replace('\r',' ')
            key_value_pair_texts = text.split(' ')
            for kv_pair in key_value_pair_texts:
                if len(kv_pair)==0:
                    continue
                kv_list = kv_pair.split('：')
                if len(kv_list)<2:
                    kv_list = kv_pair.split(':')
                if len(kv_list)>=2:
                    if len(kv_list[1].strip())>0:
                        property_map[kv_list[0]] = kv_list[1]

            if len(property_map)==0:
                property_map['__DEFAULT__'] = text

        except Exception as e:
            logging.warning('cannot resolve properties anyway, div html = %s' %div_docs)
    doc.freeDoc()
    return property_map

def resolve_Images(html):
    doc = libxml2.htmlReadDoc(html,None,'utf8',PARSE_OPTIONS)
    #img_doms = doc.xpathEval('//div[@class="spec-items"]/ul/li/img/@src')
    img_doms = doc.xpathEval('//div[@class="spec-items"]/ul/li/img/@data-url')
    img_list = []
    for dom in img_doms:
        img_list.append(dom.content)
    doc.freeDoc()
    return img_list


if __name__ == "__main__":
    html = """


<!DOCTYPE HTML>
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=gbk" />
    <title>【艾美特FSW52R】艾美特(Airmate) FSW52R 遥控落地扇/电风扇【行情 报价 价格 评测】-京东</title>
    <meta name="keywords" content="AirmateFSW52R,艾美特FSW52R,艾美特FSW52R报价,AirmateFSW52R报价"/>
    <meta name="description" content="【艾美特FSW52R】京东JD.COM提供艾美特FSW52R正品行货，全国价格最低，并包括AirmateFSW52R网购指南，以及艾美特FSW52R图片、FSW52R参数、FSW52R评论、FSW52R心得、FSW52R技巧等信息，网购艾美特FSW52R上京东,放心又轻松" />
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="mobile-agent" content="format=xhtml; url=//item.m.jd.com/product/595936.html">
    <meta http-equiv="mobile-agent" content="format=html5; url=//item.m.jd.com/product/595936.html">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <link rel="canonical" href="//item.jd.com/595936.html"/>
        <link rel="dns-prefetch" href="//misc.360buyimg.com"/>
    <link rel="dns-prefetch" href="//static.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img10.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img11.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img13.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img12.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img14.360buyimg.com"/>
    <link rel="dns-prefetch" href="//img30.360buyimg.com"/>
    <link rel="dns-prefetch" href="//pi.3.cn"/>
    <link rel="dns-prefetch" href="//ad.3.cn"/>
    <link rel="dns-prefetch" href="//st.3.cn"/>
    <link rel="dns-prefetch" href="//d.3.cn"/>
    <link rel="dns-prefetch" href="//c.3.cn"/>
    <link rel="dns-prefetch" href="//d.jd.com"/>
    <link rel="dns-prefetch" href="//x.jd.com"/>
    <link rel="dns-prefetch" href="//wl.jd.com"/>
                <link type="text/css" rel="stylesheet"  href="//misc.360buyimg.com/jdf/1.0.0/unit/??ui-base/1.0.0/ui-base.css,shortcut/2.0.0/shortcut.css,global-header/1.0.0/global-header.css,myjd/2.0.0/myjd.css,nav/2.0.0/nav.css,shoppingcart/2.0.0/shoppingcart.css,global-footer/1.0.0/global-footer.css,service/1.0.0/service.css"/>
                        <link rel="stylesheet" type="text/css" href="//static.360buyimg.com/item/main/1.0.8/??/widget/common/common.css,/widget/sprite/sprite.css,/widget/main/main.css,/widget/contrast/contrast.css,/widget/combineShare/combineShare.css,/widget/itemInfo/itemInfo.css,/widget/extInfo/extInfo.css,/widget/promiseIcon/promiseIcon.css,/widget/popScore/popScore.css,/widget/preview/preview.css,/widget/fitting/fitting.css,/widget/ui-box/ui-box.css,/widget/ui-star/ui-star.css,/widget/ui-tag/ui-tag.css,/widget/detailContent/detailContent.css,/widget/comment/comment.css,/widget/commentsList/commentsList.css,/widget/ui-page/ui-page.css,/widget/consult/consult.css,/widget/discuss/discuss.css,/widget/yourFind/yourFind.css" source="widget"/>
        <script>
       var pageConfig = {
            compatible: true,
                        product: {
                skuid: 595936,
                name: '\u827e\u7f8e\u7279\u0028\u0041\u0069\u0072\u006d\u0061\u0074\u0065\u0029\u0020\u0046\u0053\u0057\u0035\u0032\u0052\u0020\u9065\u63a7\u843d\u5730\u6247\u002f\u7535\u98ce\u6247',
                skuidkey:'E12D8AB316C48A3F40199AF1B3A07419',
                href: '//item.jd.com/595936.html',
                src: 'jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg',
                cat: [737,738,751],
                brand: 3085,
                pType: 1,
                isClosePCShow: false,
                venderId:1000001414,
                shopId:'1000001414',
                                commentVersion:'7470',                 specialAttrs:["isFlashPurchase-0","isBigClient","isCanVAT","isHaveYB","isCanUseJQ","IsNewGoods","isSelfService-0","isWeChatStock-0","PianYuanYunFei","HYKHSP-0","is7ToReturn-1","isNSNGgoods-0","YYSLLZC-0"],
                recommend : [0,1,2,3,4,5,6,7,8,9],
                stocks : [0,1,2,3,4,5,6,7,8,9],
                easyBuyUrl:"http://easybuy.jd.com/skuDetail/newSubmitEasybuyOrder.action",
                                colorSize: [{"SkuId":183566,"Color":"【暖风机爆款-即开即热2万好评】"},{"SkuId":595936,"Color":"【遥控风扇爆款-超19万好评】"}],                warestatus: 1,                                 tips: [{"order":3,"tip":"支持7天无理由退货"}],                                desc: '//d.3.cn/desc/595936',                foot: '//d.3.cn/footer?type=common_config2'
            }
        };
                        try {
                        function is_sort_black_list() {
              var jump_sort_list = {"6881":3,"1195":3,"10011":3,"6980":3,"12360":3};
              if(jump_sort_list['737'] == 1 || jump_sort_list['738']==2 || jump_sort_list['751']==3) {
                return true;
              }
              return false;
            }

            function jump_mobile() {
              if(is_sort_black_list()) {
                return;
              }

              var userAgent = navigator.userAgent || "";
              userAgent = userAgent.toUpperCase();
                            if(userAgent == "" || userAgent.indexOf("PAD") > -1) {
                  return;
              }

                            if(window.location.hash == '#m') {
                var exp = new Date();
                exp.setTime(exp.getTime() + 30 * 24 * 60 * 60 * 1000);
                document.cookie = "pcm=1;expires=" + exp.toGMTString() + ";path=/;domain=jd.com";
                                window.showtouchurl = true;
                return;
              }

                            if (/MOBILE/.test(userAgent) && /(MICROMESSENGER|QQ\/)/.test(userAgent)) {
                  window.location.href = "//item.m.jd.com/product/595936.html";
                  return;
              }

                            var jump = true;
              var cook = document.cookie.match(/(^| )pcm=([^;]*)(;|$)/);
              if(cook && cook.length > 2 && unescape(cook[2]) == "1") {
                jump = false;
              }
              var mobilePhoneList = ["IOS","IPHONE","ANDROID","WINDOWS PHONE"];
              for(var i=0, len=mobilePhoneList.length; i<len; i++) {
                if(userAgent.indexOf(mobilePhoneList[i]) > -1) {
                  if(jump) {
                    window.location.href = "//item.m.jd.com/product/595936.html";
                  } else {
                                        window.showtouchurl = true;
                  }
                  break;
                }
              }
            }
            jump_mobile();
        } catch(e) {}    </script>
    <script src="//misc.360buyimg.com/??jdf/lib/jquery-1.6.4.js,jdf/1.0.0/unit/base/1.0.0/base.js"></script>

</head>
<body version="140120" class="cat-1-737 cat-2-738 cat-3-751 item-595936 JD JD-1">
        <div id="shortcut-2014">
    <div class="w">
        <ul class="fl" clstag="shangpin|keycount|topitemnormal|a01">
            <li class="dorpdown" id="ttbar-mycity"></li>
        </ul>
        <ul class="fr">
            <li class="fore1" id="ttbar-login" clstag="shangpin|keycount|topitemnormal|a02">
                <a target="_blank" href="javascript:login();" class="link-login">你好，请登录</a>
                &nbsp;&nbsp;
                <a href="javascript:regist();" class="link-regist style-red">免费注册</a>
            </li>
            <li class="spacer"></li>
            <li class="fore2"  clstag="shangpin|keycount|topitemnormal|a03">
                <div class="dt">
                    <a target="_blank" href="http://order.jd.com/center/list.action">我的订单</a>
                </div>
            </li>
            <li class="spacer"></li>
            <li class="fore3 dorpdown" id="ttbar-myjd" clstag="shangpin|keycount|topitemnormal|b04">
                <div class="dt cw-icon">
                    <i class="ci-right"><s>◇</s></i>
                    <a target="_blank" href="http://home.jd.com/">我的京东</a>
                </div>
                <div class="dd dorpdown-layer"></div>
            </li>
            <li class="spacer"></li>
            <li class="fore4" clstag="shangpin|keycount|topitemnormal|a04">
                <div class="dt">
                    <a target="_blank" href="http://vip.jd.com/">京东会员</a>
                </div>
            </li>
            <li class="spacer"></li>
            <li class="fore5"  clstag="shangpin|keycount|topitemnormal|a05">
                <div class="dt">
                    <a target="_blank" href="http://b.jd.com/">企业采购</a>
                </div>
            </li>
            <li class="spacer"></li>
            <li class="fore6 dorpdown" id="ttbar-apps" clstag="shangpin|keycount|topitemnormal|a06">
                <div class="dt cw-icon">
                    <i class="ci-left"></i>
                    <i class="ci-right"><s>◇</s></i>
                    <a target="_blank" href="http://app.jd.com/">手机京东</a>
                </div>
            </li>
            <li class="spacer"></li>
            <li class="fore7 dorpdown" id="ttbar-atte" clstag="shangpin|keycount|topitemnormal|a09">
                <div class="dt cw-icon">
                    <i class="ci-right"><s>◇</s></i>关注京东
                </div>
            </li>
            <li class="spacer"></li>
            <li class="fore8 dorpdown" id="ttbar-serv" clstag="shangpin|keycount|topitemnormal|a07">
                <div class="dt cw-icon">
                    <i class="ci-right"><s>◇</s></i>客户服务
                </div>
                <div class="dd dorpdown-layer"></div>
            </li>
            <li class="spacer"></li>
            <li class="fore9 dorpdown" id="ttbar-navs" clstag="shangpin|keycount|topitemnormal|a08">
                <div class="dt cw-icon">
                    <i class="ci-right"><s>◇</s></i>网站导航
                </div>
                <div class="dd dorpdown-layer"></div>
            </li>
        </ul>
        <span class="clr"></span>
    </div>
</div><!-- #shortcut-2014 -->        <div class="w">
    <div id="logo-2014">
        <a href="//www.jd.com/" clstag="shangpin|keycount|topitemnormal|b01" class="logo">京东</a>
    </div>
    <div id="search-2014">
        <ul id="shelper" class="hide"></ul>
        <div class="form">
            <input type="text" onkeydown="javascript:if(event.keyCode==13) search('key');" autocomplete="off" id="key" accesskey="s" class="text" clstag="shangpin|keycount|topitemnormal|b02" />
            <button onclick="search('key');return false;" class="button cw-icon" clstag="shangpin|keycount|topitemnormal|b03"><i></i>搜索</button>
        </div>
    </div>
    <div id="settleup-2014" class="dorpdown">
        <div class="cw-icon">
            <i class="ci-left"></i>
            <i class="ci-right">&gt;</i>
            <a target="_blank" clstag="shangpin|keycount|topitemnormal|b05" href="//cart.jd.com/cart/cart.html">我的购物车</a>
        </div>
        <div class="dorpdown-layer">
            <div class="spacer"></div>
            <div id="settleup-content">
                <span class="loading"></span>
            </div>
        </div>
    </div>
    <div id="hotwords"></div>
    <span class="clr"></span>
</div>

<div id="nav-2014">
    <div class="w">
        <div class="w-spacer"></div>
        <div id="categorys-2014" class="dorpdown" data-type="default">
            <div class="dt" clstag="shangpin|keycount|topitemnormal|c01">
                <a target="_blank" href="//www.jd.com/allSort.aspx">全部商品分类</a>
            </div>
        </div>
        <div id="navitems-2014">
            <ul id="navitems-group1">
                <li class="fore1" clstag="shangpin|keycount|topitemnormal|c03" id="nav-home">
                    <a href="//www.jd.com/">首页</a>
                </li>
                <li class="fore2" clstag="shangpin|keycount|topitemnormal|c04" id="nav-fashion">
                    <a target="_blank" href="//channel.jd.com/fashion.html">服装城</a>
                </li>
                <li class="fore3" clstag="shangpin|keycount|topitemnormal|c05" id="nav-beauty">
                    <a target="_blank" href="//channel.jd.com/beautysale.html">美妆馆</a>
                </li>
                <li class="fore4" clstag="shangpin|keycount|topitemnormal|c06" id="nav-chaoshi">
                    <a target="_blank" href="//channel.jd.com/chaoshi.html">超市</a>
                </li>
                <li class="fore5" clstag="shangpin|keycount|topitemnormal|c07" id="nav-jdww">
                    <a target="_blank" href="//www.jd.hk/">全球购</a>
                </li>
            </ul>
            <div class="spacer"></div>
            <ul id="navitems-group2">
                <li class="fore1" clstag="shangpin|keycount|topitemnormal|c08" id="nav-red">
                    <a target="_blank" href="//red.jd.com/">闪购</a>
                </li>
                <li class="fore2" clstag="shangpin|keycount|topitemnormal|c09" id="nav-tuan">
                    <a target="_blank" href="//tuan.jd.com/">团购</a>
                </li>
                <li class="fore3" clstag="shangpin|keycount|topitemnormal|c10" id="nav-auction">
                    <a target="_blank" href="//paimai.jd.com/">拍卖</a>
                </li>
                <li class="fore4" clstag="shangpin|keycount|topitemnormal|c11" id="nav-jr">
                    <a target="_blank" href="//jr.jd.com/">金融</a>
                </li>
                <li class="fore5" clstag="shangpin|keycount|topitemnormal|c12" id="nav-smart">
                    <a target="_blank" href="//smart.jd.com/">智能</a>
                </li>
            </ul>
        </div>
        <div id="treasure"></div>
        <span class="clr"></span>
    </div>
</div><!-- #nav-2014 -->
<script>
    setTimeout(function () {
        seajs.use('//misc.360buyimg.com/jdf/1.0.0/unit/globalInit/2.0.0/globalInit', function(globalInit){
            globalInit();
        });
    }, 500);
</script><div id="root-nav">
    <div class="w">
        <div class="breadcrumb">
          <strong><a href='//channel.jd.com/electronic.html' clstag="shangpin|keycount|product|mbNav-1">家用电器</a></strong><span>&nbsp;&gt;&nbsp;<a href='//channel.jd.com/737-738.html' clstag="shangpin|keycount|product|mbNav-2">生活电器</a>&nbsp;&gt;&nbsp;<a href='//list.jd.com/list.html?cat=737,738,751' clstag="shangpin|keycount|product|mbNav-3">电风扇</a>&nbsp;&gt;&nbsp;</span>
<span><a href='//www.jd.com/pinpai/751-3085.html' clstag="shangpin|keycount|product|mbNav-4">艾美特（AIRMATE）</a>&nbsp;&gt;&nbsp;<a href='//item.jd.com/595936.html'>艾美特FSW52R</a></span>
        </div>
    </div>
</div>

<div id="p-box">
        <div class="w">
        <div id="seo-banner" class="m m2 hide"></div>
    </div>
        <div class="w">
        <div id="search-result" class="m m2 hide" clstag="shangpin|keycount|product|exrs"></div>
    </div>

    <div class="w">
        <div id="product-intro" class="m-item-grid clearfix">
                        <div id="preview" clstag="shangpin|keycount|product|mainpicarea_1">
                <div id="spec-n1" class="jqzoom" onclick="window.open('//item.jd.com/bigimage.aspx?id=595936')" clstag="shangpin|keycount|product|mainpic_1">
                    <img data-img="1" width="350" height="350" src="//img11.360buyimg.com/n1/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg" alt="艾美特(Airmate) FSW52R 遥控落地扇/电风扇"/>
                                                        </div>
                                                <div id="spec-list" clstag="shangpin|keycount|product|lunbotu_1">
                    <a href="javascript:;" class="spec-control" id="spec-forward"></a>
                    <a href="javascript:;" class="spec-control" id="spec-backward"></a>
                    <div class="spec-items">
                        <ul class="lh">
                                                                                <li><img class='img-hover' alt='艾美特(Airmate) FSW52R 遥控落地扇/电风扇' src='//img11.360buyimg.com/n5/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg' data-url='jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg' data-img='1' width='50' height='50'></li>
                                                        <li><img alt='艾美特(Airmate) FSW52R 遥控落地扇/电风扇' src='//img11.360buyimg.com/n5/jfs/t1147/296/602899023/67877/8392728/5535bc57N33807845.jpg' data-url='jfs/t1147/296/602899023/67877/8392728/5535bc57N33807845.jpg' data-img='1' width='50' height='50'></li>
                                                        <li><img alt='艾美特(Airmate) FSW52R 遥控落地扇/电风扇' src='//img11.360buyimg.com/n5/jfs/t1144/296/636028641/39220/d1019630/5535bc57N4754ce32.jpg' data-url='jfs/t1144/296/636028641/39220/d1019630/5535bc57N4754ce32.jpg' data-img='1' width='50' height='50'></li>
                                                        <li><img alt='艾美特(Airmate) FSW52R 遥控落地扇/电风扇' src='//img11.360buyimg.com/n5/jfs/t1141/76/633114315/65255/273d010d/5535bc58N96bdccde.jpg' data-url='jfs/t1141/76/633114315/65255/273d010d/5535bc58N96bdccde.jpg' data-img='1' width='50' height='50'></li>
                                                        <li><img alt='艾美特(Airmate) FSW52R 遥控落地扇/电风扇' src='//img11.360buyimg.com/n5/jfs/t1138/271/605768937/70206/735a5d96/5535bc58Nd2528ec3.jpg' data-url='jfs/t1138/271/605768937/70206/735a5d96/5535bc58Nd2528ec3.jpg' data-img='1' width='50' height='50'></li>
                                                  </ul>
                                            </div>
                </div>
                                                <div id="short-share">
                    <div class="fl"><span>商品编号：</span><span>595936</span></div>
                    <a id="choose-btn-coll" class="choose-btn-coll" href="#none" data-id="595936" clstag="shangpin|keycount|product|guanzhushangpin_1"><b></b><em id="">关注商品</em></a>
                    <a id="share-list" class="share-list" href="#none" clstag="shangpin|keycount|product|share_1">
                      <b></b><em>分享</em>
                    </a>
                </div>
            </div>

            <div class="m-item-inner" clstag="shangpin|keycount|product|zhushujuqu_1">
              <div id="itemInfo">
                                    <div id="name">
                      <h1>艾美特(Airmate) FSW52R 遥控落地扇/电风扇</h1>
                      <div id="p-ad" class="p-ad J-ad-595936"></div>
                      <div id="p-ad-phone" class="p-ad"></div>
                                                              </div>
                                                                              <div id="compare">
                      <a href="#none" id="comp_595936" data-sku="595936" class="J_contrast btn-compare" clstag="shangpin|keycount|product|jiaruduibi"><span>对比</span></a>
                    </div>
                                                                                                    <div id="summary">
                        <div id="comment-count" clstag="shangpin|keycount|product|pingjiabtn_1">
                            <p class="comment">累计评价</p>
                            <a class="count J-comm-595936" href="#comment">0</a>
                        </div>
                        <div id="summary-price">
                            <div class="dt">京 东 价：</div>
                            <div class="dd">
                                <strong class="p-price" id="jd-price"></strong>
                                                                                                <a data-type="1" data-sku="595936" id="notice-downp" class="J-notify-1" href="#none" clstag="shangpin|keycount|product|jiangjia_1">(降价通知)</a>
                            </div>
                        </div>
                                                <div id="J-summary-top" class="summary-top" clstag="shangpin|keycount|product|cuxiao_1">
                            <div id="summary-promotion" class="hide">
                                <div class="dt">促销信息：</div>
                                <div class="dd J-prom-wrap p-promotions-wrap">
                                    <div class="p-promotions">
                                        <ins id="prom-mbuy"></ins>
                                        <ins id="prom-gift" clstag="shangpin|keycount|product|zengpin_1"></ins>
                                        <ins id="prom"></ins>
                                        <ins id="prom-one"></ins>
                                        <ins id="prom-phone"></ins>
                                        <ins id="prom-phone-jjg"></ins>
                                        <ins id="prom-tips"></ins>
                                        <ins id="prom-quan"></ins>
                                        <div class="J-prom-more view-all-promotions">
                                            <span class="prom-sum">共<em class="prom-number J-prom-count"></em>项促销</span>
                                            <a href="#none" class="view-link"><i class="i-arrow"></i></a>
                                        </div>
                                    </div>
                                </div>
                            </div>                        </div>                                                                                                                        <div id="summary-support" class="li hide">
                            <div class="dt">支&#x3000;&#x3000;持：</div>
                            <div class="dd">
                                <ul class="choose-support lh"></ul>
                            </div>
                        </div>
                                                <div id="summary-stock" clstag="shangpin|keycount|product|quyuxuanze_1" >
                            <div class="dt">配 送 至：</div>
                            <div class="dd clearfix">
                                <div id="store-selector">
                                    <div class="text"><div></div><b></b></div>
                                    <div class="content">
                                        <span class="clr"></span>
                                    </div>
                                    <div class="close" onclick="$('#store-selector').removeClass('hover')"></div>
                                </div>                                 <div id="store-prompt"></div>                            </div>
                            <span class="clr"></span>
                        </div>
                        <div id="summary-service" clstag="shangpin|keycount|product|fuwu_1">
                            <div class="dt">服&#x3000;&#x3000;务：</div>
                            <div class="dd"></div>
                        </div>
                    </div>
                                        <div id="choose" class="clearfix p-choose-wrap" clstag="shangpin|keycount|product|choose">
                                                    <div id="choose-color" class="li choose-color-shouji p-choose">
                                <div class="dt">选择颜色：</div>
                                <div class="dd">
                                                                <div class="item"><b></b><a href="//item.jd.com/183566.html" title="【暖风机爆款-即开即热2万好评】"><img data-img="1" src="//img11.360buyimg.com/n9/jfs/t271/49/434037056/86234/3c98baf8/541154c4N19835fa6.jpg" width="25" height="25" alt="【暖风机爆款-即开即热2万好评】"><i>【暖风机爆款-即开即热2万好评】</i></a></div>
                                                                <div class="item"><b></b><a href="//item.jd.com/595936.html" title="【遥控风扇爆款-超19万好评】"><img data-img="1" src="//img11.360buyimg.com/n9/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg" width="25" height="25" alt="【遥控风扇爆款-超19万好评】"><i>【遥控风扇爆款-超19万好评】</i></a></div>
                                                                </div>
                            </div>
                                                                                                                                                    <div id="choose-type" class="li p-choose hide"></div>
                            <div id="choose-type-hy" class="li p-choose hide"></div>
                            <div id="choose-type-suit" class="li p-choose hide">
                                <div class="dt">合约套餐：</div>
                                <div class="dd">
                                    <div class="item J-suit-trigger" clstag="shangpin|keycount|product|taocanleixing">
                                        <b></b>
                                        <a href="#none" title="选择套餐与资费">选择套餐与资费</a>
                                    </div>
                                    <div class="fl" style="padding-top:5px;">
                                        <span class="J-suit-tips hide">请选择套餐内容</span>
                                        <span class="J-suit-resel J-suit-trigger hl_blue hide" href="#none">重选</span>
                                    </div>
                                </div>
                            </div>
                            <div id="btype-tip" class="hide">&#x3000;您选择的地区暂不支持合约机销售！</div>
                                                                                                                                                <div id="choose-service" class="li hide"><div class="dt"></div><div class="dd"></div></div>
                                                                        <div id="choose-additional" class="li choose-additional hide"></div>
                                                                        <div id="choose-result"></div>

                        <div id="choose-baitiao" class="li p-choose choose-baitiao hide"></div>

                                                <div id="choose-btns" class="li">
                                                        <div class="choose-amount fl " clstag="shangpin|keycount|product|goumaishuliang_1">
                                <div class="wrap-input">
                                    <a class="btn-reduce" href="javascript:;" onclick="setAmount.reduce('#buy-num')">-</a>
                                    <a class="btn-add" href="javascript:;" onclick="setAmount.add('#buy-num')">+</a>
                                    <input class="text" id="buy-num" value="1" onkeyup="setAmount.modify('#buy-num');">
                                </div>
                            </div>
                                                        <a class="btn-special1 btn-lg btn-disable" style="display:none;" id="choose-btn-qiang" href="#none">抢购</a>
                                                        <div class="btn hide" id="choose-btn-gift">
                                <a href="//cart.gift.jd.com/cart/addGiftToCart.action?pid=595936&pcount=1&ptype=1" class="btn-gift"><b></b>选作礼物购买</a>
                            </div>
                                                        <a href="#none" id="choose-btn-hy" class="btn-special1 btn-lg hide" style="display:none;">选择号码和套餐</a>
                                                        <div class="btn" id="choose-btn-append" clstag="shangpin|keycount|product|initcarturl_1">
                                <a class="btn-append " id="InitCartUrl" href="//cart.jd.com/gate.action?pid=595936&pcount=1&ptype=1">加入购物车<b></b></a>
                            </div>
                                                                                                                                            <div class="btn hide" id="choose-btn-easybuy" clstag="shangpin|keycount|product|easybuy_1"></div>
                                                                                    <a id="choose-btn-dbt" href="#none" class="btn-special2 btn-lg" style="display:none;" clstag="shangpin|keycount|product|dabaitiaobutton_737_738_751">打白条</a>
                                                        <div class="btn hide" id="choose-btn-notice" clstag="shangpin|keycount|product|daohuo_1">
                                <a id="notify-btn" class="btn-notice J-notify-2" data-type="2" data-sku="595936" href="#none">到货通知<b></b></a>
                            </div>
                                                                                </div>
                        <div class="clr"></div>
                        <div id="summary-tips" class="li hide" clstag="shangpin|keycount|product|wenxintishi_1">
                            <div class="dt">温馨提示：</div>
                            <div class="dd">
                                <ol class="tips-list clearfix"></ol>
                            </div>
                        </div>
                    </div>                                </div>
            </div>
                                    <div class="m-item-ext J-ext-trigger">
                <div class="extra-infor-show-trigger">
    <i class="i-arrow"></i> <span class="text">更多商品信息</span>
</div>

<div class="extInfo" id="extInfo">
                        <div class="brand-logo" clstag="shangpin|keycount|product|dianpulogo">
            <a href='http://mall.jd.com/index-1000001414.html' target='_blank'>
                <img src='//img30.360buyimg.com/popshop/jfs/t892/225/937783577/11177/c2d04135/55596567N878e5b1b.jpg' title='艾美特生活电器旗舰店'/>
            </a>
        </div>
                <div class="seller-infor">
                    <a class="name" href="http://mall.jd.com/index-1000001414.html" target="_blank" title="艾美特生活电器旗舰店">艾美特生活电器旗舰店</a>
                <em class="u-jd">京东自营</em>
    </div>



<dl class="customer-service clearfix">
  <dt class="label">在线客服：</dt>
  <dd class="service">
    <span id="J-im-btn" clstag="shangpin|keycount|product|dongdong_1"></span>
    <span id="J-jimi-btn" clstag="shangpin|keycount|product|jimi_1"></span>
  </dd>
</dl>

    <div class="pop-shop-enter">
        <a href="http://mall.jd.com/index-1000001414.html" target="_blank" class="btn-gray btn-shop-access J-enter-shop" clstag="shangpin|keycount|product|jinrudianpu">进入店铺</a>
        <a href="#none" class="btn-gray btn-shop-follower J-follow-shop" data-vid="1000001414" clstag="shangpin|keycount|product|guanzhu">关注店铺</a>
    </div>

<dl class="jd-service"><dt id="suport-icons">服务支持：</dt></dl>
</div>            </div>
                    </div>
    </div>
</div>

<div class="w">
            <div id="out-of-stock" class="m m2 hide out-of-stock"></div>
    <div class="m m1 hide" id="fitting-suit">
        <div class="float-nav-wrap">
            <div class="mt">
                <ul class="tab">
                    <li class="hide ui-switchable-item curr ui-switchable-selected">
                        <a href="#none">推荐配件</a>
                    </li>
                    <li class="hide ui-switchable-item">
                        <a href="#none">优惠套装</a>
                    </li>
                    <li class="hide ui-switchable-item">
                        <a href="#none">最佳组合</a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="mc" >
            <div class="ui-switchable-panel hide">
                <div id="fitting-con" class="fitting-content" clstag="shangpin|keycount|product|tuijianpeijian_1"><div class="loading-style1"><b></b>加载中，请稍候...</div></div>
            </div>
            <div class="ui-switchable-panel hide">
                <div id="suit-con" class="suit-content" clstag="shangpin|keycount|product|youhuitaozhuang_1"><div class="loading-style1"><b></b>加载中，请稍候...</div></div>
            </div>
            <div class="ui-switchable-panel hide">
                <div id="combine-con" class="combine-content" clstag="shangpin|keycount|product|zuijiazuhe_1"><div class="loading-style1"><b></b>加载中，请稍候...</div></div>
            </div>
        </div>
    </div>
</div>

<div class="w">
        <div class="right">
                <div id="J-baby"></div>
                <div id="product-detail" class="m m1" clstag="shangpin|keycount|product|detail">
            <div class="mt J-detail-tab" id="pro-detail-hd" data-fixed="pro-detail-hd-fixed">
                <div class="mt-inner m-tab-trigger-wrap clearfix">
                    <ul class="m-tab-trigger">
                        <li id="detail-tab-intro" class="ui-switchable-item trig-item curr" clstag="shangpin|keycount|product|shangpinjieshao_1"><a href="#product-detail" >商品介绍</a></li>
                                                <li id="detail-tab-param" class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|pcanshutab"><a href="#product-detail" >规格参数</a></li>
                                                                        <li id="detail-tab-list"  class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|packlisttab"><a href="#product-detail" >包装清单</a></li>
                                                                        <li id="detail-tab-comm"  class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|shangpinpingjia_1"><a href="#comment" >商品评价<em class="hl_blue hide">(0)</em></a></li>
                                                                                                <li id="detail-tab-prom"  class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|psaleservice"><a href="#product-detail">售后保障</a></li>
                                                <li id="detail-tab-yb" class="ui-switchable-item trig-item hide" clstag="shangpin|keycount|product|jingdongfuwu"><a href="#product-detail">京东服务</a></li>
                                                                                                <li id="detail-tab-doct"  class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|zhinan"><a href="#product-detail">京博士</a></li>
                                                                                            </ul>
                    <div id="nav-minicart"  style="display:block">
                        <div class="nav-minicart-inner">
                                                            <div class="nav-minicart-btn ">
                                    <a href="//cart.jd.com/gate.action?pid=595936&pcount=1&ptype=1" clstag="shangpin|keycount|product|gouwuchexuanfu_1">加入购物车</a>
                                </div>
                                                        <div class="nav-minicart-con none">
                                <div class="p-img">
                                    <img src="//img11.360buyimg.com/n4/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg" data-img="1" width="100" height="100" />
                                </div>
                                <div class="p-name">艾美特(Airmate) FSW52R 遥控落地扇/电风扇</div>
                                <div class="p-price">
                                    <em>京东价：</em>
                                    <strong class="p-price J-p-595936" id="mini-jd-price"></strong>
                                </div>
                            </div>
                            <div class="clb"></div>
                        </div>
                    </div>                    <div id="nav-jdapp" class="nav-jdapp" clstag="shangpin|keycount|product|shoujigoumai_1">
                        <div class="inner">
                            <i></i>
                            <div class="dt"><a target="_blank" href="//app.jd.com/">客户端首单 满79送79</a><b></b></div>
                            <div class="dd lh">
                                <div class="loading-style1"><b></b>加载中，请稍候...</div>
                            </div>
                        </div>
                    </div>                </div>
            </div>
            <div class="ui-switchable-panel" clstag="shangpin|keycount|product|shangpinneirongqu_1">
                <div class="mc" id="product-detail-1">
                    <div class="p-parameter" clstag="shangpin|keycount|product|canshuqu_1">
                                                <ul id="parameter2" class="p-parameter-list">
                                <li title='艾美特FSW52R'>商品名称：艾美特FSW52R</li>
    <li title='595936'>商品编号：595936</li>
                      <li title='艾美特（AIRMATE）'>品牌： <a href='//www.jd.com/pinpai/751-3085.html' target='_blank'>艾美特（AIRMATE）</a></li>
                     <li title='2014-03-04 10:55:26'>上架时间：2014-03-04 10:55:26</li>
             <li title='7.0kg'>商品毛重：7.0kg</li>
            <li title='深圳'>商品产地：深圳</li>
                                    <li title='落地扇'>类别：落地扇</li>
                  <li title='遥控版'>控制类型：遥控版</li>
                                          </ul>
                                                <p class="more-par"><a href="#product-detail" class="J-more-param">更多参数&gt;&gt;</a><p>
                                            </div>
                    <div id="J-detail-banner"></div>                                                                                                                        <div class="detail-content clearfix">
                        <div class="detail-content-wrap">
                                                        <div class="detail-correction">
                                <b></b>如果您发现商品信息不准确，<a href="//club.360buy.com/jdvote/skucheck.aspx?skuid=595936&amp;cid1=737&amp;cid2=738&amp;cid3=751" target="_blank" clstag="shangpin|keycount|product|jiucuo_1">欢迎纠错</a>
                            </div>

                            <div class="detail-content-item">
                                                                                                <div id="activity_header"><div align="center"><a target="_blank" href="http://sale.jd.com/act/DfMPSWbOUC8Lwizv.html"><img data-lazyload="http://img30.360buyimg.com/jgsq-productsoa/jfs/t2023/196/840495530/121250/f2d6bf7a/562eefb3N0f0b6097.gif" alt="" /></a></div><div align="center"><a target="_blank" href="http://sale.jd.com/act/rw31ntoGBqZ2Tk5.html"><img data-lazyload="http://img30.360buyimg.com/jgsq-productsoa/jfs/t2248/71/865247610/203154/4ab0bf2d/56301fb0Nff31d103.jpg" alt="" /></a></div></div>
                                                                                                <div id="J-detail-content"><div class="loading-style1"><b></b>商品介绍加载中...</div></div><!-- #J-detail-content -->
                                                                                                <div id="activity_footer"><div align="center"><img data-lazyload="http://img30.360buyimg.com/jgsq-productsoa/jfs/t1414/169/733509165/166234/af308485/55a77ea6N4d4d8144.jpg" alt="" /></div><div align="center"><img data-lazyload="http://img11.360buyimg.com/cms/jfs/t2167/278/350333554/218064/6d1445f0/5601091bN2799275d.jpg" alt="" usemap="#Map" height="500" border="0" width="750" /><map name="Map">  <area shape="poly" coords="150,3" href="#" />  <area shape="rect" coords="7,4,742,60" href="http://mall.jd.com/index-1000001414.html?cpdad=1DLSUE" target="_blank" />  <area shape="rect" coords="7,66,242,482" href="http://item.jd.com/183566.html" target="_blank" />  <area shape="rect" coords="260,71,487,486" href="http://item.jd.com/965742.html" target="_blank" />  <area shape="rect" coords="513,73,742,480" href="http://item.jd.com/1205663.html" target="_blank" /></map></div><div align="center"><img data-lazyload="http://img30.360buyimg.com/jgsq-productsoa/jfs/t448/250/972891238/339391/de6c3848/54a0dd45N6653edca.jpg" alt="" /><br /></div></div>
                                                            </div>
                        </div>
                                                <div id="J-detail-nav" class="detail-content-nav">
                            <ul id="J-detail-content-tab" class="detail-content-tab"></ul>
                                                                                </div>
                    </div>

                                                                                                </div>
                                            </div>
                                    <div class="ui-switchable-panel mc hide" id="product-detail-2">
                      <table cellpadding="0" cellspacing="1" width="100%" border="0" class="Ptable">
                        <tr><th class="tdTitle" colspan="2">主体</th><tr>
                              <tr><td class="tdTitle">品牌</td><td>艾美特</td></tr>
                                        <tr><td class="tdTitle">型号</td><td>FSW52R</td></tr>
                                        <tr><td class="tdTitle">类别</td><td>落地扇</td></tr>
                                        <tr><td class="tdTitle">颜色</td><td>黑色</td></tr>
                                        <tr><td class="tdTitle">产地</td><td>深圳</td></tr>
                                                    <tr><th class="tdTitle" colspan="2">材质</th><tr>
                              <tr><td class="tdTitle">电机材质</td><td>铝壳电机</td></tr>
                                        <tr><td class="tdTitle">扇叶材质</td><td>PP风叶</td></tr>
                                                    <tr><th class="tdTitle" colspan="2">功能选择</th><tr>
                              <tr><td class="tdTitle">风类模式</td><td>正常风，睡眠风</td></tr>
                                        <tr><td class="tdTitle">风力档位</td><td>3+1档</td></tr>
                                        <tr><td class="tdTitle">定时范围</td><td>0.5-7.5小时</td></tr>
                                        <tr><td class="tdTitle">摇头方式</td><td>左右摇头</td></tr>
                                        <tr><td class="tdTitle">按键方式</td><td>轻触式按键</td></tr>
                                        <tr><td class="tdTitle">显示方式</td><td>LED</td></tr>
                                        <tr><td class="tdTitle">送风原理</td><td>轴流风扇</td></tr>
                                        <tr><td class="tdTitle">升降固定</td><td>单螺钉式</td></tr>
                                        <tr><td class="tdTitle">网箍固定</td><td>轻拍式网箍</td></tr>
                                        <tr><td class="tdTitle">摇头范围</td><td>90°</td></tr>
                                        <tr><td class="tdTitle">控制方式</td><td>全遥控</td></tr>
                                                    <tr><th class="tdTitle" colspan="2">规格参数</th><tr>
                              <tr><td class="tdTitle">额定电压</td><td>220v</td></tr>
                                        <tr><td class="tdTitle">额定频率</td><td>50HZ</td></tr>
                                        <tr><td class="tdTitle">额定功率</td><td>60W</td></tr>
                                        <tr><td class="tdTitle">扇叶片数</td><td>3片</td></tr>
                                        <tr><td class="tdTitle">扇叶直径</td><td>16寸</td></tr>
                                        <tr><td class="tdTitle">产品高度</td><td>1.15cm-1.35cm</td></tr>
                                        <tr><td class="tdTitle">噪音（db）a</td><td>≤59dB(A)</td></tr>
                                        <tr><td class="tdTitle">能效等级</td><td>1级</td></tr>
                                        <tr><td class="tdTitle">净重kg</td><td>5.6</td></tr>
                                        <tr><td class="tdTitle">毛重kg</td><td>7</td></tr>
                                        <tr><td class="tdTitle">包装尺寸（mm）</td><td>555*200*455</td></tr>
                                       </table>
              </div>
                                                <div class="ui-switchable-panel mc hide" id="product-detail-3">
                <div class="item-detail">主机 × 1，说明书 × 1，遥控器 × 1</div>
            </div>
                                                <div class="ui-switchable-panel mc hide" id="product-detail-4"></div>
                                                <div class="ui-switchable-panel mc hide" id="product-detail-5">
                <div class="item-detail">
                        本产品全国联保，享受三包服务，质保期为：全国联保一年<br/>
                            自收到商品之日起，如您所购买家电商品出现质量问题，请先联系厂家进行检测，凭厂商提供的故障检测证明，在“我的京东-客户服务-返修退换货”页面提交退换申请，将有专业售后人员提供服务。京东承诺您：30天内产品出现质量问题可退货，180天内产品出现质量问题可换货，超过180天按国家三包规定享受服务。
                    您可以查询本品牌在各地售后服务中心的联系方式，<a target='_blank' href='http://www.airmate-china.com/'>请点击这儿查询......</a><br/><br/>
        品牌官方网站：<a target='_blank' href='http://www.airmate-china.com/'>http://www.airmate-china.com/</a><br/>
                售后服务电话：400-886-0315<br/>
                    </div>
            </div>

                                    <div class="ui-switchable-panel hide">
                <div id="J-yb-tab-img" class="mc yb-tab-img">
                    <img data-src="//img13.360buyimg.com/da/jfs/t955/58/96558194/276153/50963f49/54fd6bfaNae958d04.jpg" />
                </div>
            </div>
                                                            <div class="ui-switchable-panel mc hide" id="product-detail-6">
                <div class='item-detail' id='practical-guide' clstag='shangpin|keycount|product|citiao'>
                    <ul class='tab-sub'>
      <li class='ui-switchable-subitem fore curr'>实用指南</li>
  </ul>
  <ul class='ui-switchable-subpanel tabcon-sub'>
          <li>·<span>[实用指南]</span><a target='_blank' href='http://wiki.jd.com/knowledge/553.html'>电风扇工作原理</a></li>
          <li>·<span>[实用指南]</span><a target='_blank' href='http://wiki.jd.com/knowledge/554.html'>如何选购电风扇？</a></li>
          <li>·<span>[实用指南]</span><a target='_blank' href='http://wiki.jd.com/knowledge/555.html'>电风扇如何保养？</a></li>
      </ul>
                </div>
            </div>
                                                            <div id="promises" class="ui-box">
                                <div class="serve-agree-bd">
        <dl>
                <dt><i class="goods"></i><strong>正品行货</strong></dt>
                        <dd>京东商城向您保证所售商品均为正品行货，京东自营商品开具机打发票或电子发票。</dd>
                                    <dt><i class="unprofor"></i><strong>全国联保</strong></dt>
            <dd>
                凭质保证书及京东商城发票，可享受全国联保服务（奢侈品、钟表除外；奢侈品、钟表由京东联系保修，享受法定三包售后服务），与您亲临商场选购的商品享受相同的质量保证。京东商城还为您提供具有竞争力的商品价格和<a href='//help.jd.com/help/question-892.html' target='_blank'>运费政策</a>，请您放心购买！
                <br/><br/>注：因厂家会在没有任何提前通知的情况下更改产品包装、产地或者一些附件，本司不能确保客户收到的货物与商城图片、产地、附件说明完全一致。只能确保为原厂正货！并且保证与当时市场上同样主流新品一致。若本商城没有及时更新，请大家谅解！
            </dd>
                                    <dt><i class="no-worries"></i><strong>无忧退换货</strong></dt>
            <dd class="no-worries-text">
                客户购买京东自营商品7日内（含7日，自客户收到商品之日起计算），在保证商品完好的前提下，可无理由退货。（部分商品除外，详情请见各商品细则）
            </dd>
                </dl>
        </div>
                        <br /><br />
            </div>
                        <div id="state">
                <strong>权利声明：</strong><br />京东上的所有商品信息、客户评价、商品咨询、网友讨论等内容，是京东重要的经营资源，未经许可，禁止非法转载使用。
                <p><b>注：</b>本站商品信息均来自于合作方，其真实性、准确性和合法性由信息拥有者（合作方）负责。本站不提供任何保证，并不承担任何法律责任。</p>
                                    <p>印刷版次不同，印刷时间和版次以实物为准。</p>
                            </div>
        </div>

                <div id="comment" class="m m2 ">
            <div class="mt">
                <h2>商品评价</h2>
            </div>
            <div class="mc">
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
        </div>

        <div id="comments-list" class="m " clstag="shangpin|keycount|product|comment">
            <div class="mt">
                <div class="mt-inner m-tab-trigger-wrap clearfix">
                    <ul class="m-tab-trigger">
                        <li class="ui-switchable-item trig-item curr" clstag="shangpin|keycount|product|allpingjia_1"><a href="javascript:;">全部评价<em>()</em></a></li>
                        <li class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|haoping_1"><a href="javascript:;">好评<em>()</em></a></li>
                        <li class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|zhongping_1"><a href="javascript:;">中评<em>()</em></a></li>
                        <li class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|chaping_1"><a href="javascript:;">差评<em>()</em></a></li>
                        <li class="ui-switchable-item trig-item" clstag="shangpin|keycount|product|shaidantab_1"><a href="javascript:;">有图片的评价<em>()</em></a></li>
                    </ul>
                </div>
            </div>
            <div id="comment-0" class="mc ui-switchable-panel comments-table" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>            <div id="comment-1" class="mc none ui-switchable-panel comments-table" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>            <div id="comment-2" class="mc none ui-switchable-panel comments-table" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>            <div id="comment-3" class="mc none ui-switchable-panel comments-table" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>            <div id="comment-4" class="mc none ui-switchable-panel comments-table" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>        </div>                        <div id="consult" class="m m1" clstag="shangpin|keycount|product|shangpinzixun_1">
            <div class="mt">
                <div class="mt-inner m-tab-trigger-wrap clearfix">
                    <ul class="m-tab-trigger">
                        <li class="trig-item ui-switchable-item curr" clstag="shangpin|keycount|product|consult01"><a href="javascript:;">全部购买咨询</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|consult02"><a href="javascript:;">商品咨询</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|consult03"><a href="javascript:;">库存配送</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|consult04"><a href="javascript:;">支付</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|consult05"><a href="javascript:;">发票保修</a></li>
                    </ul>
                    <div id="consult-wrap" class="consult-search"> <b></b>
                        <div class="consult-pop">
                            <input type="text" id="txbReferSearch" placeholder="请输入关键词">
                            <input type="button" value="搜索" id="btnReferSearch" class="btn-search" clstag="shangpin|keycount|product|consult09"> <a class="consult-close hl_blue" href="#none" onclick="closeCounsultSearch()">取消</a>
                        </div>
                    </div>
                    <div class="J-jimi-btn consult-jimi"></div>
                                                            <div class="consult-pub">
                        <a class="css3-btn" target="_blank" href="//club.jd.com/allconsultations/595936-1-1.html#form1" clstag="shangpin|keycount|product|consult10">发表咨询</a>
                    </div>
                                    </div>
            </div>
            <div id="consult-search">
                <div class="prompt">
                    <strong>温馨提示:</strong>因厂家更改产品包装、产地或者更换随机附件等没有任何提前通知，且每位咨询者购买情况、提问时间等不同，为此以下回复仅对提问者3天内有效，其他网友仅供参考！若由此给您带来不便请多多谅解，谢谢！
                </div>
            </div>
            <div id="consult-0" class="mc tabcon ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="consult-1" class="mc tabcon none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="consult-2" class="mc tabcon none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="consult-3" class="mc tabcon none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="consult-4" class="mc tabcon none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
                    </div>
                        <div style="display: none"><a href="//cps.jd.com">销售联盟</a><a href="//gongyi.jd.com">京东公益</a><a href="//club.jd.com/links.aspx">友情链接</a>
        <div id="hidconsultations"><a href="//club.jd.com/consultation/595936-56916183.html">怎么看不到发的？想洗风扇，边上固定那个塑料圈怎么弄下来？搞了半天！不记得怎么弄了</a><a href="//club.jd.com/consultation/595936-56916074.html">想把风扇拆下来洗，边上固定的圈忘记怎么拆了？？</a><a href="//club.jd.com/consultation/595936-56735686.html">還有貨嗎？</a><a href="//club.jd.com/consultation/595936-56733899.html">买 了2年的风扇突然变得风量很小，旋转很慢，有得修理吗？</a><a href="//club.jd.com/consultation/595936-56368051.html">商品名称：艾美特(Airmate) FSW52R 遥控落地扇/电风扇直径是？</a><a href="//club.jd.com/consultation/595936-56367651.html">艾美特(Airmate) FSW52R底盘固定螺丝直径是多大？</a><a href="//club.jd.com/consultation/595936-56347183.html">你好这有热风吗</a><a href="//club.jd.com/consultation/595936-56106940.html">怎么拆卸</a><a href="//club.jd.com/consultation/595936-55781588.html">订单号245582131，2012年买的，在京东买过两台艾美特了，东西不错，但是有一套的地盘下的黑色三角掉了，可以再给我一个吗，我愿意出运费，现在风扇没法子站起来了</a><a href="//club.jd.com/consultation/595936-55699804.html">FSW52R和FSW65R-5的区别</a></div>
            <div id="hidcomment">
            <div class="item">
        <div class="user"><div class="u-name">lily_11_15</div><div class="u-address">(北京)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_fcdcec44-d9b7-40ba-9a2e-43286c2f03ec_1.html">不错不错不错不错不错</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:48:03</span></div><div class="comment-content">使用心得：不错不错不错不错不错</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">带你看大海</div><div class="u-address">()</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_c248881a-eb66-4203-ae96-ea00601a80aa_1.html">物流很快，小哥很给力</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:47:46</span></div><div class="comment-content">使用心得：物流很快，小哥很给力</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">dai974784500</div><div class="u-address">(河北)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_83ddcb59-b0ee-4f56-88fd-88fa59fb9d74_1.html">好。。。。。。..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:28:33</span></div><div class="comment-content">使用心得：好。。。。。。..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">jd180868kxc</div><div class="u-address">(广东)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_d39cc9a0-6f11-4a26-adf4-1261264c868a_1.html">一直买艾美特，..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:27:04</span></div><div class="comment-content">使用心得：一直买艾美特，..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">79010633</div><div class="u-address">(陕西)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_3bf25ca2-af09-4f53-9b30-6d4af2140b03_1.html">还行，就是有点..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:26:57</span></div><div class="comment-content">使用心得：还行，就是有点..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">biao895339443</div><div class="u-address">(四川)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_4d8e6493-2e98-42cb-b517-82ddcc6798b3_1.html">质量好，看起来..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:22:32</span></div><div class="comment-content">使用心得：质量好，看起来..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">诗琪8</div><div class="u-address">(江苏)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_f673ea31-df0d-46f4-a3e9-36c933b74caf_1.html">外观风力都还算给力</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:22:27</span></div><div class="comment-content">使用心得：外观风力都还算给力</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">jd_065123477</div><div class="u-address">(山东)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_3bec998d-8d1e-4fe3-bb5f-fe853a61b692_1.html">呜哈哈哈哈哈哈..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 19:21:10</span></div><div class="comment-content">使用心得：呜哈哈哈哈哈哈..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">anna320</div><div class="u-address">(北京)</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_b6eb0c33-63b2-4dc5-bc76-972d3197ecc4_1.html">不错非得要十个..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 18:47:28</span></div><div class="comment-content">使用心得：不错非得要十个..</div></div>
      </div>
            <div class="item">
        <div class="user"><div class="u-name">jd_海是没有982</div><div class="u-address">()</div><div class="date-buy">购买日期<br>2015-10-26</div></div>
        <div class="i-item"><div class="o-topic"><strong class="topic"><a href="//club.360buy.com/repay/595936_d91570a6-2055-4349-af2f-7672b1164397_1.html">帮别人买的，很..</a></strong><span class="star sa5"></span><span class="date-comment">2015-10-26 18:26:44</span></div><div class="comment-content">使用心得：帮别人买的，很..</div></div>
      </div>
          </div>
    </div>
                        <div id="discuss" class="m m1" data-widget="tabs" clstag="shangpin|keycount|product|alltaolunquan_1">
            <div class="mt">
                <div class="mt-inner m-tab-trigger-wrap clearfix">
                    <ul class="m-tab-trigger">
                        <li id="J-group-tab" class="trig-item ui-switchable-item hide"><a href="#none">热门贴子</a></li>
                        <li class="trig-item ui-switchable-item curr" clstag="shangpin|keycount|product|taolunquan_1"><a href="javascript:;" >网友讨论圈</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|shaidantie_1"><a href="javascript:;" >晒单贴</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|taoluntie_1"><a href="javascript:;" >讨论贴</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|wendatie_1"><a href="javascript:;" >问答贴</a></li>
                        <li class="trig-item ui-switchable-item" clstag="shangpin|keycount|product|quanzitie_1"><a href="javascript:;" >圈子贴</a></li>
                    </ul>
                </div>
            </div>
            <div id="discuss-0" class="mc ui-switchable-panel">
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="discuss-1" class="mc ui-switchable-panel">
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="discuss-2" class="mc none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="discuss-3" class="mc none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="discuss-4" class="mc none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
            <div id="discuss-5" class="mc none ui-switchable-panel" >
                <div class="loading-style1"><b></b>加载中，请稍候...</div>
            </div>
        </div>
                        <div id="related-viewed" class="m m2 hide">
            <div class="mt">
                <h2>浏览了该商品的用户还浏览了</h2>
            </div>
            <div class="mc">
                <ul class="lh"><div class="loading-style1"><b></b>加载中，请稍候...</div></ul>
            </div>
        </div>
            </div>
            <div class="left">
                            <div id="related-sorts" class="m m2" clstag="shangpin|keycount|product|sortlist_1">
        <div class="mt">
            <h2>相关分类</h2>
        </div>
        <div class="mc">
            <ul class="lh">
                                                                                            <li><a href="//list.jd.com/list.html?cat=737,738,747" target='_blank' title="取暖电器">取暖电器</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,749" target='_blank' title="净化器">净化器</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,748" target='_blank' title="加湿器">加湿器</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,12394" target='_blank' title="扫地机器人">扫地机器人</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,745" target='_blank' title="吸尘器">吸尘器</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,1279" target='_blank' title="挂烫机/熨斗">挂烫机/熨斗</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,1052" target='_blank' title="插座">插座</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,806" target='_blank' title="电话机">电话机</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,897" target='_blank' title="清洁机">清洁机</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,1283" target='_blank' title="除湿机">除湿机</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,12395" target='_blank' title="干衣机">干衣机</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,801" target='_blank' title="收录/音机">收录/音机</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,751" target='_blank' title="电风扇">电风扇</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,1278" target='_blank' title="冷风扇">冷风扇</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,825" target='_blank' title="其它生活电器">其它生活电器</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,12396" target='_blank' title="生活电器配件">生活电器配件</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,898" target='_blank' title="净水设备">净水设备</a></li>
                                                                                                                    <li><a href="//list.jd.com/list.html?cat=737,738,750" target='_blank' title="饮水机">饮水机</a></li>
                                                        </ul>
        </div>
    </div>
          <div id="related-brands" class="m m2" clstag="shangpin|keycount|product|samebrand">
        <div class="mt">
            <h2>同类其他品牌</h2>
        </div>
        <div class="mc">
            <ul class="lh">
                                                            <li><a href="//www.jd.com/pinpai/751-2505.html" target='_blank' title="TCL">TCL</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-12380.html" target='_blank' title="美的（Midea）">美的（Midea）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-3659.html" target='_blank' title="奥克斯（AUX）">奥克斯（AUX）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-3085.html" target='_blank' title="艾美特（AIRMATE）">艾美特（AIRMATE）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-20918.html" target='_blank' title="志高（CHIGO）">志高（CHIGO）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-7817.html" target='_blank' title="海尔（Haier）">海尔（Haier）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-15035.html" target='_blank' title="赛亿（Shinee）">赛亿（Shinee）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-10317.html" target='_blank' title="康佳（KONKA）">康佳（KONKA）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-7420.html" target='_blank' title="格力（GREE）">格力（GREE）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-20710.html" target='_blank' title="长虹（CHANGHONG）">长虹（CHANGHONG）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-18136.html" target='_blank' title="先锋（SINGFUN）">先锋（SINGFUN）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-8544.html" target='_blank' title="华生（Wahson）">华生（Wahson）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-7196.html" target='_blank' title="富士宝（FUSHIBAO）">富士宝（FUSHIBAO）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-3777.html" target='_blank' title="澳柯玛（AUCMA）">澳柯玛（AUCMA）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-11684.html" target='_blank' title="龙的（Longde）">龙的（Longde）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-64100.html" target='_blank' title="长城（CHANGCHENG）">长城（CHANGCHENG）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-21838.html" target='_blank' title="天骏小天使">天骏小天使</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-20988.html" target='_blank' title="中联（ZOLEE）">中联（ZOLEE）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-11505.html" target='_blank' title="联创（Lianc）">联创（Lianc）</a></li>
                                            <li><a href="//www.jd.com/pinpai/751-58415.html" target='_blank' title="永生（eosin）">永生（eosin）</a></li>
                                                </ul>
        </div>
    </div>
                        <div id="view-buy" class="m m2 related-buy"></div>
                <div id="ranklist" class="m m2" data-widget="tabs" clstag="shangpin|keycount|product|billboard">
        <div class="mt">
            <h2>电风扇排行榜</h2>
        </div>
        <div class="mc">
            <ul class="tab">
                <li class="ui-switchable-item curr">同价位</li>
                <li class="ui-switchable-item">同品牌</li>
                <li class="ui-switchable-item">同类别</li>
            </ul>
            <ul class="ui-switchable-panel tabcon">
                                                            <li class="fore1">
                        <span>1</span>
                        <div class="p-img"><a href="//item.jd.com/1361012.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t769/177/1443978083/64928/af2db003/5539d1c8N29594907.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1361012.html" target="_blank" title='美的FS40-15KRW'>美的FS40-15KRW</a></div>
                        <div class="p-price"><strong class="J-p-1361012"></strong></div>
                    </li>
                                            <li class="fore2">
                        <span>2</span>
                        <div class="p-img"><a href="//item.jd.com/594183.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t145/326/816170432/51982/a41f49e0/53984147Nd1cfec92.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/594183.html" target="_blank" title='艾美特FSW27T2-5'>艾美特FSW27T2-5</a></div>
                        <div class="p-price"><strong class="J-p-594183"></strong></div>
                    </li>
                                            <li class="fore3">
                        <span>3</span>
                        <div class="p-img"><a href="//item.jd.com/595936.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img11.360buyimg.com/n5/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/595936.html" target="_blank" title='艾美特FSW52R'>艾美特FSW52R</a></div>
                        <div class="p-price"><strong class="J-p-595936"></strong></div>
                    </li>
                                            <li class="fore4">
                        <span>4</span>
                        <div class="p-img"><a href="//item.jd.com/1058033.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t1318/73/146366273/149125/eee2a653/5552f1e6Nda38b649.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1058033.html" target="_blank" title='奥克斯FW-40-C1604'>奥克斯FW-40-C1604</a></div>
                        <div class="p-price"><strong class="J-p-1058033"></strong></div>
                    </li>
                                            <li class="fore5">
                        <span>5</span>
                        <div class="p-img"><a href="//item.jd.com/376047.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t1315/274/303564919/58264/410a7a04/55627b07Nc8fe8aa8.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/376047.html" target="_blank" title='格力FD-4010B'>格力FD-4010B</a></div>
                        <div class="p-price"><strong class="J-p-376047"></strong></div>
                    </li>
                                            <li class="fore6">
                        <span>6</span>
                        <div class="p-img"><a href="//item.jd.com/1077868.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t754/90/1390607522/63196/32686e37/5539d1b0N12e0414d.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1077868.html" target="_blank" title='美的FS40-13C'>美的FS40-13C</a></div>
                        <div class="p-price"><strong class="J-p-1077868"></strong></div>
                    </li>
                                            <li class="fore7">
                        <span>7</span>
                        <div class="p-img"><a href="//item.jd.com/1058021.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img11.360buyimg.com/n5/jfs/t1231/339/372493095/160020/35248ea6/551b4b67N1f2508ca.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1058021.html" target="_blank" title='志高FW-40-16C2RC'>志高FW-40-16C2RC</a></div>
                        <div class="p-price"><strong class="J-p-1058021"></strong></div>
                    </li>
                                                </ul>
            <ul class="ui-switchable-panel tabcon">
                                                            <li class="fore1">
                        <span>1</span>
                        <div class="p-img"><a href="//item.jd.com/1365528.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t1048/315/466185528/51721/38da4f80/55262cc7Ndbbba0f9.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1365528.html" target="_blank" title='艾美特FSW35R-14'>艾美特FSW35R-14</a></div>
                        <div class="p-price"><strong class="J-p-1365528"></strong></div>
                    </li>
                                            <li class="fore2">
                        <span>2</span>
                        <div class="p-img"><a href="//item.jd.com/594183.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t145/326/816170432/51982/a41f49e0/53984147Nd1cfec92.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/594183.html" target="_blank" title='艾美特FSW27T2-5'>艾美特FSW27T2-5</a></div>
                        <div class="p-price"><strong class="J-p-594183"></strong></div>
                    </li>
                                            <li class="fore3">
                        <span>3</span>
                        <div class="p-img"><a href="//item.jd.com/595936.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img11.360buyimg.com/n5/jfs/t1150/185/629745886/52675/b5b96c05/5535bc57N40146c65.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/595936.html" target="_blank" title='艾美特FSW52R'>艾美特FSW52R</a></div>
                        <div class="p-price"><strong class="J-p-595936"></strong></div>
                    </li>
                                            <li class="fore4">
                        <span>4</span>
                        <div class="p-img"><a href="//item.jd.com/829764.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img14.360buyimg.com/n5/jfs/t160/131/781241699/57330/12dc4cba/5398414dN44905432.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/829764.html" target="_blank" title='艾美特FSW65T2-5'>艾美特FSW65T2-5</a></div>
                        <div class="p-price"><strong class="J-p-829764"></strong></div>
                    </li>
                                            <li class="fore5">
                        <span>5</span>
                        <div class="p-img"><a href="//item.jd.com/375147.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t808/262/279633586/185233/1e89573e/550f8a45Neeb38b4c.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/375147.html" target="_blank" title='艾美特FW4035R'>艾美特FW4035R</a></div>
                        <div class="p-price"><strong class="J-p-375147"></strong></div>
                    </li>
                                            <li class="fore6">
                        <span>6</span>
                        <div class="p-img"><a href="//item.jd.com/1536383961.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img11.360buyimg.com/n5/jfs/t946/53/671960808/202943/22a778a1/553b43cdN645f8b41.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1536383961.html" target="_blank" title='艾美特(Airmate)电风扇塔扇FT41R 无叶风扇大厦风扇 静音 遥控家用香熏盒'>艾美特(Airmate)电风扇塔扇FT41R 无叶风扇大厦风扇 静音 遥控家用香熏盒</a></div>
                        <div class="p-price"><strong class="J-p-1536383961"></strong></div>
                    </li>
                                            <li class="fore7">
                        <span>7</span>
                        <div class="p-img"><a href="//item.jd.com/1083227.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t181/278/762880953/78009/f8362b86/53982a93Na44dfc6f.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1083227.html" target="_blank" title='艾美特SW59R-A'>艾美特SW59R-A</a></div>
                        <div class="p-price"><strong class="J-p-1083227"></strong></div>
                    </li>
                                                </ul>
            <ul class="ui-switchable-panel tabcon">
                                                            <li class="fore1">
                        <span>1</span>
                        <div class="p-img"><a href="//item.jd.com/1058052.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t697/293/918727221/56626/641049e3/55092f53Nf458c243.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1058052.html" target="_blank" title='TCLFS-40-AT1624'>TCLFS-40-AT1624</a></div>
                        <div class="p-price"><strong class="J-p-1058052"></strong></div>
                    </li>
                                            <li class="fore2">
                        <span>2</span>
                        <div class="p-img"><a href="//item.jd.com/1058010.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img10.360buyimg.com/n5/jfs/t1258/136/101502841/55056/f1d00e20/550a968dN80baa8f7.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1058010.html" target="_blank" title='奥克斯FS-40-A1613'>奥克斯FS-40-A1613</a></div>
                        <div class="p-price"><strong class="J-p-1058010"></strong></div>
                    </li>
                                            <li class="fore3">
                        <span>3</span>
                        <div class="p-img"><a href="//item.jd.com/1361021.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img11.360buyimg.com/n5/jfs/t847/78/676423946/46077/d5b53f01/5539d1d5N44dbed2d.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1361021.html" target="_blank" title='美的FS40-15ERW'>美的FS40-15ERW</a></div>
                        <div class="p-price"><strong class="J-p-1361021"></strong></div>
                    </li>
                                            <li class="fore4">
                        <span>4</span>
                        <div class="p-img"><a href="//item.jd.com/1074575.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img10.360buyimg.com/n5/jfs/t781/230/724537409/54964/1e64960e/553f3036N568e69aa.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1074575.html" target="_blank" title='海尔FSJ4018E'>海尔FSJ4018E</a></div>
                        <div class="p-price"><strong class="J-p-1074575"></strong></div>
                    </li>
                                            <li class="fore5">
                        <span>5</span>
                        <div class="p-img"><a href="//item.jd.com/1361012.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t769/177/1443978083/64928/af2db003/5539d1c8N29594907.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1361012.html" target="_blank" title='美的FS40-15KRW'>美的FS40-15KRW</a></div>
                        <div class="p-price"><strong class="J-p-1361012"></strong></div>
                    </li>
                                            <li class="fore6">
                        <span>6</span>
                        <div class="p-img"><a href="//item.jd.com/1365528.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img13.360buyimg.com/n5/jfs/t1048/315/466185528/51721/38da4f80/55262cc7Ndbbba0f9.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/1365528.html" target="_blank" title='艾美特FSW35R-14'>艾美特FSW35R-14</a></div>
                        <div class="p-price"><strong class="J-p-1365528"></strong></div>
                    </li>
                                            <li class="fore7">
                        <span>7</span>
                        <div class="p-img"><a href="//item.jd.com/598507.html" target="_blank"><img data-img="1" height="50" width="50"  data-lazyload="//img12.360buyimg.com/n5/jfs/t1183/194/724524047/198919/18d358b3/553f472dN49e4bd13.jpg"/></a></div>
                        <div class="p-name"><a href="//item.jd.com/598507.html" target="_blank" title='赛亿KYT25-1'>赛亿KYT25-1</a></div>
                        <div class="p-price"><strong class="J-p-598507"></strong></div>
                    </li>
                                                                        <div style='display:none'>
                                          <a href='//www.jd.com/compare/595936-1058052-0-0.html'>艾美特FSW52R和TCLFS-40-AT1624哪个好</a>
                                          <a href='//www.jd.com/compare/595936-1058010-0-0.html'>艾美特FSW52R和奥克斯FS-40-A1613哪个好</a>
                                          <a href='//www.jd.com/compare/595936-1361021-0-0.html'>艾美特FSW52R和美的FS40-15ERW哪个好</a>
                                          <a href='//www.jd.com/compare/595936-1074575-0-0.html'>艾美特FSW52R和海尔FSJ4018E哪个好</a>
                                          <a href='//www.jd.com/compare/595936-1361012-0-0.html'>艾美特FSW52R和美的FS40-15KRW哪个好</a>
                                          <a href='//www.jd.com/compare/595936-1365528-0-0.html'>艾美特FSW52R和艾美特FSW35R-14哪个好</a>
                                          <a href='//www.jd.com/compare/595936-598507-0-0.html'>艾美特FSW52R和赛亿KYT25-1哪个好</a>
                                        </div>
                            </ul>
        </div>
    </div>
                        <div id="buy-buy" class="m m2 related-buy"></div>
                <div id="browse-browse" class="m m2 related-buy"></div>
                    <div id="miaozhen7886" class="m" clstag="shangpin|keycount|product|ad_1"></div>
        <div id="miaozhen10767" class="m" clstag="shangpin|keycount|product|ad_1"></div>        </div>
        <span class="clr"></span>
</div>
<div id="footmark" class="w footmark"></div>
<div id="GLOBAL_FOOTER"></div>
<script>
seajs.config({
    paths: {
        'MISC' : '//misc.360buyimg.com',
        'APP_ROOT' : '//static.360buyimg.com/item/main/1.0.8',
        'WDG_ROOT' : '//static.360buyimg.com/item/main/1.0.8/widget',
        'JDF_UI'   : '//misc.360buyimg.com/jdf/1.0.0/ui',
        'JDF_UNIT' : '//misc.360buyimg.com/jdf/1.0.0/unit'
    }
});
seajs.use('APP_ROOT/js/entrance', function(app) {app.init();});

    if(!/debug=ad/.test(location.href)) {
        seajs.use('//d.jd.com/hotwords/get?Position=A-electronic-011');
    }


function totouchbate() {
  var exp = new Date();
  exp.setTime(exp.getTime() + 30 * 24 * 60 * 60 * 1000);
  document.cookie = "pcm=2;expires=" + exp.toGMTString() + ";path=/;domain=jd.com";
  window.location.href="//item.m.jd.com/product/595936.html";
}
if(window.showtouchurl) {
  $("#GLOBAL_FOOTER").after("<div class='ac' style='padding-bottom:30px;'>你的浏览器更适合浏览触屏版&nbsp;&nbsp;&nbsp;&nbsp;<a href='#none' style='text-decoration:underline;' onclick='totouchbate()'>京东触屏版</a></div>");
} else {
  $("#GLOBAL_FOOTER").css("padding-bottom", "30px");
}
</script>
<img src="//jcm.jd.com/pre" width="0" height="0" style="display:none"/>
<script>
seajs.use('//wl.jd.com/wl.js');


dataLayer = [{
    'google_tag_params': {
        ecomm_prodid:pageConfig.product.skuid,
        ecomm_pagetype:"item",
        ecomm_pname:pageConfig.product.name,
        ecomm_pcat:['737|738|751'],
        ecomm_pvalues:['737|738|751'],
        ecomm_totalvalue:null,
        ecomm_pbrand:3085    }
}]
</script>
<noscript>iframe(src='//www.googletagmanager.com/ns.html?id=GTM-T947SH', height='0', width='0', style='display: none; visibility: hidden;')</noscript>
<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src= '//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','GTM-T947SH');
</script><div id="J-global-toolbar"></div>
<script>
    seajs.use(['//static.360buyimg.com/devfe/toolbar/1.0.0/js/main'], function(toolbar) {
        var sid = pageConfig.product.cat[2] === 832 ? '737542' : '992349';

        pageConfig.toolbar = new toolbar({
            pType: 'item',
            bars: {
                coupon: {
                    index: 1.5,
                    enabled: true,
                    title: '优惠券',
                    login: true,
                    iframe: '//cd.jd.com/coupons?' + $.param({
                        skuId: pageConfig.product.skuid,
                        cat: pageConfig.product.cat.join(','),
                        venderId: pageConfig.product.venderId
                    })
                },
                jimi: {
                    iframe: '//jimi.jd.com/index.action?productId='+ pageConfig.product.skuid +'&source=jdhome'
                }
            },
            links: {
                feedback: {
                    href: '//surveys.jd.com/index.php?r=survey/index/sid/323814/newtest/Y/lang/zh-Hans'
                },
                top:{
                    anchor:"#"
                }
            },
            ad: {
                id: "0_0_7209",
                startTime: +new Date(2015, 9, 26, 0, 0, 1) / 1000,
                endTime: +new Date(2015, 10, 13, 0, 0, 0) / 1000
            }
        });
    });
</script></body>
</html>



        """

    print resolve_Properties(html)
    print resolve_Images(html)