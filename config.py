import MySQLdb
from MySQLdb.connections import Connection
import time
# Bot configuration
API_TOKEN = ''

# MySQL database connect
class DatabaseConnect:
    def __init__(self):
        self.ip         = 'localhost'
        self.port       = 3306
        self.username   = 'root'
        self.password   = ''
        self.database   = 'checkplace'
        self.charset    = 'utf8'
    
    def connection(self):
        connect = MySQLdb.connect(
            host    = self.ip,
            port    = self.port,
            user    = self.username,
            passwd  = self.password,
            charset = self.charset,
            db      = self.database
        )
        return connect

# about user authorization
class UserDatabaseConfig(DatabaseConnect):
    def __init__(self, telegram_id, name, age):
        DatabaseConnect.__init__(self)
        self.user_name = name
        self.user_age = age
        self.user_telegram_id = telegram_id
        self.table = 'users'

    # returned 1 if user was found, else 0
    def is_registered(self):
        is_registered = 1
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = "SELECT `telegram_id` FROM `{}` WHERE `telegram_id` = {}".format(self.table, self.user_telegram_id)
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query")
            cur.close()
            con.close()
            return False
        
        if not cur.fetchall():
            is_registered = 0
        cur.close()
        con.close()
        return is_registered


    def user_register(self):
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = "INSERT INTO `{}` (`id`, `telegram_id`, `name`, `birth`, `last_place_post`) VALUES (NULL, '{}', '{}', '{}', '{}')".format(self.table, self.user_telegram_id, self.user_name, self.user_age, int(time.time()))
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        else:
            con.commit()
        cur.close()
        con.close()
        return 1
    
    # checked how much hours has passed after posting place
    def check_hours(self):
        con = DatabaseConnect.connection(self)
        current_time = int(time.time())
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = f"SELECT `last_place_post` FROM `users` WHERE `telegram_id` = {self.user_telegram_id}"
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        
        user_time = int(cur.fetchall()[0][0])
        current_time = (current_time - user_time) // 3600
        cur.close()
        con.close()
        return current_time




# This class for parsing content
class Checkplace(DatabaseConnect):
    def __init__(self):
        DatabaseConnect.__init__(self)
        self.categories = 'categories'
        self.places = 'global_places'
    
    def show_categories(self):
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = "SELECT * FROM {} ORDER BY `id`".format(self.categories)
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        
        output = cur.fetchall()
        cur.close()
        con.close()
        return output
    
    def show_posts_preview_list(self, category_id):
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = "SELECT `id`, `name` FROM {} WHERE `category_id` = {}".format(self.places, category_id)
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        
        output = cur.fetchall()
        cur.close()
        con.close()
        return output
    
    def show_post(self, post_id):
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = "SELECT * FROM {} WHERE `id` = {}".format(self.places, post_id)
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        
        output = cur.fetchall()
        cur.close()
        con.close()
        return output



class UserPlaces(DatabaseConnect):
    def __init__(self, telegram_id):
        super().__init__()
        self.table = 'users_places'
        self.table2 = 'users'
        self.telegram_id = telegram_id
    
    def show_user_places(self):
        con = DatabaseConnect.connection(self)
        if not con:
            print("Fail to connect")
            return False
        cur = con.cursor()
        sql = f"SELECT `name`, `status` FROM `{self.table}` WHERE `telegram_id` = '{self.telegram_id}'"
        try:
            cur.execute(sql)
        except:
            print("Wrong SQL query: {}".format(sql))
            cur.close()
            con.close()
            return False
        output = cur.fetchall()
        cur.close()
        con.close()
        return output
