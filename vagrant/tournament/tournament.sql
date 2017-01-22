-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop existing Player table.
DROP TABLE IF EXISTS player CASCADE;

-- Create Player table.
CREATE TABLE player(id serial PRIMARY KEY,
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

-- Drop existing Match table.
DROP TABLE IF EXISTS match CASCADE;

-- Create Match table.
CREATE TABLE match(id serial PRIMARY KEY,
                   winner int REFERENCES player(id),
                   loser int REFERENCES player(id));

-- insert into match (winner, loser) values (1, 2);
-- insert into match (winner, loser) values (3, 4);
-- insert into match (winner, loser) values (5, 6);
-- insert into match (winner, loser) values (7, 8);

SELECT DISTINCT a.id,
                a.name,
                b.id,
                b.name
FROM player a,
     player b
WHERE abs(a.wins - b.wins) <= 1
  AND a.id < b.id;