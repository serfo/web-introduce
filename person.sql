/*
 Navicat Premium Data Transfer

 Source Server         : aaa
 Source Server Type    : MySQL
 Source Server Version : 50740 (5.7.40)
 Source Host           : localhost:3306
 Source Schema         : person

 Target Server Type    : MySQL
 Target Server Version : 50740 (5.7.40)
 File Encoding         : 65001

 Date: 11/01/2023 23:43:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Content` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Path` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `From` int(11) NOT NULL,
  `Time` datetime NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `From`(`From`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`From`) REFERENCES `user` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------

-- ----------------------------
-- Table structure for game
-- ----------------------------
DROP TABLE IF EXISTS `game`;
CREATE TABLE `game`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Label` varchar(30) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Name` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Detail` varchar(360) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Image` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Url` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of game
-- ----------------------------
INSERT INTO `game` VALUES (1, 'Wordle', 'Wordle', 'Wordle is an online word guessing game. Players can guess a five letter word in Wordle every day. There are six chances to enter a word. Green means that the correct letter is in this position, yellow means that the letter is included in the word, but not in this position, and gray means that the letter is not included in the word.', '../static/image/Wordle.png', '/games/wordle');
INSERT INTO `game` VALUES (2, 'Wordle Assist', 'Wordle_assist', 'Wordle assistant can assist you in word guessing game. You only need to enter your word guessing situation in Wordle to get the word closest to the answer.You can continue to input the situation of guessing words many times, and it will update the score ranking of each word.', '../static/image/Wordle_assist.png', '/games/wordle_assist');

-- ----------------------------
-- Table structure for gamedata
-- ----------------------------
DROP TABLE IF EXISTS `gamedata`;
CREATE TABLE `gamedata`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `GameName` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Player` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Data` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Result` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gamedata
-- ----------------------------

-- ----------------------------
-- Table structure for like
-- ----------------------------
DROP TABLE IF EXISTS `like`;
CREATE TABLE `like`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `To` int(11) NOT NULL,
  `From` int(11) NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE,
  INDEX `To`(`To`) USING BTREE,
  INDEX `From`(`From`) USING BTREE,
  CONSTRAINT `like_ibfk_1` FOREIGN KEY (`To`) REFERENCES `comment` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `like_ibfk_2` FOREIGN KEY (`From`) REFERENCES `user` (`Id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of like
-- ----------------------------

-- ----------------------------
-- Table structure for tech
-- ----------------------------
DROP TABLE IF EXISTS `tech`;
CREATE TABLE `tech`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Label` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Detail` varchar(320) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tech
-- ----------------------------
INSERT INTO `tech` VALUES (1, 'HTML and CSS', 'Master the bootstrap UI framework, skillfully write CSS code, be familiar with common HTML tags, and be able to design HTML pages of 4.0 and below.');
INSERT INTO `tech` VALUES (2, 'JavaScript', 'Master the JQuery JS framework, skillfully write JS functions, and use the Ajax provided by the framework to interact with each other through Get and Post.');
INSERT INTO `tech` VALUES (3, 'Python', 'Be familiar with Flask and Django frameworks, have a deep understanding of python\'s various data processing (strings, lists, dictionaries, pictures, etc.), and master numpy, pandas and other data analysis tools.');
INSERT INTO `tech` VALUES (4, 'Mysql', 'Understand the database connection principle of pymysql, and query the database through the orm method provided by the flash sqlalchemy library to make the code written simple and easy to read.');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Email` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Password` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Avatar` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Notify` enum('1','2','3') CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `Lastlogin` datetime NOT NULL,
  PRIMARY KEY (`Id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
