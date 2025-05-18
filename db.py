import sqlite3

from contextlib import closing

from objects import Player, Lineup

conn = None

def connect():
    global conn
    if not conn:
        DB_FILE = "team_players.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_player(row):
    return Player(row["firstName"], row["lastName"],
                  row["position"], row["points"], row["rebounds"],
                  row["assists"], row["startingOrder"], row["playerID"])

def get_players():    
    query = '''SELECT playerID, startingOrder, firstName, lastName,
                      position, points, rebounds, assists
               FROM Player 
               ORDER BY startingOrder'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    players = Lineup()
    for row in results:
        player = make_player(row)
        players.add(player)
    return players

def get_player(id):
    query = '''SELECT playerID, startingOrder, firstName, lastName,
                      position, points, rebounds, assists
               FROM Player
               WHERE playerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (id,))
        row = c.fetchone()
        if row:
            player = make_player(row)
            return player
        else:
            return None

def add_player(player):
    sql = '''INSERT INTO Player
               (firstName, lastName, position, points, rebounds, assists, startingOrder) 
             VALUES
               (?, ?, ?, ?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (player.firstName, player.lastName, player.position,
                        player.points, player.rebounds, player.assists, player.startingOrder))
        conn.commit()

def delete_player(player):
    sql = '''DELETE FROM Player WHERE playerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (player.playerID,))
        conn.commit()

def update_starting_order(lineup):
    for num, player in enumerate(lineup, start=1):
        player.startingOrder = num
        sql = '''UPDATE Player
                 SET startingOrder = ?
                 WHERE playerID = ?'''
        with closing(conn.cursor()) as c:
            c.execute(sql, (player.startingOrder, player.playerID))
    conn.commit()      

def update_player(player):
    sql = '''UPDATE Player
             SET position = ?,
                 points = ?,
                 rebounds = ?,
                 assists = ?
             WHERE playerID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (player.position, player.points, player.rebounds, player.assists, player.playerID))
        conn.commit()

def main():
    connect()
    players = get_players()
    for player in players:
        print(player.startingOrder, player.firstName, player.lastName,
              player.position, player.points, player.rebounds, player.assists)


if __name__ == "__main__":
    main()
