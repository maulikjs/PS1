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
Gender varchar(10),
PRIMARY KEY(UserID)
);

CREATE TABLE Albums(
AlubmID integer NOT NULL AUTO_INCREMENT UNIQUE,
Album_name varchar(60),
OwnerID integer,
DateOfCreation DATE,
PRIMARY KEY(AlbumID)
);

CREATE TABLE Photos
(
  PhotoID int4  AUTO_INCREMENT,
  data longblob ,
  caption VARCHAR(255),
  AlbumID int4,
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
UserID integer,
CID integer,
PRIMARY KEY(UserID, CID),
FOREIGN KEY(UserID) REFERENCES Users,
FOREIGN KEY(CID) REFERENCES Comments
);

CREATE TABLE Creates(
UserID integer,
AlbumID integer,
PRIMARY KEY(AlbumID),
FOREIGN KEY(UserID) REFERENCES Users,
FOREIGN KEY(AlbumID) REFERENCES Albums
);

CREATE TABLE Likes(
UserID integer,
PhotoID integer,
PRIMARY KEY(UserID,PhotoID),
FOREIGN KEY(UserID) REFERENCES Users,
FOREIGN KEY(PhotoID) REFERENCES Photos
);

CREATE TABLE Stores(
PhotoID integer,
AlbumID integer,
PRIMARY KEY(PhotoID),
FOREIGN KEY(PhotoID) REFERENCES Photos,
FOREIGN KEY(AlbumID) REFERENCES Albums
);

CREATE TABLE Has(
CID integer,
PhotoID integer,
PRIMARY KEY(CID),
FOREIGN KEY(CID) REFERENCES Comments,
FOREIGN KEY(PhotoID) REFERENCES Photos
);

CREATE TABLE AssociatedWith(
TagID integer,
AlbumID integer,
PRIMARY KEY(TagID,PhotoID),
FOREIGN KEY(TagID) REFERENCES Tags,
FOREIGN KEY(PhotoID) REFERENCES Photos
);

CREATE TABLE FriendsWith(
UID1 integer,
UID2 integer,
PRIMARY KEY(UID1,UID2),
FOREIGN KEY(UID1) REFERENCES Users(UserID),
FOREIGN KEY(UID2) REFERENCES Users(UserID)
);





INSERT INTO Users (email, password) VALUES ('test@bu.edu', 'test');
INSERT INTO Users (email, password) VALUES ('test1@bu.edu', 'test');
