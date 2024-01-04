import mysql.connector
import os
from dotenv import load_dotenv
# This file allows you to connect to the MySQL database
def connect_to_Database():
  #.env file contains host , user info, and password
  mydb = mysql.connector.connect(
  host= os.getenv("HOST"),
  user= os.getenv("USER"),
  password= os.getenv("PASSWORD"))

  return mydb
