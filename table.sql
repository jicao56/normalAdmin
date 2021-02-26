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

 Date: 27/02/2021 00:27:53
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
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '账号表。系统中，会有各种各样的登录方式，如手机号、邮箱地址、身份证号码和微信登录等。因此该表主要是用来记录每一种登录方式的信息，但不包含密码信息，因为各种登录方式都会使用同一个密码。每一条记录都会关联到唯一的一条用户记录' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户组表。\r\n虽然增加了角色表（role）后，把数据量从 100 亿降低至 10 亿，但 10 倍的数据量依然还是很多。而且大部分的用户（主体用户。如学生系统，学生就是主体）都会分配相同的角色组。用户组和角色组的区别：\r\n\r\n角色组（role）：解决的是权限的分组，减少了权限的重复分配\r\n用户组（user_group）：解决的是用户的分组，减少了用户的重复授权\r\n' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单表' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '菜单权限表。\r\n用来定义每个菜单对应哪个权限（一对一）' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '功能操作表' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '功能模块操作权限表。\r\n用来定义哪个权限对该模块可操作（一对一）' ROW_FORMAT = DYNAMIC;

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
  `category` tinyint(1) NOT NULL DEFAULT 0 COMMENT '权限类别  0-未知；1-菜单访问权限；2-页面元素可见性权限；3-功能模块操作权限；4-文件修改权限；',
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
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '权限表。\r\n不同的用户能操作和查看不同的功能（如页面、菜单和按钮等）。因此需要定义一张表来存储权限相关的信息。包括权限之前还有父子关系，分配了父级后，应该拥有所有的子级权限。同时权限的信息也会分配至前端页面来控制，因此需要提供一个唯一标识（code）' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '角色' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '角色权限表。\r\n用来定义每个角色组中有哪些权限' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户表。主要是用来记录用户的基本信息和密码信息。其中禁用状态（state）主要是在后台管理控制非法用户使用系统；密码加盐（salt）则是用于给每个用户的登录密码加一把唯一的锁，即使公司加密公钥泄露后，也不会导致全部用户的密码泄露' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户组成员。最终用户拥有的所有权限 = 用户个人拥有的权限（t_role_user）+该用户所在用户组拥有的权限（t_role_user_group）' ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '用户角色' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
