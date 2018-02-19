
DROP DATABASE IF EXISTS bot;
CREATE DATABASE IF NOT EXISTS bot DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

USE bot;

CREATE TABLE `wxadmins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(191) NOT NULL COMMENT '管理员昵称',
  `right_level` int(11) NOT NULL COMMENT '权限等级',
  `group_name` varchar(255) COMMENT '群组名',
  `status` int(11) DEFAULT '0' COMMENT '状态',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微信管理员表';