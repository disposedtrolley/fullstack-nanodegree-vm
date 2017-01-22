#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    # Delete all match records.
    c.execute("DELETE FROM match;")
    # Reset all player stats to 0.
    c.execute("UPDATE player SET matches = 0 WHERE matches > 0;")
    c.execute("UPDATE player SET wins = 0 WHERE wins > 0;")
    c.execute("UPDATE player SET losses = 0 WHERE losses > 0;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    # Delete all player records.
    c.execute("DELETE FROM player;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
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
    DB = connect()
    c = DB.cursor()
    # Insert new player with stats defaulted to 0.
    c.execute("""INSERT INTO player (name, wins, losses, matches)
                 VALUES (%s, %s, %s, %s);""",
              (name, 0, 0, 0))
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
    DB = connect()
    c = DB.cursor()
    # Retrieve players ordered by most wins first.
    c.execute("SELECT id, name, wins, matches FROM player ORDER BY wins DESC;")
    player_standings = c.fetchall()
    DB.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    # Insert details of the new match.
    c.execute("INSERT INTO match (winner, loser) VALUES (%s, %s);",
              (winner, loser))
    # Update the stats of the winning player.
    c.execute("UPDATE player SET wins = wins + 1 WHERE id = %s;",
              (winner,))
    c.execute("UPDATE player SET matches = matches + 1 WHERE id = %s;",
              (winner,))
    # Update the stats of the losing player.
    c.execute("UPDATE player SET losses = losses + 1 WHERE id = %s;",
              (loser,))
    c.execute("UPDATE player SET matches = matches + 1 WHERE id = %s;",
              (loser,))
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
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT a.id, a.name, b.id, b.name
              FROM player a, player b
              WHERE a.wins = b.wins
              AND a.id < b.id
              ORDER BY a.id, b.id""")
    all_pairs = c.fetchall()

    registered_player_ids = []
    registered_players = []

    # Remove repeated players:
    # Iterate through tuples and add each encountered player ID to an array.
    # If a tuple is encountered where neither of its players are found in the
    # ID array, add it as a valid pairing.
    for tup in all_pairs:
        if tup[0] not in registered_player_ids and \
                tup[2] not in registered_players:
            registered_player_ids.append(tup[0])
            registered_player_ids.append(tup[2])
            registered_players.append(tup)

    return registered_players


if __name__ == "__main__":
    pass
