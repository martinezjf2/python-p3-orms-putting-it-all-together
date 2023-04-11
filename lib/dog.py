import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        
        self.id = CURSOR.lastrowid
        # self.id = CURSOR.execute("SELECT last_insert_rowid() from dogs").fetchone()[0]
        
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        song = cls(row[1], row[2], row[0])
        return song

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        
        dog = CURSOR.execute(sql,(name,)).fetchone()
        
        if not dog:
            return None
        
        return cls(
            name=dog[1],
            breed=dog[2],
            id=dog[0]
        )
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        
        dog = CURSOR.execute(sql, (id,)).fetchone()
        if not dog:
            return None
        
        return cls(
            name=dog[1],
            breed=dog[2],
            id=dog[0]
        )
        
        
    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            where (name, breed) = (?, ?)
            LIMIT 1
        """
        
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name, 
                breed=breed, 
                id=CURSOR.lastrowid)
        
        return Dog(
            name=row[1], 
            breed=row[2], 
            id=row[0]
            )   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
        pass