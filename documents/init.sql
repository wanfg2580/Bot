
DROP DATABASE IF EXISTS bot_back;
CREATE DATABASE IF NOT EXISTS bot_back DEFAULT CHARACTER SET utf8mb4;

USE bot_back;

CREATE TABLE `wxadmins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(191) NOT NULL COMMENT '管理员昵称',
  `user_id` varchar(191) NOT NULL COMMENT '管理员用户id',
  `right_level` int(11) NOT NULL COMMENT '权限等级',
  `group_name` varchar(255) COMMENT '群组名',
  `group_id` varchar(255) COMMENT '群组id',
  `status` int(11) DEFAULT '0' COMMENT '状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='微信管理员表';

CREATE TABLE `wxmessages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `msg_id` varchar(255) NOT NULL COMMENT '消息编号',
  `user_name` VARCHAR (100) NOT NULL COMMENT '用户昵称',
  `user_id` varchar(255) NOT NULL COMMENT '用户编号',
  `is_group` int(11) NOT NULL COMMENT '是否为群消息',
  `group_name` varchar(50) COMMENT '群昵称',
  `group_id` varchar(255) COMMENT '群编号',
  `msg_content` TEXT COMMENT '消息内容',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='微信管理员表';