CREATE DATABASE IF NOT EXISTS 'packit';
USE 'packit';

DROP TABLE IF EXISTS 'user';
CREATE TABLE 'user'(
  'uID' int(8),
  'email' text,
  'varify' boolean,
  'password' int(8)
)

DROP TABLE IF EXISTS 'event';
CREATE TABLE 'event'(
  'event_title' text,
  'uID' int(8),
  'destination' text,
  'eventtype' text,
  'date' date,
  'lenth' int(8),
  'remained_time' int(8),
  'luggag_size' int(8),
  'eventID' text
)

DROP TABLE IF EXISTS 'private_list';
CREATE TABLE 'private_list'(
	'uID' int (8),
	'list_name' text,
	'eventID' text,
	'privatelistID' text
)

DROP TABLE IF EXISTS 'private_item';
CREATE TABLE 'private_item'(
	'uID' int(8),
	'item_name' text,
	'check' boolean,
	'itemID' text,
	'privatelistID' text
)

DROP TABLE IF EXISTS 'share_list';
CREATE TABLE 'share_list'(
	'list_name' text,
	'eventID' text,
	'sharelistID' text
)

DROP TABLE IF EXISTS 'share_item';
CREATE TABLE 'share_item'(
	'item_name' text,
	'check' boolean,
	'sharelistID' text,
	'itemID' text
)

