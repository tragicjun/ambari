/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50090
Source Host           : localhost:3306
Source Database       : gri_monitor

Target Server Type    : MYSQL
Target Server Version : 50090
File Encoding         : 65001

Date: 2015-06-17 10:37:28
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `ge_js_error`
-- ----------------------------
DROP TABLE IF EXISTS `ge_js_error`;
CREATE TABLE `ge_js_error` (
  `ID` bigint(20) NOT NULL auto_increment,
  `SERVER_IP` varchar(100) default NULL,
  `STAFF_NAME` varchar(100) default NULL,
  `CREATE_TIME` timestamp NULL default '0000-00-00 00:00:00',
  `CHECKED` int(1) default '0',
  `URL` varchar(6000) default NULL,
  `AGENT` varchar(128) default NULL,
  `MSG` varchar(6000) default NULL COMMENT '门户英文名，唯一',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8695 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ge_js_error
-- ----------------------------

-- ----------------------------
-- Table structure for `ge_php_error`
-- ----------------------------
DROP TABLE IF EXISTS `ge_php_error`;
CREATE TABLE `ge_php_error` (
  `ID` bigint(20) NOT NULL auto_increment,
  `SERVER_IP` varchar(100) default NULL,
  `STAFF_NAME` varchar(100) default NULL,
  `CREATE_TIME` timestamp NULL default '0000-00-00 00:00:00',
  `CHECKED` int(1) default '0',
  `URL` varchar(6000) default NULL,
  `AGENT` varchar(128) default NULL,
  `MSG` varchar(6000) default NULL COMMENT '门户英文名，唯一',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4105 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ge_php_error
-- ----------------------------

-- ----------------------------
-- Table structure for `ge_portal`
-- ----------------------------
DROP TABLE IF EXISTS `ge_portal`;
CREATE TABLE `ge_portal` (
  `ID` int(11) NOT NULL auto_increment,
  `SERVER_IP` varchar(100) default NULL,
  `STAFF_NAME` varchar(100) default NULL,
  `URL` varchar(6000) default NULL,
  `CREATE_TIME` timestamp NULL default '0000-00-00 00:00:00',
  `PARAM1` varchar(500) default NULL,
  `PARAM2` varchar(500) default NULL,
  `PARAM3` varchar(500) default NULL,
  `PARAM4` varchar(500) default NULL,
  `PARAM5` varchar(500) default NULL,
  `PARAM6` varchar(500) default NULL,
  `PARAM7` varchar(500) default NULL,
  `PARAM8` varchar(500) default NULL,
  `PARAM9` varchar(500) default NULL,
  `PARAM10` varchar(500) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3324 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ge_portal
-- ----------------------------

-- ----------------------------
-- Table structure for `ge_sys`
-- ----------------------------
DROP TABLE IF EXISTS `ge_sys`;
CREATE TABLE `ge_sys` (
  `ID` int(11) NOT NULL auto_increment,
  `SERVER_IP` varchar(100) default NULL,
  `STAFF_NAME` varchar(100) default NULL,
  `URL` varchar(6000) default NULL,
  `CREATE_TIME` timestamp NULL default '0000-00-00 00:00:00',
  `PARAM1` varchar(500) default NULL,
  `PARAM2` varchar(500) default NULL,
  `PARAM3` varchar(500) default NULL,
  `PARAM4` varchar(500) default NULL,
  `PARAM5` varchar(500) default NULL,
  `PARAM6` varchar(500) default NULL,
  `PARAM7` varchar(500) default NULL,
  `PARAM8` varchar(500) default NULL,
  `PARAM9` varchar(500) default NULL,
  `PARAM10` varchar(500) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=18363 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ge_sys
-- ----------------------------
