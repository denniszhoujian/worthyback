# encoding: utf-8

from datasys import dbhelper, timeHelper
import rows_helper

JD_CATALOG_ARRAY = [

    {
        'catalog_name': '营养健康',
        'category_ids': [
			'	营养健康	',
			'	营养成分	',
			'	滋补养生	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '高端配饰',
        'category_ids': [
			'	饰品	',
			'	箱包	',
			'	钱包	',
			'	腰带	',
			'	太阳镜/眼镜框	',
			'	配件	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '高端服饰',
        'category_ids': [
			'	鞋靴	',
			'	服饰	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '餐厨用品',
        'category_ids': [
			'	烹饪锅具	',
			'	刀剪菜板	',
			'	厨房配件	',
			'	水具酒具	',
			'	餐具	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '户外服饰',
        'category_ids': [
			'	运动服饰	',
			'	户外鞋服	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '运动健身',
        'category_ids': [
 			'	骑行运动	',
			'	游泳用品	',
			'	健身训练	',
			'	体育用品	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '户外装备',
        'category_ids': [
            '	户外装备	',
            # '	垂钓用品	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '婴儿日常',
        'category_ids': [
            '	奶粉	',
			'	营养辅食	',
			'	尿裤湿巾	',
			'	喂养用品	',
			'	洗护用品	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '婴儿家居',
        'category_ids': [
            '童装童鞋',
			'	安全座椅	',
            '	童车童床	',
        ],
        'max_price':None,
    },

     {
        'catalog_name': '个人护理',
        'category_ids': [
            '	面部护肤	',
            '	身体护肤	',
            '	口腔护理	',
            '	女性护理	',
            '	洗发护发	',
            # JD put the below in other categories though...
            '	个护健康	',
            '	护理护具	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '美容美妆',
        'category_ids': [
			'	香水彩妆	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '五金家装',
        'category_ids': [
            '	五金家装	',
        ],
        'max_price':None,
    },


    {
        'catalog_name': '超市-食品',
        'category_ids': [
			'	休闲食品	',
			# '	粮油调味	',
			'	饮料冲调	',
			'	食品礼券	',
        ],
        'max_price':None,
    },


    # {
    #     'catalog_name': '超市-粮油调味',
    #     'category_ids': [
    #         '	粮油调味	',
    #     ],
    #     'max_price':None,
    # },


    {
        'catalog_name': '超市-生鲜',
        'category_ids': [
            '	生鲜	',
        ],
        'max_price':None,
    },


    # {
    #     'catalog_name': '超市-茗茶',
    #     'category_ids': [
    #         '	茗茶	',
    #     ],
    #     'max_price':None,
    # },

    {
        'catalog_name': '超市-进口食品',
        'category_ids': [
            '	进口食品	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '厨房电器',
        'category_ids': [
			'	厨房电器	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '生活电器',
        'category_ids': [
			'	生活电器	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '数码配件',
        'category_ids': [
            '	数码配件	',
            '家电配件',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '游戏设备',
        'category_ids': [
            '	游戏设备	',
            '游戏本'
        ],
        'max_price':None,
    },

    {
        'catalog_name': '摄影摄像',
        'category_ids': [
            '	摄影摄像	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '智能设备',
        'category_ids': [
            '	智能设备	',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '影音娱乐',
        'category_ids': [
            '	影音娱乐	',
            '迷你音响',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '电脑配件',
        'category_ids': [
			'	电脑配件	',
			'	外设产品	',
			'	网络产品	',
			'	服务产品	',
            '平板电脑配件',
            '笔记本配件',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '电脑/笔记本',
        'category_ids': [
			'游戏本',
            '一体机',
            '平板电脑',
            '笔记本',
            '台式机',
            '超极本',
        ],
        'max_price':None,
    },

    {
        'catalog_name': '手机配件',
        'category_ids': [
			'	手机配件	',
        ],
        'max_price':None,
    },


    {
        'catalog_name': '大家电',
        'category_ids': [
            '冷柜/冰吧',
            '酒柜',
            '烟机/灶具',
            '消毒柜/洗碗机',
            '热水器',
            '平板电视',
            '家庭影院',
            '空调',
            '冰箱',
            '洗衣机',
            'DVD'
        ],
        'max_price':None,
    },

    {
        'catalog_name': '手机',
        'category_ids': [
            '	手机	',
        ],
        'max_price':None,
    },



    # {
    #     'catalog_name': '',
    #     'category_ids': [
    #
    #     ],
    #     'max_price':None,
    # },
    #
    # {
    #     'catalog_name': '',
    #     'category_ids': [
    #
    #     ],
    #     'max_price':None,
    # },

]

# global CATEGORY_MAP
# CATEGORY_MAP = {}

def _load_category_map():
    sql = 'select category_id_prefix,category_prefix_name from jd_category_show'
    retrows = dbhelper.executeSqlRead(sql)
    retdict = rows_helper.transform_retrows_to_dict(retrows,'category_prefix_name')
    return retdict

def _get_category_id_prefix_given_category_name(category_name) :
    # global CATEGORY_MAP
    # if len(CATEGORY_MAP)==0:
    #     CATEGORY_MAP = _load_category_map()
    category_name = category_name.decode('utf-8')
    CATEGORY_MAP = _load_category_map()
    if category_name in CATEGORY_MAP:
        return [CATEGORY_MAP[category_name]['category_id_prefix'],CATEGORY_MAP[category_name]['category_prefix_name'] ]
    else:
        raise Exception("%s not found in category_map" %category_name)
        return None

def fill_catalog():

    tnow = timeHelper.getNowLong()

    catalog_id = 1000
    vlist = []
    tlist = []
    for cdict in JD_CATALOG_ARRAY:
        ttp = []
        catids = cdict['category_ids']
        catalog_name = cdict['catalog_name'].strip()
        ttp += [ catalog_id, catalog_name, catalog_id, tnow ]

        for item in catids:
            vtp = []
            cat_name = item.strip()
            id_prefix_array = _get_category_id_prefix_given_category_name(cat_name)
            vtp += id_prefix_array
            vtp += [catalog_id, catalog_name, tnow]
            vlist.append(vtp)

        tlist.append(ttp)
        catalog_id += 1000

    sql1 = 'insert into jd_catalog values(%s,%s,%s,%s)'
    ar1 = dbhelper.executeSqlWriteMany(sql1, tlist)

    sql2 = 'insert into jd_catalog_map values(%s,%s,%s,%s,%s)'
    ar2 = dbhelper.executeSqlWriteMany(sql2, vlist)

    print 'jd_catalog rows inserted: %s' %ar1
    print 'jd_catalog_ref rows inserted: %s' %ar2


def empty_catalogs():
    sql1 = 'delete from jd_catalog'
    sql2 = 'delete from jd_catalog_map'
    ret1 = dbhelper.executeSqlWrite1(sql1)
    ret2 = dbhelper.executeSqlWrite1(sql2)
    print ret1
    print ret2


"""
DEBUG SQL

insert into jd_category_show

select

id,
name,
name,
5000,
CURRENT_TIMESTAMP()

from jd_category

where id like '670-671-%'





select

a.sku_id,
a.category_id,
b.title

from

jd_item_category a
left join
jd_item_dynamic_latest b
using(sku_id)

where a.category_id like '1320-5019-%'



select a.*, b.*, d.* from

jd_item_category a
left JOIN
jd_category b
on a.category_id = b.id

left join jd_worthy_latest c
on a.sku_id = c.sku_id

left join jd_catalog_map d
on c.catalog_id = d.catalog_id

where a.sku_id = 769338



select * from jd_category
where id like '670-671-%'

"""


if __name__ == "__main__":
    empty_catalogs()
    fill_catalog()


