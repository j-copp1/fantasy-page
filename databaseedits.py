import sqlite3

def run() :

    dbAddress = 'fantasyDb_JL.db'
    db = sqlite3.connect(dbAddress)
    cursor = db.cursor()

    #edits for playoffs, corrects brackets

    #2016
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Bill Hedman',
            Away_Id = 'Megan Hale',
            Home_Score = 72,
            Away_Score = 73
            
        WHERE rowid = 103
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Adam Hedman',
            Away_Id = 'Tiffany Cloud',
            Home_Score = 69,
            Away_Score = 88
            
        WHERE rowid = 105
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Nathan Copp',
            Away_Id = 'Tiffany Cloud',
            Home_Score = 78,
            Away_Score = 111
            
        WHERE rowid = 110
    ''')
    #2017
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'HK Copp',
            Away_Id = 'Christopher Cherry',
            Home_Score = 68,
            Away_Score = 80
            
        WHERE rowid = 221
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Mackenzie Schofield',
            Away_Id = 'Adam Hedman',
            Home_Score = 121,
            Away_Score = 92
            
        WHERE rowid = 222
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Mackenzie Schofield',
            Away_Id = 'Adam Hedman',
            Home_Score = 121,
            Away_Score = 92
            
        WHERE rowid = 222
    ''')
    #2018
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Tiffany Cloud',
            Away_Id = 'Jonathan Copp',
            Home_Score = 74,
            Away_Score = 65
            
        WHERE rowid = 321
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Tiffany Cloud',
            Away_Id = 'Adam Hedman',
            Home_Score = 110,
            Away_Score = 94
            
        WHERE rowid = 326
    ''')
    #2019
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Mia Hedman',
            Away_Id = 'Nathan Copp',
            Home_Score = 95,
            Away_Score = 105
            
        WHERE rowid = 404
    ''')
    #2020
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'HK Copp',
            Away_Id = 'Chrisopher Cherry',
            Home_Score = 99.96,
            Away_Score = 96.24
            
        WHERE rowid = 485
    ''')
    cursor.execute('''
        UPDATE games
        SET Home_Id = 'Julie Hedman',
            Away_Id = 'HK Copp',
            Home_Score = 99.78,
            Away_Score = 81.22
            
        WHERE rowid = 489
    ''')
    db.commit()
    db.close()