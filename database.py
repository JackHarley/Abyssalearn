import sqlite3

class DbHolder:
    conn = None

def get_db_conn():
    if not DbHolder.conn:
        DbHolder.conn = sqlite3.connect("data/database.db")
    return DbHolder.conn

def create_tables():
    db_conn = get_db_conn()
    c = db_conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dogma_attributes (
            attribute_id INTEGER PRIMARY KEY,
            name TEXT,
            display_name TEXT,
            description TEXT,
            high_is_good INTEGER,
            default_value REAL
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS types (
            type_id INTEGER PRIMARY KEY,
            name TEXT
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            contract_id INTEGER PRIMARY KEY,
            date_issued INTEGER,
            date_expired INTEGER,
            price INTEGER
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS abyssal_observations (
            item_id INTEGER PRIMARY KEY,
            type_id INTEGER,
            contract_id INTEGER,
            dogma_attributes TEXT,
            dogma_effects TEXT,
            source_type_id INTEGER,
            mutator_type_id INTEGER
        );
    ''')

    db_conn.commit()