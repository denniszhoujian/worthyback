CREATE TABLE `jd_category` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `add_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `jd_category_white_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8

CREATE TABLE `jd_item_category` (
  `sku_id` bigint(11) NOT NULL,
  `category_id` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `jd_item_dynamic` (
  `sku_id` bigint(20) NOT NULL,
  `update_date` date NOT NULL,
  `update_time` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `thumbnail_url` varchar(255) NOT NULL,
  `stock_status` tinyint(4) NOT NULL,
  `comment_count` bigint(20) NOT NULL,
  `is_global` tinyint(4) NOT NULL,
  `is_pay_on_delivery` tinyint(4) NOT NULL,
  `has_free_gift` tinyint(4) NOT NULL,
  `icon_url` varchar(255) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `price_m` decimal(10,0) NOT NULL,
  `price_pcp` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`update_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `jd_item_images` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` datetime NOT NULL,
  `image_url` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`update_time`,`image_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


CREATE TABLE `jd_item_property` (
  `sku_id` int(11) NOT NULL,
  `update_date` datetime NOT NULL,
  `p_key` varchar(255) NOT NULL,
  `p_value` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`update_date`,`p_key`,`p_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `jd_item_property_latest` (
  `sku_id` int(11) NOT NULL,
  `update_date` datetime NOT NULL,
  `p_key` varchar(255) NOT NULL,
  `p_value` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`p_key`,`p_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `task_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(255) NOT NULL,
  `task_id` varchar(255) NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5316 DEFAULT CHARSET=utf8

