-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop database and recreate.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- Create Player table.
CREATE TABLE player(id serial PRIMARY KEY,
                    name text);

insert into player (name) values ('John');
insert into player (name) values ('James');
insert into player (name) values ('April');
insert into player (name) values ('Jane');
insert into player (name) values ('Katherine');

-- Create Match table.
CREATE TABLE match(id serial PRIMARY KEY,
                   winner int REFERENCES player(id),
                   loser int REFERENCES player(id));

insert into match (winner, loser) values (1, 2);
insert into match (winner, loser) values (3, 4);