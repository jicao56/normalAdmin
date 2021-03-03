CREATE DATABASE `normal_admin` CHARACTER SET utf8 COLLATE utf8_general_ci;

use normal_admin;

/*
 Navicat Premium Data Transfer

 Source Server         : 本地虚拟机数据库
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : 192.168.45.138:3306
 Source Schema         : normal_admin

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 03/03/2021 09:40:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_account
-- ----------------------------
DROP TABLE IF EXISTS `t_account`;
CREATE TABLE `t_account`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '账号ID',
  `user_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '用户ID',
  `open_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '登录账号,如手机号/邮箱/自定义账号等',
  `category` tinyint(1) NOT NULL DEFAULT 1 COMMENT '账号类别，1-手机号；2-邮箱；3-自定义账号',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '账号状态',
  INDEX `user_id`(`user_id`) USING BTREE COMMENT '用户id'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '账号表。系统中，会有各种各样的登录方式，如手机号、邮箱地址、身份证号码和微信登录等。因此该表主要是用来记录每一种登录方式的信息，但不包含密码信息，因为各种登录方式都会使用同一个密码。每一条记录都会关联到唯一的一条用户记录' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_account
-- ----------------------------
INSERT INTO `t_account` VALUES (1, 1, 'root', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_element
-- ----------------------------
DROP TABLE IF EXISTS `t_element`;
CREATE TABLE `t_element`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '页面元素ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '页面元素唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '页面元素名称',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '页面元素介绍',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '页面元素状态',
  INDEX `code`(`code`) USING BTREE COMMENT '页面元素CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '页面元素表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_element
-- ----------------------------

-- ----------------------------
-- Table structure for t_element_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_element_permission`;
CREATE TABLE `t_element_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `element_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '页面元素ID',
  `permission_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '权限ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '菜单权限状态',
  INDEX `element_id`(`element_id`) USING BTREE COMMENT '页面元素ID',
  INDEX `permission_id`(`permission_id`) USING BTREE COMMENT '权限ID'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '页面元素权限表。\r\n用来定义哪个权限对该页面元素可见（一对一）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_element_permission
-- ----------------------------

-- ----------------------------
-- Table structure for t_file
-- ----------------------------
DROP TABLE IF EXISTS `t_file`;
CREATE TABLE `t_file`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '文件ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '文件唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '文件名称',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '文件介绍',
  `uri` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '文件uri',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '文件状态',
  INDEX `code`(`code`) USING BTREE COMMENT '文件CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '文件表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_file
-- ----------------------------

-- ----------------------------
-- Table structure for t_file_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_file_permission`;
CREATE TABLE `t_file_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `file_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '文件ID',
  `permission_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '权限ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '菜单权限状态',
  INDEX `file_id`(`file_id`) USING BTREE COMMENT '文件ID',
  INDEX `permission_id`(`permission_id`) USING BTREE COMMENT '权限ID'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '文件权限表。\r\n用来定义文件的权限（一对一）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_file_permission
-- ----------------------------

-- ----------------------------
-- Table structure for t_group
-- ----------------------------
DROP TABLE IF EXISTS `t_group`;
CREATE TABLE `t_group`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `pid` bigint(20) NOT NULL DEFAULT 0 COMMENT '所属父级用户组ID',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户组名称',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户组CODE唯一代码',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户组介绍',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '用户组状态',
  INDEX `pid`(`pid`) USING BTREE COMMENT '父级用户组ID',
  INDEX `code`(`code`) USING BTREE COMMENT '用户组CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户组表。\r\n虽然增加了角色表（role）后，把数据量从 100 亿降低至 10 亿，但 10 倍的数据量依然还是很多。而且大部分的用户（主体用户。如学生系统，学生就是主体）都会分配相同的角色组。用户组和角色组的区别：\r\n\r\n角色组（role）：解决的是权限的分组，减少了权限的重复分配\r\n用户组（user_group）：解决的是用户的分组，减少了用户的重复授权\r\n' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_group
-- ----------------------------
INSERT INTO `t_group` VALUES (1, 0, 'root', 'GROUP_SUPER_MANAGER', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_group_role
-- ----------------------------
DROP TABLE IF EXISTS `t_group_role`;
CREATE TABLE `t_group_role`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `group_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '用户组ID',
  `role_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '角色ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '用户组角色状态',
  INDEX `user_group_id`(`group_id`) USING BTREE COMMENT '用户组ID',
  INDEX `role_id`(`role_id`) USING BTREE COMMENT '角色ID'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户组角色表。\r\n每个系统主体用户，基本都占用了所有用户的 90% 以上（既包含用户，又包含商家的系统，用户和商家同时都是主题用户）。因此，每个用户注册时，基本只需要分配一条所属的用户组，即可完成角色权限的配置。这样处理后，数据量将从 10 亿下降至 1 亿多。同时也减少了用户注册时的需批量写入数量。' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_group_role
-- ----------------------------
INSERT INTO `t_group_role` VALUES (1, 1, 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_menu
-- ----------------------------
DROP TABLE IF EXISTS `t_menu`;
CREATE TABLE `t_menu`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `pid` bigint(20) NOT NULL DEFAULT 0 COMMENT '所属父级菜单ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '菜单唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '菜单名称',
  `uri` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '菜单uri',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '菜单介绍',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '菜单状态',
  INDEX `pid`(`pid`) USING BTREE COMMENT '父级菜单ID',
  INDEX `code`(`code`) USING BTREE COMMENT '菜单CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_menu
-- ----------------------------
INSERT INTO `t_menu` VALUES (1, 0, 'HOME', '主页', '', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (2, 0, 'SETTING', '设置', '', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (3, 2, 'MENU_MANAGE', '菜单管理', '/setting/menu', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (4, 2, 'OPERATION_MANAGE', '操作管理', '/setting/operation', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (5, 2, 'USER_MANAGE', '用户管理', '/setting/user', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (6, 2, 'GROUP_MANAGE', '用户组管理', '/setting/group', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (7, 2, 'ROLE_MANAGE', '角色管理', '/setting/role', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu` VALUES (8, 2, 'PERMISSION_MANAGE', '权限管理', '/setting/permission', '', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_menu_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_menu_permission`;
CREATE TABLE `t_menu_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `menu_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '菜单ID',
  `permission_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '权限ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '菜单权限状态',
  INDEX `menu_id`(`menu_id`) USING BTREE COMMENT '菜单ID',
  INDEX `permission_id`(`permission_id`) USING BTREE COMMENT '权限ID'
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单权限表。\r\n用来定义每个菜单对应哪个权限（一对一）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_menu_permission
-- ----------------------------
INSERT INTO `t_menu_permission` VALUES (1, 1, 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (2, 2, 2, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (3, 3, 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (4, 4, 4, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (5, 5, 5, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (6, 6, 6, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (7, 7, 7, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_menu_permission` VALUES (8, 8, 8, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_operation
-- ----------------------------
DROP TABLE IF EXISTS `t_operation`;
CREATE TABLE `t_operation`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '功能操作ID',
  `pid` bigint(20) NOT NULL DEFAULT 0 COMMENT '功能操作父操作ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '功能操作唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '功能操作名称',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '功能操作介绍',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '功能操作状态',
  INDEX `code`(`code`) USING BTREE COMMENT '功能操作CODE代码',
  INDEX `pid`(`pid`) USING BTREE COMMENT '功能操作父操作ID'
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '功能操作表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_operation
-- ----------------------------
INSERT INTO `t_operation` VALUES (1, 0, 'OPERATION_MENU_ADD', '添加菜单', '[添加菜单]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (2, 0, 'OPERATION_MENU_EDIT', '修改菜单', '[修改菜单]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (3, 0, 'OPERATION_MENU_DEL', '删除菜单', '[删除菜单]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (4, 0, 'OPERATION_MENU_DISABLE', '禁用菜单', '[禁用菜单]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (5, 0, 'OPERATION_MENU_ENABLE', '启用菜单', '[启用菜单]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (6, 0, 'OPERATION_PERMISSION_VIEW', '查看权限', '[查看权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (7, 0, 'OPERATION_PERMISSION_ADD', '添加权限', '[添加权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (8, 0, 'OPERATION_PERMISSION_EDIT', '修改权限', '[修改权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (9, 0, 'OPERATION_PERMISSION_DEL', '删除权限', '[删除权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (10, 0, 'OPERATION_PERMISSION_DISABLE', '禁用权限', '[禁用权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (11, 0, 'OPERATION_PERMISSION_ENABLE', '启用权限', '[启用权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (12, 0, 'OPERATION_USER_VIEW', '查看用户', '[查看用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (13, 0, 'OPERATION_USER_ADD', '添加用户', '[添加用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (14, 0, 'OPERATION_USER_EDIT', '修改用户', '[修改用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (15, 0, 'OPERATION_USER_DEL', '删除用户', '[删除用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (16, 0, 'OPERATION_USER_DISABLE', '禁用用户', '[禁用用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (17, 0, 'OPERATION_USER_ENABLE', '启用用户', '[启用用户]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (18, 0, 'OPERATION_GROUP_VIEW', '查看用户组', '[查看用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (19, 0, 'OPERATION_GROUP_ADD', '添加用户组', '[添加用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (20, 0, 'OPERATION_GROUP_EDIT', '修改用户组', '[修改用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (21, 0, 'OPERATION_GROUP_DEL', '删除用户组', '[删除用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (22, 0, 'OPERATION_GROUP_DISABLE', '禁用用户组', '[禁用用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (23, 0, 'OPERATION_GROUP_ENABLE', '启用用户组', '[启用用户组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (24, 0, 'OPERATION_ROLE_VIEW', '查看角色', '[查看角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (25, 0, 'OPERATION_ROLE_ADD', '添加角色', '[添加角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (26, 0, 'OPERATION_ROLE_EDIT', '修改角色', '[修改角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (27, 0, 'OPERATION_ROLE_DEL', '删除角色', '[删除角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (28, 0, 'OPERATION_ROLE_DISABLE', '禁用角色', '[禁用角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (29, 0, 'OPERATION_ROLE_ENABLE', '启用角色', '[启用角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (30, 0, 'OPERATION_USER_GROUP_BIND', '给用户分配组', '[给用户分配组]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (31, 0, 'OPERATION_USER_ROLE_BIND', '给用户分配角色', '[给用户分配角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (32, 0, 'OPERATION_ROLE_GROUP_BIND', '给用户组分配角色', '[给用户组分配角色]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation` VALUES (33, 0, 'OPERATION_ROLE_PERMISSION_BIND', '给角色分配权限', '[给角色分配权限]功能', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_operation_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_operation_permission`;
CREATE TABLE `t_operation_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `operation_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '功能模块操作ID',
  `permission_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '权限ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '菜单权限状态',
  INDEX `operation_id`(`operation_id`) USING BTREE COMMENT '功能模块操作ID',
  INDEX `permission_id`(`permission_id`) USING BTREE COMMENT '权限ID'
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '功能模块操作权限表。\r\n用来定义哪个权限对该模块可操作（一对一）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_operation_permission
-- ----------------------------
INSERT INTO `t_operation_permission` VALUES (1, 1, 6, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (2, 2, 7, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (3, 3, 8, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (4, 4, 9, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (5, 5, 10, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (6, 6, 11, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (7, 7, 12, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (8, 8, 13, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (9, 9, 14, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (10, 10, 15, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (11, 11, 16, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (12, 12, 17, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (13, 13, 18, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (14, 14, 19, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (15, 15, 20, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (16, 16, 21, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (17, 17, 22, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (18, 18, 23, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (19, 19, 24, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (20, 20, 25, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (21, 21, 26, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (22, 22, 27, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (23, 23, 28, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (24, 24, 29, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (25, 25, 30, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (26, 26, 31, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (27, 27, 32, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (28, 28, 33, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (29, 29, 34, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (30, 30, 35, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (31, 31, 36, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (32, 32, 37, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_operation_permission` VALUES (33, 33, 38, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_permission`;
CREATE TABLE `t_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `pid` bigint(20) NOT NULL DEFAULT 0 COMMENT '所属父级权限ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '权限唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '权限名称',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '权限介绍',
  `category` tinyint(1) NOT NULL DEFAULT 1 COMMENT '权限类别  1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '权限状态',
  INDEX `pid`(`pid`) USING BTREE COMMENT '父级权限ID',
  INDEX `code`(`code`) USING BTREE COMMENT '权限CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 42 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '权限表。\r\n不同的用户能操作和查看不同的功能（如页面、菜单和按钮等）。因此需要定义一张表来存储权限相关的信息。包括权限之前还有父子关系，分配了父级后，应该拥有所有的子级权限。同时权限的信息也会分配至前端页面来控制，因此需要提供一个唯一标识（code）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_permission
-- ----------------------------
INSERT INTO `t_permission` VALUES (1, 0, 'PERMISSION_HOME_QUERY', '首页菜单访问', '[首页]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (2, 0, 'PERMISSION_SETTING_QUERY', '设置菜单访问', '[设置]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (3, 2, 'PERMISSION_MENU_QUERY', '设置 - 菜单管理', '[设置 - 菜单管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (4, 2, 'PERMISSION_OPERATION_QUERY', '设置 - 操作管理', '[设置 - 操作管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (5, 2, 'PERMISSION_USER_QUERY', '设置 - 用户管理', '[设置 - 用户管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (6, 2, 'PERMISSION_GROUP_QUERY', '设置 - 用户组管理', '[设置 - 用户组管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (7, 2, 'PERMISSION_ROLE_QUERY', '设置 - 角色管理', '[设置 - 角色管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (8, 2, 'PERMISSION_PERMISSION_QUERY', '设置 - 权限管理', '[设置 - 权限管理]的访问权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (9, 0, 'PERMISSION_MENU_ADD', '添加菜单', '[添加菜单]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (10, 0, 'PERMISSION_MENU_EDIT', '修改菜单', '[修改菜单]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (11, 0, 'PERMISSION_MENU_DEL', '删除菜单', '[删除菜单]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (12, 0, 'PERMISSION_MENU_DISABLE', '禁用菜单', '[禁用菜单]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (13, 0, 'PERMISSION_MENU_DISABLE', '启用菜单', '[启用菜单]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (14, 0, 'PERMISSION_PERMISSION_VIEW', '查看权限', '[查看权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (15, 0, 'PERMISSION_PERMISSION_ADD', '添加权限', '[添加权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (16, 0, 'PERMISSION_PERMISSION_EDIT', '修改权限', '[修改权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (17, 0, 'PERMISSION_PERMISSION_DEL', '删除权限', '[删除权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (18, 0, 'PERMISSION_PERMISSION_DISABLE', '禁用权限', '[禁用权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (19, 0, 'PERMISSION_PERMISSION_ENABLE', '启用权限', '[启用权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (20, 0, 'PERMISSION_USER_VIEW', '查看用户', '[查看用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (21, 0, 'PERMISSION_USER_ADD', '添加用户', '[添加用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (22, 0, 'PERMISSION_USER_EDIT', '修改用户', '[修改用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (23, 0, 'PERMISSION_USER_DEL', '删除用户', '[删除用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (24, 0, 'PERMISSION_USER_DISABLE', '禁用用户', '[禁用用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (25, 0, 'PERMISSION_USER_ENABLE', '启用用户', '[启用用户]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (26, 0, 'PERMISSION_GROUP_VIEW', '查看用户组', '[查看用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (27, 0, 'PERMISSION_GROUP_ADD', '添加用户组', '[添加用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (28, 0, 'PERMISSION_GROUP_EDIT', '修改用户组', '[修改用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (29, 0, 'PERMISSION_GROUP_DEL', '删除用户组', '[删除用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (30, 0, 'PERMISSION_GROUP_DISABLE', '禁用用户组', '[禁用用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (31, 0, 'PERMISSION_GROUP_ENABLE', '启用用户组', '[启用用户组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (32, 0, 'PERMISSION_ROLE_VIEW', '查看角色', '[查看角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (33, 0, 'PERMISSION_ROLE_ADD', '添加角色', '[添加角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (34, 0, 'PERMISSION_ROLE_EDIT', '修改角色', '[修改角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (35, 0, 'PERMISSION_ROLE_DEL', '删除角色', '[删除角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (36, 0, 'PERMISSION_ROLE_DISABLE', '禁用角色', '[禁用角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (37, 0, 'PERMISSION_ROLE_ENABLE', '启用角色', '[启用角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (38, 0, 'PERMISSION_USER_GROUP_BIND', '给用户分配组', '[给用户分配组]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (39, 0, 'PERMISSION_USER_ROLE_BIND', '给用户分配角色', '[给用户分配角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (40, 0, 'PERMISSION_GROUP_ROLE_BIND', '给用户组分配角色', '[给用户组分配角色]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);
INSERT INTO `t_permission` VALUES (41, 0, 'PERMISSION_ROLE_PERMISSION_BIND', '给角色分配权限', '[给角色分配权限]的操作权限', 3, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_role
-- ----------------------------
DROP TABLE IF EXISTS `t_role`;
CREATE TABLE `t_role`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `pid` bigint(20) NOT NULL DEFAULT 0 COMMENT '所属父级角色ID',
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '角色唯一CODE代码',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '角色名称',
  `intro` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '角色介绍',
  `is_super` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否超管  0-否  1-是',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '角色状态',
  INDEX `pid`(`pid`) USING BTREE COMMENT '父级角色ID',
  INDEX `code`(`code`) USING BTREE COMMENT '角色CODE代码'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '角色' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_role
-- ----------------------------
INSERT INTO `t_role` VALUES (1, 0, 'ROLE_SUPER_MANAGER', '超级管理员', '超级管理员，拥有所有权限', 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_role_permission
-- ----------------------------
DROP TABLE IF EXISTS `t_role_permission`;
CREATE TABLE `t_role_permission`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `role_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '角色ID',
  `permission_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '权限ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '角色权限状态',
  INDEX `role_id`(`role_id`) USING BTREE COMMENT '角色ID',
  INDEX `permission_id`(`permission_id`) USING BTREE COMMENT '权限ID'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '角色权限表。\r\n用来定义每个角色组中有哪些权限' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_role_permission
-- ----------------------------

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '姓名',
  `head_img_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '头像图片地址',
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '手机号码',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT '' COMMENT '邮箱',
  `salt` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '密码加盐',
  `password` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '登录密码',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '用户状态'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户表。主要是用来记录用户的基本信息和密码信息。其中禁用状态（state）主要是在后台管理控制非法用户使用系统；密码加盐（salt）则是用于给每个用户的登录密码加一把唯一的锁，即使公司加密公钥泄露后，也不会导致全部用户的密码泄露' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user
-- ----------------------------
INSERT INTO `t_user` VALUES (1, 'root', '', '', '', 'root', 'b4b8daf4b8ea9d39568719e1e320076f', '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_user_group
-- ----------------------------
DROP TABLE IF EXISTS `t_user_group`;
CREATE TABLE `t_user_group`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '用户ID',
  `group_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '用户组ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '用户组成员状态',
  INDEX `user_group_id`(`group_id`) USING BTREE COMMENT '用户组ID',
  INDEX `user_id`(`user_id`) USING BTREE COMMENT '用户ID'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户组成员。最终用户拥有的所有权限 = 用户个人拥有的权限（t_role_user）+该用户所在用户组拥有的权限（t_role_user_group）' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user_group
-- ----------------------------
INSERT INTO `t_user_group` VALUES (1, 1, 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

-- ----------------------------
-- Table structure for t_user_role
-- ----------------------------
DROP TABLE IF EXISTS `t_user_role`;
CREATE TABLE `t_user_role`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '用户ID',
  `role_id` bigint(20) NOT NULL DEFAULT 0 COMMENT '角色ID',
  `created` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `creator` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '创建人',
  `edited` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  `editor` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '修改人',
  `status` tinyint(1) UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态  1-有效  2-无效',
  `sub_status` tinyint(2) UNSIGNED NOT NULL DEFAULT 10 COMMENT '子状态  10-有效  20-无效（删除）  21-无效（禁用）',
  `sort` int(11) NOT NULL DEFAULT 0 COMMENT '排序字段',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE COMMENT '用户角色状态',
  INDEX `user_id`(`user_id`) USING BTREE COMMENT '用户ID',
  INDEX `role_id`(`role_id`) USING BTREE COMMENT '角色ID'
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户角色' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_user_role
-- ----------------------------
INSERT INTO `t_user_role` VALUES (1, 1, 1, '2021-03-03 09:40:09', 'SYS', '2021-03-03 09:40:09', '', 1, 10, 0);

SET FOREIGN_KEY_CHECKS = 1;
