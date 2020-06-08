CREATE DATABASE  IF NOT EXISTS `proj1`;
USE `proj1`;

-- Host: 127.0.0.1    Database: proj1
-- ------------------------------------------------------
-- Table structure for table `projects`

CREATE TABLE `projects` (
  `projname` varchar(60) DEFAULT NULL,
  `sub` varchar(500) DEFAULT NULL,
  `estbud` int(11) DEFAULT NULL,
  `allbud` int(11) DEFAULT NULL,
  `projid` int(11) DEFAULT NULL,
  `complsubs` varchar(500) DEFAULT NULL,
  `complbudg` int(11) DEFAULT NULL
);