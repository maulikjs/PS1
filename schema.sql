DROP DATABASE photosharemaulik;
CREATE DATABASE photosharemaulik;
USE photosharemaulik;   

CREATE TABLE Users(
UserID int4 NOT NULL AUTO_INCREMENT UNIQUE,
First_Name varchar(60),
Last_Name varchar(60),
email varchar(60) UNIQUE,
Password varchar(60),
DOB DATE,
Hometown varchar(60),
Gender varchar(1),
PRIMARY KEY(UserID)
);

CREATE TABLE Albums(
AlbumID int4 AUTO_INCREMENT UNIQUE,
Album_name varchar(60),
OwnerID integer,
DateOfCreation DATETIME default current_timestamp,
PRIMARY KEY(AlbumID)
);

CREATE TABLE Photos
(
  PhotoID int4  AUTO_INCREMENT,
  data longblob ,
  caption VARCHAR(255),
  PRIMARY KEY (PhotoID)
);

CREATE TABLE Tags(
TagID integer NOT NULL AUTO_INCREMENT UNIQUE,
Title varchar(60),
PRIMARY KEY(TagID)
);

CREATE TABLE Comments(
CID integer NOT NULL AUTO_INCREMENT UNIQUE,
CommentText varchar(255),
PRIMARY KEY(CID)
);

CREATE TABLE Writes(
UserID int4,
CID int4,
PRIMARY KEY(UserID, CID),
FOREIGN KEY(UserID) REFERENCES Users(UserID),
FOREIGN KEY(CID) REFERENCES Comments(CID) ON DELETE CASCADE
);

CREATE TABLE Creates(
UserID integer,
AlbumID integer auto_increment,
PRIMARY KEY(AlbumID),
FOREIGN KEY(UserID) REFERENCES Users(UserID),
FOREIGN KEY(AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE
);

CREATE TABLE Likes(
UserID integer,
PhotoID integer,
PRIMARY KEY(UserID,PhotoID),
FOREIGN KEY(UserID) REFERENCES Users(UserID), 
FOREIGN KEY(PhotoID) REFERENCES Photos(PhotoID) ON DELETE CASCADE
);

CREATE TABLE Stores(
PhotoID integer auto_increment,
AlbumID integer,
PRIMARY KEY(PhotoID),
FOREIGN KEY(PhotoID) REFERENCES Photos(PhotoID) ON DELETE CASCADE,
FOREIGN KEY(AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE
);

CREATE TABLE Has(
CID integer,
PhotoID integer,
PRIMARY KEY(CID),
FOREIGN KEY(CID) REFERENCES Comments(CID) ON DELETE CASCADE,
FOREIGN KEY(PhotoID) REFERENCES Photos(PhotoID) ON DELETE CASCADE
);

CREATE TABLE AssociatedWith(
TagID integer,
PhotoID integer,
PRIMARY KEY(TagID,PhotoID),
FOREIGN KEY(TagID) REFERENCES Tags(TagID) ON DELETE CASCADE,
FOREIGN KEY(PhotoID) REFERENCES Photos(PhotoID) ON DELETE CASCADE
);

CREATE TABLE FriendsWith(
UID1 integer,
UID2 integer,
PRIMARY KEY(UID1,UID2),
FOREIGN KEY(UID1) REFERENCES Users(UserID),
FOREIGN KEY(UID2) REFERENCES Users(UserID)
);

INSERT INTO USERS(USERID, FIRST_NAME) VALUES (99,'Anonymous')