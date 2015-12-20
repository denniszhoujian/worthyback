# encoding: utf-8

"""
select
a.sku_id as sku_id,
title,
price,
id,
name

from
jd_item_dynamic_latest a
left join
jd_item_category b
on a.sku_id = b.sku_id
left join jd_category c
on b.category_id = c.id

order by id ASC, price ASC
"""