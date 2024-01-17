import mysql.connector
import os
from dotenv import load_dotenv
# This file allows you to connect to the MySQL database

class DatabaseManager:

  @staticmethod
  def connect_to_Database():
    # .env file contains host , user info, and password
    mydb = mysql.connector.connect(
      host=os.getenv("HOST"),
      user=os.getenv("USER"),
      password=os.getenv("PASSWORD"))

    return mydb

  @staticmethod
  def createSQLTableTopTracksQuery(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS top_tracks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                artist_id VARCHAR(255),
                song_name VARCHAR(255),
                artists VARCHAR(255),
                album VARCHAR(255),
                release_date DATE,
                preview_url VARCHAR(255)
            )
        """)
  @staticmethod
  def createSQLTableTopAlbumsQuery(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
               CREATE TABLE IF NOT EXISTS top_albums (
               id INT AUTO_INCREMENT PRIMARY KEY,
               artist_id VARCHAR(255)
               album_name VARCHAR(255)
               release_date DATE
               )
               """)
    return cursor





    
    
    
    




