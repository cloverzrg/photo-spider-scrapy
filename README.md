# photo-spider-scrapy

some photo spider.

### create project
```
scrapy startproject project_name
```

### run project
```
scrapy crawl project_name
```

### set up user agent
```
https://blog.jeongen.com/python-scrapy-she-zhi-useragent/
```

### MySQL
```sql
/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : photo

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2017-08-09 17:24:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for magdeleine
-- ----------------------------
DROP TABLE IF EXISTS `magdeleine`;
CREATE TABLE `magdeleine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_url` varchar(255) NOT NULL,
  `photo_url` varchar(255) NOT NULL,
  `resolution` char(20) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `chinese_category` varchar(255) DEFAULT NULL,
  `chinese_tags` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1226 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pexels
-- ----------------------------
DROP TABLE IF EXISTS `pexels`;
CREATE TABLE `pexels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(500) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `resolution` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `type_id` int(3) DEFAULT '0',
  `chinese_tags` varchar(255) DEFAULT NULL,
  `thumb_name` varchar(255) DEFAULT NULL,
  `thumb_name2` varchar(255) DEFAULT NULL,
  `is_posted` int(255) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37971 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for photock
-- ----------------------------
DROP TABLE IF EXISTS `photock`;
CREATE TABLE `photock` (
  `url` varchar(255) NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stocksnap
-- ----------------------------
DROP TABLE IF EXISTS `stocksnap`;
CREATE TABLE `stocksnap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `img_id` char(20) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `chinese_tags` varchar(255) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `file_size` char(10) DEFAULT NULL,
  `thumb_name` varchar(255) DEFAULT NULL,
  `thumb_name2` varchar(255) DEFAULT NULL,
  `posted` int(2) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`img_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=81955 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stockvault
-- ----------------------------
DROP TABLE IF EXISTS `stockvault`;
CREATE TABLE `stockvault` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `file_size` varchar(20) DEFAULT NULL,
  `resolution` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `chinese_tags` varchar(255) DEFAULT NULL,
  `is_posted` int(255) DEFAULT '0',
  `thumb_name` varchar(255) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `chinese_title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=237592 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Function structure for LastIndexOf
-- ----------------------------
DROP FUNCTION IF EXISTS `LastIndexOf`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `LastIndexOf`(`str` varchar(255),`mysubstr` varchar(255)) RETURNS int(11)
BEGIN
	#Routine body goes here...
	DECLARE pos int(5);
	DECLARE re_pos int(5);
	set re_pos = INSTR(REVERSE(str), REVERSE(mysubstr));
	if re_pos = 0 THEN
		RETURN 0;
	end if;
	set pos = LENGTH(str) - re_pos - LENGTH(mysubstr) + 2;
	RETURN pos;
END
;;
DELIMITER ;

```