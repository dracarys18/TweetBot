import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

def getValue(name, default):
    return os.environ.get(name, default)

DB_URI = getValue("DATABASE_URL", "")
dbparse = urlparse(DB_URI)
DB_USER = dbparse.username
DB_PASS = dbparse.password
DB_NAME = dbparse.path[1:]
DB_HOST = dbparse.hostname

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port="5432")

cur = conn.cursor()

def create_table():
    '''RUN THIS FILE ONCE LOCALLY'''
    cur.execute("""CREATE TABLE acdet (
        ACID INT PRIMARY KEY  NOT NULL,
        ACCNAME TEXT  NOT NULL,
        LAST_TWEET BIGINT );""")

    conn.commit()
    conn.close()

class Users:
    def __init__(self):
        pass

    def add_to_db(self, ac_id, ac_name,last_tweet):
        """Add userdata to DB!"""
        if not ac_name:
            ac_name = ""
        if not last_tweet:
            last_tweet = 0
        try:
            data = (ac_id,ac_name,last_tweet)
            command = "INSERT INTO acdet (ACID, ACCNAME , LAST_TWEET) VALUES (%s, %s, %s)"
            cur.execute(command, data)
            conn.commit()
        except:
            conn.rollback()
        finally:
            return True
    
    def update_lastweet(self,ac_id,last_tweet):
        try:
            cur.execute("UPDATE acdet SET LAST_TWEET=%s WHERE ACID=%s",(last_tweet,ac_id))
            conn.commit()
        except:
            print("problem")
        finally:    
            return True


    def getUser_from_userid(self, ac_id):
        """Get user details from just userid!"""
        cur.execute(f"SELECT * from acdet where ACID = {str(ac_id)}")
        return cur.fetchall()

    def getAll(self):
        cur.execute(f"SELECT * from acdet")
        return cur.fetchall()
    
    def get_lastweet(self,ac_id):
        cur.execute(f"SELECT last_tweet from acdet where ACID = {str(ac_id)} ")
        return cur.fetchall()

    def count(self):
        cur.execute(f"SELECT COUNT(*) from acdet")
        return cur.fetchall()

    def get_userids(self):
        cur.execute(f"SELECT ACID from acdet")
        return cur.fetchall()

    def close(self):
        conn.close()

    def search(self, ac_id=None, ac_name=None, last_tweet=None):
        cur.execute("SELECT * FROM acdet WHERE ac_id=%s or ac_name=%s or last_tweet=%s ", (ac_id, ac_name, last_tweet))
        return cur.fetchall()


if __name__ == '__main__':
    create_table()