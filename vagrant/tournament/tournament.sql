-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- PLAYER table
-- id (serial) PK
-- wins (int)
-- losses (int)

drop table if exists player cascade;
create table player(id serial primary key,
                    name text,
                    wins int,
                    losses int,
                    matches int);

-- insert into player (name, wins, losses, matches) values ('John', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('James', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('April', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Jane', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Katherine', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Ken', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Zoe', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Liz', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Susan', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Emily', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('David', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Robert', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Chris', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Sarah', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Paul', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Charlotte', 0, 0, 0);
-- insert into player (name, wins, losses, matches) values ('Stephanie', 0, 0, 0);

-- MATCH table

-- id (serial) PK
-- player (int) FK
-- winner (int), -1 if tie

drop table if exists match cascade;
create table match(id serial primary key,
                   winner int references player(id),
                   loser int references player(id));

-- insert into match (winner, loser) values (1, 2);
-- insert into match (winner, loser) values (3, 4);
-- insert into match (winner, loser) values (5, 6);
-- insert into match (winner, loser) values (7, 8);