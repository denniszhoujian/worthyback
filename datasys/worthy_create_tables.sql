-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: worthyDB
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.10.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `jd_analytic_category_rating`
--

DROP TABLE IF EXISTS `jd_analytic_category_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_category_rating` (
  `category_id` varchar(255) NOT NULL,
  `sample_count` int(11) NOT NULL,
  `sum_1` int(11) NOT NULL,
  `sum_2` int(11) NOT NULL,
  `sum_3` int(11) NOT NULL,
  `sum_4` int(11) NOT NULL,
  `sum_5` int(11) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `rate_1` float DEFAULT NULL,
  `rate_2` float DEFAULT NULL,
  `rate_3` float DEFAULT NULL,
  `rate_4` float DEFAULT NULL,
  `rate_5` float DEFAULT NULL,
  `rate_good` float DEFAULT NULL,
  `rate_bad` float DEFAULT NULL,
  `origin_dt` date DEFAULT NULL,
  `dt` date NOT NULL,
  `category_name` varchar(255) NOT NULL,
  PRIMARY KEY (`category_id`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_category_rating_latest`
--

DROP TABLE IF EXISTS `jd_analytic_category_rating_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_category_rating_latest` (
  `category_id` varchar(255) NOT NULL,
  `sample_count` int(11) NOT NULL,
  `sum_1` int(11) NOT NULL,
  `sum_2` int(11) NOT NULL,
  `sum_3` int(11) NOT NULL,
  `sum_4` int(11) NOT NULL,
  `sum_5` int(11) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `rate_1` float DEFAULT NULL,
  `rate_2` float DEFAULT NULL,
  `rate_3` float DEFAULT NULL,
  `rate_4` float DEFAULT NULL,
  `rate_5` float DEFAULT NULL,
  `rate_good` float DEFAULT NULL,
  `rate_bad` float DEFAULT NULL,
  `origin_dt` date DEFAULT NULL,
  `dt` date NOT NULL,
  `category_name` varchar(255) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_item_rating_diff`
--

DROP TABLE IF EXISTS `jd_analytic_item_rating_diff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_item_rating_diff` (
  `sku_id` bigint(20) NOT NULL,
  `dt` date NOT NULL,
  `category_id` varchar(255) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `comment_count` int(11) NOT NULL,
  `category_sample_count` int(11) NOT NULL,
  `rate_good` float DEFAULT NULL,
  `category_rate_good` float DEFAULT NULL,
  `rate_good_diff` float DEFAULT NULL,
  `rate_bad` float DEFAULT NULL,
  `category_rate_bad` float DEFAULT NULL,
  `rate_bad_diff` float DEFAULT NULL,
  `rate_1` float DEFAULT NULL,
  `category_rate_1` float DEFAULT NULL,
  `rate_1_diff` float DEFAULT NULL,
  `rate_2` float DEFAULT NULL,
  `category_rate_2` float DEFAULT NULL,
  `rate_2_diff` float DEFAULT NULL,
  `rate_3` float DEFAULT NULL,
  `category_rate_3` float DEFAULT NULL,
  `rate_3_diff` float DEFAULT NULL,
  `rate_4` float DEFAULT NULL,
  `category_rate_4` float DEFAULT NULL,
  `rate_4_diff` float DEFAULT NULL,
  `rate_5` float DEFAULT NULL,
  `category_rate_5` float DEFAULT NULL,
  `rate_5_diff` float DEFAULT NULL,
  `item_origin_dt` date DEFAULT NULL,
  `category_origin_dt` date DEFAULT NULL,
  `raw_origin_dt` date DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_deduction`
--

DROP TABLE IF EXISTS `jd_analytic_promo_deduction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_deduction` (
  `sku_id` bigint(20) NOT NULL,
  `add_time` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `is_repeat` varchar(255) NOT NULL,
  `reach` varchar(255) NOT NULL,
  `deduction` varchar(255) NOT NULL,
  `max_deduction` varchar(255) NOT NULL,
  `dr_ratio` varchar(255) NOT NULL,
  `maxp_ratio` varchar(255) NOT NULL,
  `single_discount_rate` varchar(255) NOT NULL,
  `category_id` varchar(11) NOT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `origin_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_deduction_latest`
--

DROP TABLE IF EXISTS `jd_analytic_promo_deduction_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_deduction_latest` (
  `sku_id` bigint(20) NOT NULL,
  `add_time` datetime NOT NULL,
  `title` varchar(255) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `is_repeat` varchar(255) NOT NULL,
  `reach` varchar(255) NOT NULL,
  `deduction` varchar(255) NOT NULL,
  `max_deduction` varchar(255) NOT NULL,
  `dr_ratio` varchar(255) NOT NULL,
  `maxp_ratio` varchar(255) NOT NULL,
  `single_discount_rate` varchar(255) NOT NULL,
  `category_id` varchar(255) NOT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `origin_time` datetime NOT NULL,
  PRIMARY KEY (`sku_id`,`reach`),
  KEY `skuid` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_discount`
--

DROP TABLE IF EXISTS `jd_analytic_promo_discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_discount` (
  `sku_id` bigint(20) NOT NULL,
  `add_time` datetime NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `deduct_type` smallint(6) DEFAULT NULL,
  `reach_num` smallint(6) DEFAULT NULL,
  `discount` float DEFAULT NULL,
  `free_num` smallint(6) DEFAULT NULL,
  `rf_ratio` float DEFAULT NULL,
  `category_id` varchar(255) DEFAULT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `origin_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_discount_latest`
--

DROP TABLE IF EXISTS `jd_analytic_promo_discount_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_discount_latest` (
  `sku_id` bigint(20) NOT NULL,
  `add_time` datetime NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `deduct_type` smallint(6) DEFAULT NULL,
  `reach_num` smallint(6) DEFAULT NULL,
  `discount` float DEFAULT NULL,
  `free_num` smallint(6) DEFAULT NULL,
  `rf_ratio` float DEFAULT NULL,
  `category_id` varchar(255) DEFAULT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `origin_dt` datetime DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`pid`),
  KEY `skuid` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_gift`
--

DROP TABLE IF EXISTS `jd_analytic_promo_gift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_gift` (
  `sku_id` bigint(20) NOT NULL,
  `dt` datetime NOT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `gift_name` varchar(255) NOT NULL,
  `gift_num` int(11) NOT NULL,
  `gift_image` varchar(255) DEFAULT NULL,
  `gift_sku_id` bigint(20) NOT NULL,
  `gift_gt` varchar(255) DEFAULT NULL,
  `gift_gs` varchar(255) DEFAULT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`sku_id`,`dt`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_gift_latest`
--

DROP TABLE IF EXISTS `jd_analytic_promo_gift_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_gift_latest` (
  `sku_id` bigint(20) NOT NULL,
  `dt` datetime NOT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `gift_name` varchar(255) NOT NULL,
  `gift_num` int(11) NOT NULL,
  `gift_image` varchar(255) DEFAULT NULL,
  `gift_sku_id` bigint(20) NOT NULL,
  `gift_gt` varchar(255) DEFAULT NULL,
  `gift_gs` varchar(255) DEFAULT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`sku_id`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_gift_valued`
--

DROP TABLE IF EXISTS `jd_analytic_promo_gift_valued`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_gift_valued` (
  `sku_id` bigint(20) NOT NULL,
  `dt` datetime NOT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `gift_name` varchar(255) NOT NULL,
  `gift_num` int(11) NOT NULL,
  `gift_image` varchar(255) DEFAULT NULL,
  `gift_sku_id` bigint(20) NOT NULL,
  `gift_gt` varchar(255) DEFAULT NULL,
  `gift_gs` varchar(255) DEFAULT NULL,
  `update_date` datetime NOT NULL,
  `price` float DEFAULT NULL,
  `gift_price` float DEFAULT NULL,
  `gift_value` float DEFAULT NULL,
  `gift_ratio` float DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`pid`),
  KEY `skuid` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_item`
--

DROP TABLE IF EXISTS `jd_analytic_promo_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_item` (
  `sku_id` bigint(20) NOT NULL,
  `dt` datetime NOT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`sku_id`,`dt`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytic_promo_item_latest`
--

DROP TABLE IF EXISTS `jd_analytic_promo_item_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytic_promo_item_latest` (
  `sku_id` bigint(20) NOT NULL,
  `dt` datetime NOT NULL,
  `pid` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
  `adurl` varchar(255) DEFAULT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`sku_id`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytics_price_base`
--

DROP TABLE IF EXISTS `jd_analytics_price_base`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytics_price_base` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` date NOT NULL,
  `price_base` decimal(10,0) NOT NULL,
  PRIMARY KEY (`sku_id`,`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_analytics_price_base_latest`
--

DROP TABLE IF EXISTS `jd_analytics_price_base_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_analytics_price_base_latest` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` date NOT NULL,
  `price_base` decimal(10,0) NOT NULL,
  PRIMARY KEY (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_category`
--

DROP TABLE IF EXISTS `jd_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_category` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `add_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_category_white_list`
--

DROP TABLE IF EXISTS `jd_category_white_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_category_white_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` varchar(255) NOT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `is_service` tinyint(4) unsigned zerofill NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_category`
--

DROP TABLE IF EXISTS `jd_item_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_category` (
  `sku_id` bigint(11) NOT NULL,
  `category_id` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`category_id`),
  KEY `sku` (`sku_id`),
  KEY `category` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_comment_count`
--

DROP TABLE IF EXISTS `jd_item_comment_count`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_comment_count` (
  `ShowCount` int(11) NOT NULL,
  `GeneralCount` int(11) NOT NULL,
  `GoodRateShow` int(11) NOT NULL,
  `GoodRateStyle` int(11) NOT NULL,
  `GeneralRateShow` int(11) NOT NULL,
  `Score2Count` int(11) NOT NULL,
  `AverageScore` int(11) NOT NULL,
  `PoorRateStyle` int(11) NOT NULL,
  `CommentCount` int(11) NOT NULL,
  `GoodRate` float(11,0) NOT NULL,
  `PoorRate` float(11,0) NOT NULL,
  `GeneralRate` float(11,0) NOT NULL,
  `dt` date NOT NULL,
  `ProductId` bigint(11) NOT NULL,
  `SkuId` bigint(11) NOT NULL,
  `GeneralRateStyle` int(11) NOT NULL,
  `Score5Count` int(11) NOT NULL,
  `Score4Count` int(11) NOT NULL,
  `Score3Count` int(11) NOT NULL,
  `GoodCount` int(11) NOT NULL,
  `PoorCount` int(11) NOT NULL,
  `Score1Count` int(11) NOT NULL,
  `PoorRateShow` int(11) NOT NULL,
  PRIMARY KEY (`SkuId`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_comment_count_latest`
--

DROP TABLE IF EXISTS `jd_item_comment_count_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_comment_count_latest` (
  `ShowCount` int(11) NOT NULL,
  `GeneralCount` int(11) NOT NULL,
  `GoodRateShow` int(11) NOT NULL,
  `GoodRateStyle` int(11) NOT NULL,
  `GeneralRateShow` int(11) NOT NULL,
  `Score2Count` int(11) NOT NULL,
  `AverageScore` int(11) NOT NULL,
  `PoorRateStyle` int(11) NOT NULL,
  `CommentCount` int(11) NOT NULL,
  `GoodRate` float(11,0) NOT NULL,
  `PoorRate` float(11,0) NOT NULL,
  `GeneralRate` float(11,0) NOT NULL,
  `dt` date NOT NULL,
  `ProductId` bigint(11) NOT NULL,
  `SkuId` bigint(11) NOT NULL,
  `GeneralRateStyle` int(11) NOT NULL,
  `Score5Count` int(11) NOT NULL,
  `Score4Count` int(11) NOT NULL,
  `Score3Count` int(11) NOT NULL,
  `GoodCount` int(11) NOT NULL,
  `PoorCount` int(11) NOT NULL,
  `Score1Count` int(11) NOT NULL,
  `PoorRateShow` int(11) NOT NULL,
  PRIMARY KEY (`SkuId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_dynamic`
--

DROP TABLE IF EXISTS `jd_item_dynamic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
  PRIMARY KEY (`sku_id`,`update_date`),
  KEY `sku_id-dt` (`sku_id`,`update_date`),
  KEY `sku_id` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_dynamic_latest`
--

DROP TABLE IF EXISTS `jd_item_dynamic_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_dynamic_latest` (
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
  PRIMARY KEY (`sku_id`),
  KEY `sku_id` (`sku_id`),
  KEY `sku_id_dt` (`sku_id`,`update_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_images`
--

DROP TABLE IF EXISTS `jd_item_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_images` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` datetime NOT NULL,
  `image_url` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`update_time`,`image_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_images_latest`
--

DROP TABLE IF EXISTS `jd_item_images_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_images_latest` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` datetime NOT NULL,
  `image_url` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`image_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_property`
--

DROP TABLE IF EXISTS `jd_item_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_property` (
  `sku_id` int(11) NOT NULL,
  `update_date` datetime NOT NULL,
  `p_key` varchar(255) NOT NULL,
  `p_value` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`update_date`,`p_key`,`p_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_property_latest`
--

DROP TABLE IF EXISTS `jd_item_property_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_property_latest` (
  `sku_id` int(11) NOT NULL,
  `update_date` datetime NOT NULL,
  `p_key` varchar(255) NOT NULL,
  `p_value` varchar(255) NOT NULL,
  PRIMARY KEY (`sku_id`,`p_key`,`p_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_stock`
--

DROP TABLE IF EXISTS `jd_item_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_stock` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` datetime NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `l` int(11) DEFAULT NULL,
  `j` int(11) DEFAULT NULL,
  `stock_json` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_item_stock_latest`
--

DROP TABLE IF EXISTS `jd_item_stock_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_item_stock_latest` (
  `sku_id` bigint(20) NOT NULL,
  `update_time` datetime NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `l` int(11) DEFAULT NULL,
  `j` int(11) DEFAULT NULL,
  `stock_json` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`sku_id`),
  KEY `sku` (`sku_id`),
  KEY `sku-dt` (`sku_id`,`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_price`
--

DROP TABLE IF EXISTS `jd_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_price` (
  `sku_id` bigint(20) NOT NULL,
  `current_price` float NOT NULL,
  `average_price` float NOT NULL,
  `min_price` float NOT NULL,
  `max_price` float NOT NULL,
  `price_m` float NOT NULL,
  `discount_rate` float NOT NULL,
  `update_date` date NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `j` int(11) DEFAULT NULL,
  `l` int(11) DEFAULT NULL,
  `stock_json` varchar(2048) DEFAULT NULL,
  `stock_update_time` datetime DEFAULT NULL,
  `category_id` varchar(255) NOT NULL,
  `cat_ads_json` varchar(2048) DEFAULT NULL,
  `cat_promo_json` varchar(2048) DEFAULT NULL,
  `cat_quan_json` varchar(2048) DEFAULT NULL,
  `cat_promo_dt` date DEFAULT NULL,
  `ads_json` varchar(2048) DEFAULT NULL,
  `promo_json` varchar(2048) DEFAULT NULL,
  `quan_json` varchar(2048) DEFAULT NULL,
  `promo_dt` date DEFAULT NULL,
  PRIMARY KEY (`sku_id`),
  KEY `sku` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_price_temp`
--

DROP TABLE IF EXISTS `jd_price_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_price_temp` (
  `sku_id` bigint(20) NOT NULL,
  `current_price` float NOT NULL,
  `average_price` float NOT NULL,
  `min_price` float NOT NULL,
  `max_price` float NOT NULL,
  `price_m` float NOT NULL,
  `discount_rate` float NOT NULL,
  `update_date` date NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
  `j` int(11) DEFAULT NULL,
  `l` int(11) DEFAULT NULL,
  `stock_json` varchar(2048) DEFAULT NULL,
  `stock_update_time` datetime DEFAULT NULL,
  `category_id` varchar(255) NOT NULL,
  `cat_ads_json` varchar(2048) DEFAULT NULL,
  `cat_promo_json` varchar(2048) DEFAULT NULL,
  `cat_quan_json` varchar(2048) DEFAULT NULL,
  `cat_promo_dt` date DEFAULT NULL,
  PRIMARY KEY (`sku_id`),
  KEY `sku` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_promo_category`
--

DROP TABLE IF EXISTS `jd_promo_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_promo_category` (
  `category_id` varchar(255) NOT NULL,
  `dt` date NOT NULL,
  `quan_json` varchar(2048) DEFAULT NULL,
  `ads_json` varchar(2048) DEFAULT NULL,
  `promo_json` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`category_id`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_promo_category_latest`
--

DROP TABLE IF EXISTS `jd_promo_category_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_promo_category_latest` (
  `category_id` varchar(255) NOT NULL,
  `dt` date NOT NULL,
  `quan_json` varchar(2048) DEFAULT NULL,
  `ads_json` varchar(2048) DEFAULT NULL,
  `promo_json` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  KEY `catid` (`category_id`),
  KEY `catid-dt` (`category_id`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_promo_item`
--

DROP TABLE IF EXISTS `jd_promo_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_promo_item` (
  `sku_id` varchar(255) NOT NULL,
  `dt` datetime NOT NULL,
  `quan_json` varchar(2048) DEFAULT NULL,
  `ads_json` varchar(2048) DEFAULT NULL,
  `promo_json` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`sku_id`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `jd_promo_item_latest`
--

DROP TABLE IF EXISTS `jd_promo_item_latest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jd_promo_item_latest` (
  `sku_id` varchar(255) NOT NULL,
  `dt` datetime NOT NULL,
  `quan_json` varchar(2048) DEFAULT NULL,
  `ads_json` varchar(2048) DEFAULT NULL,
  `promo_json` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`sku_id`),
  KEY `sku_dt` (`sku_id`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `task_status`
--

DROP TABLE IF EXISTS `task_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(255) NOT NULL,
  `task_id` varchar(255) NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jb_dt` (`job_name`,`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=8650740 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `test_id` int(11) NOT NULL,
  `test_value` varchar(255) NOT NULL,
  PRIMARY KEY (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-11-14  1:42:33
