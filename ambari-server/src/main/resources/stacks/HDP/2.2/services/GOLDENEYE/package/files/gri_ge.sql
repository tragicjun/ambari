/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50090
Source Host           : localhost:3306
Source Database       : gri_ge

Target Server Type    : MYSQL
Target Server Version : 50090
File Encoding         : 65001

Date: 2015-06-17 10:37:07
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `database_config`
-- ----------------------------
DROP TABLE IF EXISTS `database_config`;
CREATE TABLE `database_config` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `NAME` varchar(100) NOT NULL,
  `ALIAS` varchar(100) NOT NULL,
  `DRIVER` varchar(50) NOT NULL,
  `DATA_CHARACTER` varchar(50) default NULL,
  `URL` varchar(512) NOT NULL,
  `USERNAME` varchar(50) NOT NULL,
  `PORT` int(10) NOT NULL default '3306',
  `PASSWORD` varchar(100) NOT NULL,
  `PRIVATE_TABLE` text,
  `MEMO` varchar(1000) default NULL COMMENT '数据源描述',
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=240 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of database_config
-- ----------------------------

-- ----------------------------
-- Table structure for `database_data_index`
-- ----------------------------
DROP TABLE IF EXISTS `database_data_index`;
CREATE TABLE `database_data_index` (
  `ID` int(11) NOT NULL auto_increment,
  `DATABASE_ID` int(11) NOT NULL,
  `DATATABLE_ID` int(11) NOT NULL,
  `FIELDNAME` varchar(100) NOT NULL COMMENT '字段名',
  `NAME` varchar(100) NOT NULL COMMENT '指标名称',
  `MEMO` varchar(1024) default NULL COMMENT '指标备注',
  `INDEX_TYPE` int(11) NOT NULL COMMENT '一般数据指标；自定义指标',
  `DATA_TYPE` int(11) NOT NULL COMMENT '整数、小数、百分比',
  `DECIMALS` int(11) NOT NULL COMMENT '小数位数',
  `INDEX_CONFIG` varchar(512) default NULL COMMENT '指标配置()',
  `DATE_TYPE` varchar(50) NOT NULL,
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`),
  KEY `datatable_id_index` (`DATATABLE_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=69752 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of database_data_index
-- ----------------------------

-- ----------------------------
-- Table structure for `database_dimension_dictionary`
-- ----------------------------
DROP TABLE IF EXISTS `database_dimension_dictionary`;
CREATE TABLE `database_dimension_dictionary` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL,
  `DATABASE_ID` int(11) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `KEY_FIELD` varchar(100) NOT NULL,
  `VALUE_FIELD` varchar(100) NOT NULL,
  `PARENT_FIELD` varchar(100) default NULL,
  `FILTER_CONDITION` varchar(100) default NULL,
  `ORDER_CONDITION` varchar(100) default NULL,
  `TYPE` int(11) NOT NULL default '1',
  `MEMO` varchar(1024) default NULL COMMENT '数据表描述',
  `IS_ENABLED` int(11) NOT NULL,
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=539 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of database_dimension_dictionary
-- ----------------------------

-- ----------------------------
-- Table structure for `database_dimension_index`
-- ----------------------------
DROP TABLE IF EXISTS `database_dimension_index`;
CREATE TABLE `database_dimension_index` (
  `ID` int(11) NOT NULL auto_increment,
  `DATABASE_ID` int(11) NOT NULL,
  `DATATABLE_ID` int(11) NOT NULL,
  `FIELDNAME` varchar(100) NOT NULL COMMENT '字段名',
  `NAME` varchar(100) NOT NULL COMMENT '指标名称',
  `DICTIONARY_ID` int(11) NOT NULL COMMENT '维度字典ID',
  `MEMO` varchar(1024) default NULL COMMENT '指标备注',
  `PARENT_FIELD` int(11) default NULL,
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`),
  KEY `数据表ID索引` (`DATATABLE_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11871 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of database_dimension_index
-- ----------------------------

-- ----------------------------
-- Table structure for `datatable`
-- ----------------------------
DROP TABLE IF EXISTS `datatable`;
CREATE TABLE `datatable` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL,
  `DATABASE_ID` int(11) NOT NULL,
  `NAME` varchar(100) default NULL,
  `TABLE_SQL` text,
  `TABLE_TYPE` int(11) NOT NULL,
  `MEMO` varchar(1024) default NULL COMMENT '数据表描述',
  `DATE_TYPE` int(11) NOT NULL COMMENT '日期类型',
  `DATE_FIELD` varchar(50) NOT NULL COMMENT '日期字段',
  `DATE_FORMAT` varchar(50) NOT NULL,
  `TIME_INTERVAL` int(11) default NULL,
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8494 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of datatable
-- ----------------------------

-- ----------------------------
-- Table structure for `datatable_r`
-- ----------------------------
DROP TABLE IF EXISTS `datatable_r`;
CREATE TABLE `datatable_r` (
  `ID` int(11) NOT NULL auto_increment,
  `DATATABLE_ID` int(11) default NULL,
  `HOUR_TABLE` int(11) default NULL,
  `DAY_TABLE` int(11) default NULL,
  `WEEK_TABLE` int(11) default NULL,
  `MONTH_TABLE` int(11) default NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of datatable_r
-- ----------------------------

-- ----------------------------
-- Table structure for `feedback`
-- ----------------------------
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE `feedback` (
  `ID` int(11) NOT NULL auto_increment,
  `PUSH_ID` int(11) default NULL,
  `FROM_USER` varchar(20) default NULL,
  `TO_USERS` text,
  `CONTENT` text,
  `CREATE_TIME` varchar(40) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of feedback
-- ----------------------------

-- ----------------------------
-- Table structure for `notice`
-- ----------------------------
DROP TABLE IF EXISTS `notice`;
CREATE TABLE `notice` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名',
  `TITLE` varchar(100) NOT NULL COMMENT '公告标题',
  `CONTENT` text NOT NULL COMMENT '公告内容',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notice
-- ----------------------------

-- ----------------------------
-- Table structure for `notification`
-- ----------------------------
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `ID` int(11) NOT NULL auto_increment,
  `PUSH_ID` int(11) NOT NULL,
  `PUSH_NAME` varchar(20) NOT NULL,
  `PUSH_DATE` varchar(15) NOT NULL,
  `CONTENT` text,
  `STATUS` int(1) NOT NULL default '1' COMMENT '1:生效,0:失效',
  `CREAT_TIME` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notification
-- ----------------------------

-- ----------------------------
-- Table structure for `page`
-- ----------------------------
DROP TABLE IF EXISTS `page`;
CREATE TABLE `page` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `PARENT_ID` int(11) NOT NULL COMMENT '父页面ID，默认为0',
  `NAME` varchar(100) NOT NULL,
  `TYPE` int(11) NOT NULL COMMENT '概览页1，详情页2',
  `SORT` int(11) NOT NULL COMMENT '排序',
  `IS_FILTER` int(11) NOT NULL,
  `IS_PUBLISHED` int(11) NOT NULL default '0',
  `MMDATA_ID` int(11) default NULL,
  `MEMO` varchar(1024) default NULL,
  `URL` varchar(1024) default NULL,
  `PV` int(11) NOT NULL default '0',
  `UV` int(11) NOT NULL default '0',
  `IS_HOT` int(11) NOT NULL default '0',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  `UPDATE_STAFF` char(10) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '修改时间',
  `APPROVE_USER` varchar(50) default '' COMMENT '产品负责人',
  `DEVELOP_USER` varchar(50) default NULL COMMENT '开发负责人',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11067 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page
-- ----------------------------

-- ----------------------------
-- Table structure for `page_analyse`
-- ----------------------------
DROP TABLE IF EXISTS `page_analyse`;
CREATE TABLE `page_analyse` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `NAME` varchar(100) default NULL,
  `URL` varchar(1024) default NULL,
  `COST_TIME` float default NULL,
  `MSG` varchar(50) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=11053 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_analyse
-- ----------------------------

-- ----------------------------
-- Table structure for `page_filter`
-- ----------------------------
DROP TABLE IF EXISTS `page_filter`;
CREATE TABLE `page_filter` (
  `ID` int(11) NOT NULL auto_increment,
  `PAGE_ID` int(11) NOT NULL COMMENT '页面ID',
  `DIMENSION_ID` int(11) NOT NULL COMMENT '维度指标ID',
  `TYPE` int(11) NOT NULL COMMENT '筛选类型',
  `DEFAULT_VALUE` varchar(512) NOT NULL,
  `SORT` int(11) NOT NULL COMMENT '排序',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=19953 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_filter
-- ----------------------------

-- ----------------------------
-- Table structure for `page_panel`
-- ----------------------------
DROP TABLE IF EXISTS `page_panel`;
CREATE TABLE `page_panel` (
  `ID` int(11) NOT NULL auto_increment,
  `PAGE_ID` int(11) NOT NULL COMMENT '页面ID',
  `TITLE` varchar(100) NOT NULL COMMENT '标题',
  `TITLE_ENABLED` int(11) NOT NULL default '0' COMMENT '标题是否启用',
  `TAB_NUM` int(11) NOT NULL default '0' COMMENT '0则不启用，最多6个',
  `TAB_NAME` varchar(300) default NULL COMMENT '多个以逗号隔开',
  `DETAIL_ENABLED` int(11) NOT NULL default '0' COMMENT '详情链接是否启用',
  `DETAIL_PAGE` int(11) default NULL,
  `DETAIL_OPEN_TYPE` int(11) default NULL,
  `MEMO_ENABLED` int(11) default '0',
  `MEMO` varchar(300) NOT NULL,
  `WIDTH` int(11) default NULL,
  `HEIGHT` int(11) default NULL,
  `ROW_NUM` int(11) default NULL,
  `SORT` int(11) default NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '修改时间',
  PRIMARY KEY  (`ID`),
  KEY `page_id_index` (`PAGE_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=9589 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_panel
-- ----------------------------

-- ----------------------------
-- Table structure for `page_panel_widget`
-- ----------------------------
DROP TABLE IF EXISTS `page_panel_widget`;
CREATE TABLE `page_panel_widget` (
  `ID` int(11) NOT NULL auto_increment,
  `PANEL_ID` int(11) NOT NULL,
  `TAB_INDEX` int(11) NOT NULL COMMENT '即控件在第几个TAB；没有TAB，则为0',
  `TITLE` varchar(100) NOT NULL,
  `TITLE_ENABLED` int(11) NOT NULL COMMENT '标题是否启用，默认为1：启用',
  `MEMO_ENABLED` int(11) NOT NULL,
  `MEMO` varchar(300) default NULL,
  `WIDTH` int(11) NOT NULL,
  `HEIGHT` int(11) NOT NULL,
  `ROW_NUM` int(11) NOT NULL,
  `SORT` int(11) NOT NULL,
  `WIDGET_TYPE` int(11) NOT NULL,
  `DATE_TYPE` int(11) NOT NULL default '1',
  `ACCESS_MODE` int(11) NOT NULL,
  `CONFIG` text COMMENT 'json对象',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '修改时间',
  `PAGE_ID` int(11) default '0',
  `enabled` int(1) default '1',
  PRIMARY KEY  (`ID`),
  KEY `panel_id_index` (`PANEL_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8887 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_panel_widget
-- ----------------------------

-- ----------------------------
-- Table structure for `page_panel_widget_index`
-- ----------------------------
DROP TABLE IF EXISTS `page_panel_widget_index`;
CREATE TABLE `page_panel_widget_index` (
  `ID` int(11) NOT NULL auto_increment,
  `PARENT_ID` int(11) NOT NULL,
  `WIDGET_ID` int(11) NOT NULL,
  `AXIS_TYPE` int(11) NOT NULL COMMENT 'X轴，Y轴',
  `AXIS_INDEX` int(11) NOT NULL COMMENT '用于双坐标轴，默认为0',
  `INDEX_TYPE` int(11) NOT NULL COMMENT '数据指标，维度指标',
  `INDEX_ID` int(11) NOT NULL,
  `DIMENSION_VALUE` text,
  `CONFIG` varchar(1024) default NULL,
  `IS_DISPLAY` int(11) NOT NULL default '1',
  `SORT` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  PRIMARY KEY  (`ID`),
  KEY `widget_id_index` (`WIDGET_ID`),
  KEY `widget_index_id_index` (`INDEX_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=94572 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_panel_widget_index
-- ----------------------------

-- ----------------------------
-- Table structure for `page_role`
-- ----------------------------
DROP TABLE IF EXISTS `page_role`;
CREATE TABLE `page_role` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `NAME` varchar(100) NOT NULL,
  `TYPE` int(11) NOT NULL default '1' COMMENT '1普通用户；2目录管理员',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_role
-- ----------------------------

-- ----------------------------
-- Table structure for `page_role_auth`
-- ----------------------------
DROP TABLE IF EXISTS `page_role_auth`;
CREATE TABLE `page_role_auth` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL,
  `ROLE_ID` int(11) NOT NULL,
  `PAGE_ID` int(11) NOT NULL,
  `IS_DOCUMENT_AUTH` int(11) NOT NULL default '0',
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=62686 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_role_auth
-- ----------------------------

-- ----------------------------
-- Table structure for `page_role_r_staff`
-- ----------------------------
DROP TABLE IF EXISTS `page_role_r_staff`;
CREATE TABLE `page_role_r_staff` (
  `ID` int(11) NOT NULL auto_increment,
  `ROLE_ID` int(11) NOT NULL,
  `STAFF_ID` int(11) default NULL COMMENT 'STAFF ID OR DEPARTMENT ID',
  `STAFF_NAME` varchar(100) NOT NULL,
  `TYPE` varchar(20) default NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10188 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of page_role_r_staff
-- ----------------------------

-- ----------------------------
-- Table structure for `portal_log`
-- ----------------------------
DROP TABLE IF EXISTS `portal_log`;
CREATE TABLE `portal_log` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名',
  `STAFF_ID` int(11) NOT NULL,
  `STAFF_NAME` varchar(100) NOT NULL,
  `TYPE` int(11) NOT NULL,
  `CONTENT` varchar(500) NOT NULL,
  `EXTEND1` varchar(500) default NULL,
  `EXTEND2` varchar(500) default NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of portal_log
-- ----------------------------

-- ----------------------------
-- Table structure for `power_users`
-- ----------------------------
DROP TABLE IF EXISTS `power_users`;
CREATE TABLE `power_users` (
  `ID` int(11) NOT NULL auto_increment,
  `USER_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `AUTH_TYPE` tinyint(2) NOT NULL default '1' COMMENT '1页面权限, 2目录权限, 3门户权限',
  `PORTAL_NAME` varchar(20) NOT NULL default '',
  `PAGE_ID` int(11) NOT NULL default '0',
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '更新时间',
  `END_TIME` timestamp NOT NULL default '0000-00-00 00:00:00' COMMENT '结束时间',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of power_users
-- ----------------------------

-- ----------------------------
-- Table structure for `private_table_log`
-- ----------------------------
DROP TABLE IF EXISTS `private_table_log`;
CREATE TABLE `private_table_log` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(100) NOT NULL,
  `USER_NAME` varchar(100) NOT NULL,
  `DB_ID` int(11) NOT NULL,
  `PAGE_ID` int(11) default NULL,
  `DATA_SQL` text,
  `TABLE_NAMES` text NOT NULL,
  `CREATE_TIME` timestamp NULL default NULL on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of private_table_log
-- ----------------------------

-- ----------------------------
-- Table structure for `push_config`
-- ----------------------------
DROP TABLE IF EXISTS `push_config`;
CREATE TABLE `push_config` (
  `ID` int(11) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(20) NOT NULL,
  `TITLE` varchar(50) NOT NULL,
  `IS_WX` int(1) NOT NULL default '0',
  `IS_MAIL` int(1) NOT NULL default '0',
  `EDITORS` text NOT NULL,
  `TOS` text NOT NULL,
  `TO_WEIXIN` text,
  `TO_MAIL` text,
  `MAIL_CC` text,
  `MAIL_BCC` text,
  `CREATOR` varchar(20) NOT NULL,
  `REMINDER_ID` int(11) NOT NULL COMMENT '时间周期crontab配置ID',
  `PAGE_ID` int(11) NOT NULL default '0',
  `PERIOD` varchar(5) NOT NULL default 'd',
  `DAYS` int(1) NOT NULL default '0',
  `HOURS` int(2) NOT NULL default '0',
  `MINUTES` int(2) default '0',
  `MEMO` text,
  `FOOTER` text,
  `ALL_ACCESS` int(1) default '1',
  `IS_CUSTOMED` int(1) NOT NULL default '0',
  `OFFSET_TIME` int(5) default NULL,
  `DURING_TIME` int(5) default NULL,
  `VALIDATE_DATA` int(1) default '0',
  `MARK` int(1) NOT NULL default '0',
  `NEED_CONFIRM` int(1) NOT NULL default '0',
  `ENABLED` int(1) NOT NULL default '1',
  `IS_TITLE_TIME` int(1) default '1',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=198 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of push_config
-- ----------------------------

-- ----------------------------
-- Table structure for `reminder_config`
-- ----------------------------
DROP TABLE IF EXISTS `reminder_config`;
CREATE TABLE `reminder_config` (
  `ID` int(11) NOT NULL auto_increment COMMENT 'id',
  `SYSTEM_NAME` varchar(50) NOT NULL COMMENT '系统名',
  `CRONTAB` varchar(30) NOT NULL COMMENT 'cronta的时间格式',
  `SCRIPT` varchar(200) NOT NULL COMMENT '执行脚本路径',
  `ACTIVED` int(1) NOT NULL default '1' COMMENT '是否激活（1： 是， 0： 否，默认是）',
  `CREATOR` varchar(20) NOT NULL COMMENT '创建者',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=208 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of reminder_config
-- ----------------------------

-- ----------------------------
-- Table structure for `reminder_log`
-- ----------------------------
DROP TABLE IF EXISTS `reminder_log`;
CREATE TABLE `reminder_log` (
  `ID` int(11) NOT NULL auto_increment,
  `PUSH_ID` int(11) default NULL,
  `USER_NAME` varchar(20) default NULL,
  `CREATE_TIME` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `PUSH_TYPE` int(2) default NULL,
  `PUSH_WAY` int(2) default NULL,
  `STATUS` int(2) default NULL,
  `MSG` varchar(1000) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of reminder_log
-- ----------------------------

-- ----------------------------
-- Table structure for `sys_log`
-- ----------------------------
DROP TABLE IF EXISTS `sys_log`;
CREATE TABLE `sys_log` (
  `ID` bigint(20) NOT NULL auto_increment,
  `PORTAL_NAME` varchar(50) default NULL COMMENT '门户英文名，唯一',
  `OPERATOR_CONTENT` varchar(512) NOT NULL,
  `PARAMS` varchar(1000) default NULL,
  `OPERATOR_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_log
-- ----------------------------

-- ----------------------------
-- Table structure for `sys_portal`
-- ----------------------------
DROP TABLE IF EXISTS `sys_portal`;
CREATE TABLE `sys_portal` (
  `ID` int(11) NOT NULL auto_increment COMMENT '门户ID',
  `NAME` varchar(50) default NULL COMMENT '门户名称',
  `PORTAL_NAME` varchar(50) default NULL COMMENT '门户英文名，唯一',
  `LOGO_TYPE` varchar(10) default NULL COMMENT '门户LOGO图片类型',
  `PORTAL_TYPE` int(11) default NULL,
  `CUSTOM_URL` varchar(50) default NULL COMMENT '个性域名',
  `IS_PUBLISHED` int(11) default NULL COMMENT '是否发布',
  `ADMIN` text COMMENT '后台管理员',
  `ADMIN_DEVELOP` varchar(500) default NULL,
  `ADMIN_PRODUCT` varchar(500) default NULL,
  `BG` int(11) default NULL COMMENT 'BG的ID',
  `DEPARTMENT` int(11) default NULL COMMENT '部门',
  `DEPARTMENT_NAME` varchar(100) default NULL,
  `IS_DELETED` int(11) default NULL COMMENT '是否删除',
  `CREATE_STAFF` int(11) default NULL,
  `CREATE_TIME` timestamp NULL default '0000-00-00 00:00:00' COMMENT '创建时间',
  `UPDATE_STAFF` int(11) default NULL,
  `UPDATE_TIME` timestamp NULL default '0000-00-00 00:00:00' COMMENT '修改时间',
  `PRIVATE_TYPE` tinyint(2) default '0',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=329 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_portal
-- ----------------------------

-- ----------------------------
-- Table structure for `tbl_log`
-- ----------------------------
DROP TABLE IF EXISTS `tbl_log`;
CREATE TABLE `tbl_log` (
  `tbl_id` int(12) NOT NULL default '0',
  `tbl_sql_old` text,
  `tbl_sql_new` text,
  `status` tinyint(5) default '0',
  `error_log` text,
  PRIMARY KEY  (`tbl_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tbl_log
-- ----------------------------

-- ----------------------------
-- Table structure for `tmp_db_config`
-- ----------------------------
DROP TABLE IF EXISTS `tmp_db_config`;
CREATE TABLE `tmp_db_config` (
  `ID` int(11) NOT NULL default '0',
  `PORTAL_NAME` varchar(50) NOT NULL COMMENT '门户英文名，唯一',
  `NAME` varchar(100) NOT NULL,
  `ALIAS` varchar(100) NOT NULL,
  `DRIVER` varchar(50) NOT NULL,
  `DATA_CHARACTER` varchar(50) default NULL,
  `URL` varchar(512) NOT NULL,
  `USERNAME` varchar(50) NOT NULL,
  `PORT` int(10) NOT NULL default '3306',
  `PASSWORD` varchar(50) NOT NULL,
  `MEMO` varchar(1000) default NULL COMMENT '数据源描述',
  `IS_DELETED` int(11) NOT NULL,
  `CREATE_STAFF` int(11) NOT NULL,
  `CREATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00',
  `UPDATE_STAFF` int(11) NOT NULL,
  `UPDATE_TIME` timestamp NOT NULL default '0000-00-00 00:00:00'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tmp_db_config
-- ----------------------------
