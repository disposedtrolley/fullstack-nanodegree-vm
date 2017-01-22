#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    database_name = "tournament"
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not establish a connection to the database.")


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    # Delete all match records.
    c.execute("TRUNCATE match;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    # Delete all player records.
    c.execute("TRUNCATE player CASCADE;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    # Get count of player records.
    c.execute("SELECT COUNT(*) FROM player;")
    count = c.fetchone()[0]
    DB.close()
    return int(count)


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()
    # Insert new player with stats defaulted to 0.
    query = "INSERT INTO player (name) VALUES (%s);"
    params = (name,)
    c.execute(query, params)
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, c = connect()
    # Retrieve players ordered by most wins first.
    c.execute("""SELECT p.id, p.name,
                 SUM(CASE WHEN m.winner = p.id THEN 1 ELSE 0 END) AS total_wins,
                 COUNT(m.id) AS total_matches
                 FROM player p
                 LEFT JOIN match m ON p.id IN (m.winner, m.loser)
                 GROUP BY p.id, p.name;
             """)
    player_standings = c.fetchall()
    DB.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, c = connect()
    # Insert details of the new match.
    query = "INSERT INTO match (winner, loser) VALUES (%s, %s);"
    params = (winner, loser)
    c.execute(query, params)
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    pairings = []
    paired_ids = []

    for i in standings:
        for j in standings:
            p1_id, p2_id = i[0], j[0]
            p1_name, p2_name = i[1], j[1]
            p1_wins, p2_wins = i[2], j[2]
            # check if either player is already registered.
            if p1_id not in paired_ids and p2_id not in paired_ids:
                # check number of wins is equal.
                if p1_wins == p2_wins:
                    # check that players are unique.
                    if p1_id != p2_id:
                        new_pairing = (p1_id, p1_name, p2_id, p2_name)
                        pairings.append(new_pairing)
                        paired_ids.append(p1_id)
                        paired_ids.append(p2_id)

    return pairings


if __name__ == "__main__":
    swissPairings()
