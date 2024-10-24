CREATE DATABASE PJ;

USE PJ;

CREATE TABLE Users(ID int PRIMARY KEY AUTO_INCREMENT NOT NULL, userName varchar(255) NOT NULL, userID varchar(255) NOT NULL, userEmail varchar(255) NOT NULL, userPassword varchar(255) NOT NULL, userDP varchar(255) NOT NULL);

CREATE TABLE Blogs(userID varchar(255) NOT NULL, uploadTime DATETIME NOT NULL, blogTitle varchar(255) NOT NULL, blog longtext NOT NULL);

CREATE TABLE Follow(follower varchar(255) NOT NULL, following varchar(255) NOT NULL);