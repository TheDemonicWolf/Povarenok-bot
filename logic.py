import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS recipes(
                                    name TEXT,
                                    id INTEGER PRIMARY KEY,
                                    minutes INTEGER,
                                    contributor_id INTEGER,
                                    submitted DATE,
                                    tags TEXT,
                                    nutrition TEXT,
                                    n_steps INTEGER,
                                    steps TEXT,
                                    description TEXT,
                                    ingredients TEXT,
                                    n_ingredients INTEGER
                        )''') 
            
            
            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def get_random_recipe_3(self):
        sql = 'SELECT name FROM recipe ORDER BY RANDOM() LIMIT 3'
        return self.__select_data(sql)
    
    def get_random_recipe_5(self):
        sql = 'SELECT name FROM recipe ORDER BY RANDOM() LIMIT 5'
        return self.__select_data(sql)
    
    def get_random_recipe_10(self):
        sql = 'SELECT name FROM recipe ORDER BY RANDOM() LIMIT 10'
        return self.__select_data(sql)
            
    def get_info_recipe(self, name):
        sql = ''' 
                SELECT name, minutes, n_steps, steps, ingredients
                FROM recipe 
                WHERE name = ?
                '''
        return self.__select_data(sql=sql, data = (name,))
    
    def add_recipe(self, data):
        sql = '''INSERT INTO recipe 
                (name, minutes, contributor_id, date, tags, steps, description, ingredients)
                VALUES (?,?,?,?,?,?,?,?)'''
        
        return self.__executemany(sql, data)
    

    def find_by_ingredient(self, ingredient):
        sql = '''SELECT name FROM recipe WHERE ingredients LIKE ? LIMIT 15'''
        return self.__select_data(sql, (f"%{ingredient}%",))
    
    def get_id(self, name):
        sql = 'SELECT id FROM recipe WHERE name = ? '
        result = self.__select_data(sql=sql, data = (name,))
        return result[0][0] if result else None
    
    def add_favorite(self, user_id, recipe_name):
        recipe_id = self.get_id(recipe_name)
        if recipe_id:
            sql = 'INSERT INTO favorite (user_id, recipe_id, comment) VALUES (?, ?)'
            self.__executemany(sql, [(user_id, recipe_id)])
            return True
        
    def get_favorites(self, user_id):
        sql = '''
            SELECT recipe.name
            FROM favorite
            INNER JOIN recipes ON favorite.recipe_id = recipe.id
            WHERE favorite.user_id = ?
        '''
        return self.__select_data(sql = sql, data = (user_id,))





if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()