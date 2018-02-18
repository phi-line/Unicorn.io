-- Authors: Mojia and Harshita
-- Filename: database.sql
-- Modified Date: December 19, 2017
-- Scott.ai Final Project beta version

-- This DDL initializes the SQL database that will be used to store
-- all relevant data to the Scott.ai app. It contains multiple
-- tables to keep track of users, the content stored by the AI,
-- and user's activity within the app. The account and profile
-- tables are used to store user information, and are separate because
-- a user can create an account without creating a detailed profile,
-- and can even start using the AI without their profile filled out.
-- The category and AI tables are used to store hard-coded questions that the
-- AI can ask the users, and in the future, can even be added to by users
-- of the app to crowd-source more of the content. The convos
-- table stores all of the interacts between the user and the AI,
-- and for every conversation the user has (a set number of questions),
-- it will store the user's information, a conversation id, and a recorded
-- audio file that the user generates. In the future, this can be used to
-- use speech-to-text to check for the correctness of the user's spoken English.

SET FOREIGN_KEY_CHECKS=0; -- ignore foreign key checks when initializing tables

-- delete all tables before creating new ones
drop table if exists convos;
drop table if exists category;
drop table if exists sessions;
drop table if exists AI;
drop table if exists profile;
drop table if exists account;

SET FOREIGN_KEY_CHECKS=1;


-- This table stores basic profile information necessary to start
-- the account. All fields are required, as they are all needed
-- to login the uesr, and thus there are not many fields.
create table account(
	userId int auto_increment not null primary key,
	name varchar(50) not null,
	username varchar(50) not null,
	password varchar(100) not null -- this will be stored as a hash
);


-- This table stores more detailed information about the user, and
-- is generated from the onboarding survey. It includes relevant infromation
-- to their amount of history learning English, and also data about their
-- hobbies and interests, which can be used to tailor the user's conversations
-- with the AI. A foreign key of userId is used to link this data to
-- account data.
create table profile(
	userId int not null,
	yearsLearned varchar(50) not null,
	birthday Date not null,
	nativeLang varchar(50), -- persons native language
	nation varchar(50),
	points int not null default 0, -- points earned using the application
	timeActive int not null default 0, -- measured in time (minutes)
	-- link foreign key userId to account table
	foreign key (userId) references account(userId) on delete cascade on update cascade
);


-- This table stores mappings of categoryId and type, such that
-- users can later on add questions and create new categories.
-- The primary key is a categoryId, which is a foreign key in the AI
-- table, which ties questions to category.
create table category(
	categoryId int auto_increment not null primary key,
	categoryType varchar(50) -- topic of conversation
);

-- Hardcode some categories into table initially.
insert into category (categoryType) values ('school');
insert into category (categoryType) values ('food');
insert into category (categoryType) values ('hobby');


-- This table stores all questions that the AI can ask the user, categorized by questionId.
-- Each question is also linked to a unique categoryId, which helps the user choose what
-- kinds of questions they should expect. This categoryId is a foreign key stored in the
-- category table.
create table AI( -- stores all possible conversations
	questionId int auto_increment not null primary key,
	categoryId int not null, -- allows multiple questions to be grouped
	questionText varchar(100) not null, -- question the AI will ask
	foreign key (categoryId) references category(categoryId) on delete cascade on update cascade
);


-- Hardcode an initial set of questions to the AI table. In the future, users can contribute
-- to this and add more questions.
insert into AI (categoryId, questionText) values (1, "Tell me about your school. Do you like it?");
insert into AI (categoryId, questionText) values (1, "What's your favorite subject? Why do you like it so much?");
insert into AI (categoryId, questionText) values (1, "What's your favorite book? What makes it so fascinating?");
insert into AI (categoryId, questionText) values (1, "So...what do you imagine yourself doing in 50 years?");
insert into AI (categoryId, questionText) values (2, "What's your favorite dish? Describe it to be coz I want to try.");
insert into AI (categoryId, questionText) values (2, "Do you like to cook? What kind of food can you cook?");
insert into AI (categoryId, questionText) values (2, "What would you do to keep a healthy lifestyle?");
insert into AI (categoryId, questionText) values (3, "What do you like to do in your free time?");
insert into AI (categoryId, questionText) values (3, "What's your favorite sports? What's the secret of being good at it?");


-- This table stores all conversations that users have had with the AI. Each conversation is distinct,
-- so in a single session, the user can have multiple conversatins with the AI. This table maps each
create table convos( -- stores each conversation a user has
	convoId int auto_increment not null primary key,
	categoryId int not null, -- so we can join them to give feedback on user's performance for a set topic
	userId int not null, -- maps convo back to user
	audio varchar(100), -- store file path for audio answer - one audio file for entire conversation
	feedback varchar(256),
	foreign key (categoryId) references category(categoryId) on delete cascade on update cascade,
	foreign key (userId) references account(userId) on delete cascade on update cascade
);
