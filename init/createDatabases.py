from users import default_avatar
from init import initCards

def create_databases(conn):
    # users
    conn.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password INTEGER NOT NULL,
        avatar TEXT DEFAULT "''' + default_avatar.avatar + '''",
        init_date DATE DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    # invites
    conn.execute('''CREATE TABLE IF NOT EXISTS invites(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invitee_id INTEGER NOT NULL,
        invited_id INTEGER NOT NULL,
        FOREIGN KEY(invitee_id) REFERENCES users(id),
        FOREIGN KEY(invited_id) REFERENCES users(id)
    )''')
    # friends
    conn.execute('''CREATE TABLE IF NOT EXISTS friends(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invitee_id INTEGER NOT NULL,
        invited_id INTEGER NOT NULL,
        init_date DATE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(invitee_id) REFERENCES users(id),
        FOREIGN KEY(invited_id) REFERENCES users(id)
    )''')
    conn.commit()
    # chat messeages
    conn.execute('''CREATE TABLE IF NOT EXISTS messeages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        messeage VARCHAR(250) NOT NULL,
        invitee_id INTEGER NOT NULL,
        invited_id INTEGER NOT NULL,
        init_date DATE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(invitee_id) REFERENCES users(id),
        FOREIGN KEY(invited_id) REFERENCES users(id)
    )''')
    conn.commit()

    # cards
    # crit_chance INTEGER NOT NULL,
    conn.execute('''CREATE TABLE IF NOT EXISTS cards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(20) UNIQUE,
        image TEXT UNIQUE,
        card_pos TINYINT NOT NULL,
        damage TINYINT NOT NULL,
        
        fire_damage TINYINT DEFAULT 0,
        fire_time TINYINT DEFAULT 0,
        poison_damage TINYINT DEFAULT 0,
        poison_time TINYINT DEFAULT 0,
        defense TINYINT DEFAULT 0,
        affect_next REAL DEFAULT 1,
        affect_last REAL DEFAULT 1
    )''')
    conn.commit()
    # decks     14 cards
    conn.execute('''CREATE TABLE IF NOT EXISTS decks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        deck VARCHAR(55) NOT NULL,
        init_date DATE DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()

    # matches
    conn.execute('''CREATE TABLE IF NOT EXISTS matches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invitee_id INTEGER NOT NULL,
        invited_id INTEGER NOT NULL,

        invitee_turn TINYINT DEFAULT 1,

        invitee_deck VARCHAR(55) NOT NULL,
        invited_deck VARCHAR(55) NOT NULL,

        invitee_cards VARCHAR(27) NOT NULL,
        invited_cards VARCHAR(27) NOT NULL,

        invitee_hp INTEGER DEFAULT 1500 NOT NULL,
        invited_hp INTEGER DEFAULT 1500 NOT NULL,
        
        invitee_fire_damage INTEGER DEFAULT 0,
        invitee_fire_time INTEGER  DEFAULT 0,

        invited_fire_damage INTEGER DEFAULT 0,
        invited_fire_time INTEGER DEFAULT 0,
        
        invitee_poison_damage INTEGER DEFAULT 0,
        invitee_poison_time INTEGER DEFAULT 0,
        
        invited_poison_damage INTEGER DEFAULT 0,
        invited_poison_time INTEGER DEFAULT 0,
        
        invitee_defense INTEGER DEFAULT 1,
        invited_defense INTEGER DEFAULT 1,

        last_move_cards TEXT NOT NULL,
        last_move DATE DEFAULT CURRENT_TIMESTAMP,
        init_date DATE DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(invitee_id) REFERENCES users(id),
        FOREIGN KEY(invited_id) REFERENCES users(id)
    )''')
    conn.commit()
    # waiting matches
    conn.execute('''CREATE TABLE IF NOT EXISTS waiting_matches(
        id INTEGER PRiMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_deck
        code INTEGER,
        init_date DATE DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_deck) REFERENCES decks(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    initCards.initCards(conn)