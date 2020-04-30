/*
Navicat MySQL Data Transfer

Source Server         : qa_all
Source Server Version : 50632
Source Host           : 172.17.0.203:3306
Source Database       : qa_user

Target Server Type    : MYSQL
Target Server Version : 50632
File Encoding         : 65001

Date: 2020-04-30 17:53:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for api_job
-- ----------------------------
DROP TABLE IF EXISTS `api_job`;
CREATE TABLE `api_job` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_api_job_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of api_job
-- ----------------------------

-- ----------------------------
-- Table structure for Dept
-- ----------------------------
DROP TABLE IF EXISTS `Dept`;
CREATE TABLE `Dept` (
  `deptId` int(11) NOT NULL AUTO_INCREMENT,
  `deptName` varchar(100) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`deptId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of Dept
-- ----------------------------
INSERT INTO `Dept` VALUES ('1', '其他', '1');
INSERT INTO `Dept` VALUES ('2', '流量课组', '1');
INSERT INTO `Dept` VALUES ('3', 'CRM组', '1');
INSERT INTO `Dept` VALUES ('4', '基础课组', '1');
INSERT INTO `Dept` VALUES ('5', '销售组', '1');
INSERT INTO `Dept` VALUES ('6', '班课组', '1');
INSERT INTO `Dept` VALUES ('7', '自动化测试组', '1');

-- ----------------------------
-- Table structure for Manager
-- ----------------------------
DROP TABLE IF EXISTS `Manager`;
CREATE TABLE `Manager` (
  `userId` int(10) NOT NULL,
  `userName` varchar(100) DEFAULT NULL,
  `deptId` int(11) DEFAULT NULL,
  `passwd` varchar(100) NOT NULL,
  PRIMARY KEY (`userId`),
  KEY `deptId` (`deptId`),
  CONSTRAINT `Manager_ibfk_1` FOREIGN KEY (`deptId`) REFERENCES `Dept` (`deptId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of Manager
-- ----------------------------
INSERT INTO `Manager` VALUES ('1', 'admin', '1', 'admin');

-- ----------------------------
-- Table structure for Project
-- ----------------------------
DROP TABLE IF EXISTS `Project`;
CREATE TABLE `Project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` varchar(100) DEFAULT NULL,
  `deptId` int(11) DEFAULT NULL,
  `detail` text,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `deptId` (`deptId`),
  CONSTRAINT `Project_ibfk_1` FOREIGN KEY (`deptId`) REFERENCES `Dept` (`deptId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of Project
-- ----------------------------
INSERT INTO `Project` VALUES ('1', '项目', '1', 'desc', '1');

-- ----------------------------
-- Table structure for SystemMessage
-- ----------------------------
DROP TABLE IF EXISTS `SystemMessage`;
CREATE TABLE `SystemMessage` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `createDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  `fromUser` varchar(100) DEFAULT NULL COMMENT '来源用户',
  `toUser` varchar(100) NOT NULL COMMENT '推送用户',
  `msg` text COMMENT '推送消息',
  `params` varchar(200) DEFAULT NULL COMMENT '推送参数',
  `func` varchar(100) DEFAULT NULL COMMENT '使用方法',
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '消息状态：0 未审核 1已审核；2已拒绝;3已阅读',
  `userId` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of SystemMessage
-- ----------------------------
INSERT INTO `SystemMessage` VALUES ('30', '2020-01-03 13:22:15', 'admin', 'guohongjie', '已同意guohongjie更换至:其他', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"自动化测试组\", \"updateDept\": \"其他\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('31', '2020-01-03 13:22:53', 'admin', 'guohongjie', '已同意guohongjie更换至:自动化测试组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"其他\", \"updateDept\": \"自动化测试组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('32', '2020-01-03 16:07:31', 'admin', 'liushuang', '已同意liushuang更换至:CRM组', '{\"urlName\": \"static/userImg/liushuang.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '392');
INSERT INTO `SystemMessage` VALUES ('33', '2020-01-03 14:00:24', 'admin', 'jiayujiao', '已同意jiayujiao更换至:基础课组', '{\"urlName\": \"static/userImg/jiayujiao.png\", \"nowDept\": \"其他\", \"updateDept\": \"基础课组\"}', 'uploadDept', '3', '512');
INSERT INTO `SystemMessage` VALUES ('34', '2020-01-03 14:17:27', 'admin', 'liangguoqing', '已同意liangguoqing更换至:CRM组', '{\"urlName\": \"static/userImg/liangguoqing.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '612');
INSERT INTO `SystemMessage` VALUES ('35', '2020-01-03 14:17:31', 'admin', 'liangguoqing', '已同意liangguoqing更换至:CRM组', '{\"urlName\": \"static/userImg/liangguoqing.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '612');
INSERT INTO `SystemMessage` VALUES ('36', '2020-01-03 14:17:34', 'admin', 'liangguoqing', '已同意liangguoqing更换至:CRM组', '{\"urlName\": \"static/userImg/liangguoqing.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '612');
INSERT INTO `SystemMessage` VALUES ('37', '2020-01-03 16:08:12', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('38', '2020-01-03 16:08:32', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('39', '2020-01-08 09:36:29', 'admin', 'xuhongying', '已同意xuhongying更换至:班课组', '{\"urlName\": \"static/userImg/xuhongying.png\", \"nowDept\": \"其他\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '419');
INSERT INTO `SystemMessage` VALUES ('40', '2020-01-08 09:36:31', 'admin', 'xuhongying', '已同意xuhongying更换至:班课组', '{\"urlName\": \"static/userImg/xuhongying.png\", \"nowDept\": \"其他\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '419');
INSERT INTO `SystemMessage` VALUES ('41', '2020-01-08 09:36:34', 'admin', 'xuhongying', '已同意xuhongying更换至:班课组', '{\"urlName\": \"static/userImg/xuhongying.png\", \"nowDept\": \"班课组\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '419');
INSERT INTO `SystemMessage` VALUES ('42', '2020-01-03 16:05:34', 'admin', 'hongchen', '已同意hongchen更换至:销售组', '{\"urlName\": \"static/userImg/hongchen.png\", \"nowDept\": \"其他\", \"updateDept\": \"销售组\"}', 'uploadDept', '1', '240');
INSERT INTO `SystemMessage` VALUES ('43', '2020-01-03 16:08:34', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('44', '2020-01-03 16:08:37', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('45', '2020-01-03 16:08:42', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('46', '2020-01-03 16:08:40', 'admin', 'tianningxue', '已同意tianningxue更换至:CRM组', '{\"urlName\": \"static/userImg/tianningxue.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '270');
INSERT INTO `SystemMessage` VALUES ('47', '2020-01-14 16:23:42', 'admin', 'guohongjie', '已同意guohongjie更换至:班课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"自动化测试组\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('48', '2020-01-15 13:27:39', 'admin', 'guohongjie', '已同意guohongjie更换至:销售组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"班课组\", \"updateDept\": \"销售组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('49', '2020-01-15 13:27:41', 'admin', 'guohongjie', '已同意guohongjie更换至:基础课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"销售组\", \"updateDept\": \"基础课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('50', '2020-01-15 14:47:29', 'admin', 'guohongjie', '已同意guohongjie更换至:CRM组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"基础课组\", \"updateDept\": \"CRM组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('51', '2020-01-15 18:27:46', 'admin', 'guohongjie', '已同意guohongjie更换至:流量课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"CRM组\", \"updateDept\": \"流量课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('52', '2020-01-15 18:27:48', 'admin', 'guohongjie', '已同意guohongjie更换至:基础课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"流量课组\", \"updateDept\": \"基础课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('53', '2020-01-16 16:55:54', 'admin', 'guohongjie', '已同意guohongjie更换至:班课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"基础课组\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('54', '2020-01-16 16:55:56', 'admin', 'guohongjie', '已同意guohongjie更换至:销售组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"班课组\", \"updateDept\": \"销售组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('55', '2020-01-16 16:12:00', 'admin', 'litonglin', '已同意litonglin更换至:CRM组', '{\"urlName\": \"static/userImg/litonglin.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '239');
INSERT INTO `SystemMessage` VALUES ('56', '2020-01-16 16:46:54', 'admin', 'litonglin', '已同意litonglin更换至:CRM组', '{\"urlName\": \"static/userImg/litonglin.png\", \"nowDept\": \"CRM组\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '239');
INSERT INTO `SystemMessage` VALUES ('57', '2020-03-03 14:34:47', 'admin', 'guohongjie', '已同意guohongjie更换至:流量课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"销售组\", \"updateDept\": \"流量课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('58', '2020-01-17 14:41:23', 'admin', 'litonglin', '已同意litonglin更换至:CRM组', '{\"urlName\": \"static/userImg/litonglin.png\", \"nowDept\": \"CRM组\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '239');
INSERT INTO `SystemMessage` VALUES ('59', '2020-02-04 14:44:24', 'admin', 'wuyang', '已同意wuyang更换至:CRM组', '{\"urlName\": \"static/userImg/wuyang.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '645');
INSERT INTO `SystemMessage` VALUES ('60', '2020-02-04 14:44:27', 'admin', 'wuyang', '已同意wuyang更换至:CRM组', '{\"urlName\": \"static/userImg/wuyang.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '645');
INSERT INTO `SystemMessage` VALUES ('61', '2020-03-03 14:34:49', 'admin', 'guohongjie', '已同意guohongjie更换至:自动化测试组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"流量课组\", \"updateDept\": \"自动化测试组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('62', '2020-04-11 17:41:43', 'admin', 'guohongjie', '已同意guohongjie更换至:班课组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"自动化测试组\", \"updateDept\": \"班课组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('63', '2020-04-11 17:41:46', 'admin', 'guohongjie', '已同意guohongjie更换至:自动化测试组', '{\"urlName\": \"static/userImg/guohongjie.png\", \"nowDept\": \"班课组\", \"updateDept\": \"自动化测试组\"}', 'uploadDept', '3', '274');
INSERT INTO `SystemMessage` VALUES ('64', '2020-04-23 14:54:25', 'admin', 'yangmengting', '已同意yangmengting更换至:CRM组', '{\"urlName\": \"static/userImg/yangmengting.png\", \"nowDept\": \"其他\", \"updateDept\": \"CRM组\"}', 'uploadDept', '1', '680');
INSERT INTO `SystemMessage` VALUES ('65', '2020-04-24 17:15:28', 'admin', 'libin', '已同意libin更换至:班课组', '{\"urlName\": \"static/userImg/libin.png\", \"nowDept\": \"其他\", \"updateDept\": \"班课组\"}', 'uploadDept', '1', '231');
INSERT INTO `SystemMessage` VALUES ('66', '2020-04-24 17:26:17', 'admin', 'lichaochao', '已同意lichaochao更换至:班课组', '{\"urlName\": \"static/userImg/lichaochao.png\", \"nowDept\": \"其他\", \"updateDept\": \"班课组\"}', 'uploadDept', '1', '251');

-- ----------------------------
-- Table structure for User
-- ----------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `userId` int(10) NOT NULL DEFAULT '0',
  `userName` varchar(100) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  `deptId` int(11) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `imgUrl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `deptId` (`deptId`),
  CONSTRAINT `User_ibfk_1` FOREIGN KEY (`deptId`) REFERENCES `Dept` (`deptId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of User
-- ----------------------------
INSERT INTO `User` VALUES ('231', 'libin', '1', '6', '15210761699', 'libin@yunshuxie.com', 'static/userImg/libin.png');
INSERT INTO `User` VALUES ('239', 'litonglin', '1', '3', '15313349725', 'litonglin@yunshuxie.com', 'static/userImg/litonglin.png');
INSERT INTO `User` VALUES ('240', 'hongchen', '1', '5', '18010136420', 'hongchen@yunshuxie.com', 'static/userImg/hongchen.png');
INSERT INTO `User` VALUES ('250', 'zhangyu', '1', '1', '17600749128', 'zhangyu@yunshuxie.com', null);
INSERT INTO `User` VALUES ('251', 'lichaochao', '1', '6', '18811063258', 'lichaochao@yunshuxie.com', 'static/userImg/lichaochao.png');
INSERT INTO `User` VALUES ('266', 'pengjunxia', '1', '2', '18518274036', 'pengjunxia@yunshuxie.com', 'static/userImg/pengjunxia.png');
INSERT INTO `User` VALUES ('270', 'tianningxue', '1', '3', '17600053698', 'tianningxue@yunshuxie.com', 'static/userImg/tianningxue.png');
INSERT INTO `User` VALUES ('274', 'guohongjie', '1', '7', '18519118952', 'guohongjie@yunshuxie.com', 'static/userImg/guohongjie.png');
INSERT INTO `User` VALUES ('385', 'renhuihui', '1', '7', '13466710714', 'renhuihui@yunshuxie.com', 'static/userImg/renhuihui.png');
INSERT INTO `User` VALUES ('392', 'liushuang', '1', '3', '18811566306', 'liushuang@yunshuxie.com', 'static/userImg/liushuang.png');
INSERT INTO `User` VALUES ('419', 'xuhongying', '1', '6', '15910632119', 'xuhongying@yunshuxie.com', 'static/userImg/xuhongying.png');
INSERT INTO `User` VALUES ('510', 'panze', '1', '6', '15810346836', 'panze@yunshuxie.com', 'static/userImg/panze.png');
INSERT INTO `User` VALUES ('512', 'jiayujiao', '1', '4', '18810140570', 'jiayujiao@yunshuxie.com', 'static/userImg/jiayujiao.png');
INSERT INTO `User` VALUES ('612', 'liangguoqing', '1', '3', '15811460708', 'liangguoqing@yunshuxie.com', 'static/userImg/liangguoqing.png');
INSERT INTO `User` VALUES ('613', 'huyanfeng', '1', '4', '18322550511', 'huyanfeng@yunshuxie.com', 'static/userImg/huyanfeng.png');
INSERT INTO `User` VALUES ('645', 'wuyang', '1', '3', '17621846810', 'wuyang@yunshuxie.com', 'static/userImg/wuyang.png');
INSERT INTO `User` VALUES ('680', 'yangmengting', '1', '3', '18370006614', 'yangmengting@yunshuxie.com', 'static/userImg/yangmengting.png');
