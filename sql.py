'''
Python script to simplify usage of PostgreSQL
Goal: Any team member can use PostgreSQL without needing to learn any PostgreSQL commands
'''

import psycopg2
from psycopg2 import sql

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="photon"
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def create_table():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INT,
                    codename VARCHAR(100)
                );
            ''')
            conn.commit()
            cur.close()
            print("Table created successfully.")
        except Exception as e:
            print("Error creating table:", e)
        finally:
            conn.close()

def create_player(player_id, codename):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename,))
            conn.commit()
            cur.close()
            print(f"Player '{codename}' inserted with ID {player_id}.")
        except Exception as e:
            print("Error inserting player:", e)
        finally:
            conn.close()

def fetch_players():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM players;")
            players = cur.fetchall()
            cur.close()
            print("\nPLAYER LIST:\n")
            for player in players:
                print(player)
        except Exception as e:
            print("Error fetching players:", e)
        finally:
            conn.close()
            return players

def update_player(player_id, codename):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE players SET name = %s WHERE id = %s;", (codename, player_id))
            conn.commit()
            cur.close()
            print("Player updated successfully.")
        except Exception as e:
            print("Error updating player:", e)
        finally:
            conn.close()

def delete_player(player_id):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM players WHERE id = %s;", (player_id,))
            conn.commit()
            cur.close()
            print("Player deleted successfully.")
        except Exception as e:
            print("Error deleting player:", e)
        finally:
            conn.close()

def delete_table(table_name):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
            conn.commit()
            cur.close()
            print(f"Table '{table_name}' deleted successfully.")
        except Exception as e:
            print("Error deleting table:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    #create_table()
    fetch_players()
