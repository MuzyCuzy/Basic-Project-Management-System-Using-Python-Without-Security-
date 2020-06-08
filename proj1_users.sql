CREATE DATABASE  IF NOT EXISTS `proj1`;
USE `proj1`;
--
-- Host: 127.0.0.1    Database: proj1
-- ------------------------------------------------------
-- Table structure for table `users`

CREATE TABLE `users` (
  `name` varchar(30) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `dept` varchar(50) DEFAULT NULL,
  `doj` varchar(11) DEFAULT NULL,
  `un` varchar(30) DEFAULT NULL,
  `pw` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL
);