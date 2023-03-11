from hidden import images
from getResult import get_result

def initCards(conn):
    imagesList = images.images
    existing_cards =  get_result(conn.execute('SELECT * FROM cards'))
    if len(existing_cards) > 0:
        return
    # -2 down               0
    # -1 up to down         1
    # 0 all                 2
    # 1 down to up          3
    # 2 up                  4
    cardsList = [
        { "image": imagesList[0], "damage": 70, "crit_chance": 10, "card_pos": 4, "title": "Wodny smok", "affect_next": 1.2, "affect_last":1.2},
        { "image": imagesList[1], "damage": 80, "crit_chance": 30, "card_pos": 0, "title": "Avatar of bravery"},
        { "image": imagesList[2], "damage": 80, "crit_chance": 25, "card_pos": 2, "title": "Avatar of death"},
        { "image": imagesList[3], "damage": 70, "crit_chance": 15, "card_pos": 1, "title": "Boski dziryt"},
        { "image": imagesList[4], "damage": 90, "crit_chance": 30, "card_pos": 0, "title": "Elemental mix-cios"},
        { "image": imagesList[5], "damage": 60, "crit_chance": 20, "card_pos": 0, "title": "Fireball", "fire_damage": 60, "fire_time": 1},
        { "image": imagesList[6], "damage": 45, "crit_chance": 20, "card_pos": 3, "title": "Flaming Boa", "fire_damage": 10, "fire_time": 3},
        { "image": imagesList[7], "damage": 25, "crit_chance": 5, "card_pos": 2, "title": "Fools tree", "poison_damage": 20, "poison_time": 2},
        { "image": imagesList[8], "damage": 50, "crit_chance": 25, "card_pos": 1, "title": "Jump stroke"},
        { "image": imagesList[9], "damage": 35, "crit_chance": 25, "card_pos": 1, "title": "Lightning spear", "affect_next": 1.4},
        { "image": imagesList[10], "damage": 80, "crit_chance": 10, "card_pos": 4, "title": "Piekielna hybryda"},
        { "image": imagesList[11], "damage": 60, "crit_chance": 10, "card_pos": 0, "title": "Possesed greatsword", "defense": 10},
        { "image": imagesList[12], "damage": 50, "crit_chance": 10, "card_pos": 4, "title": "Przelot"},
        { "image": imagesList[13], "damage": 60, "crit_chance": 20, "card_pos": 3, "title": "Savage Dove"},
        { "image": imagesList[14], "damage": 45, "crit_chance": 15, "card_pos": 1, "title": "Sparking blade", "defense": 15, "fire_damage": 20, "fire_time": 2},
        { "image": imagesList[15], "damage": 75, "crit_chance": 35, "card_pos": 0, "title": "Storming fist -2"},
        { "image": imagesList[16], "damage": 75, "crit_chance": 35, "card_pos": 3, "title": "Storming fist -1"},
        { "image": imagesList[17], "damage": 40, "crit_chance": 35, "card_pos": 1, "title": "Wierzchowiec"}
    ]
    
    for c in cardsList:
        text = []
        arg = []
        entries = [(k, c[k]) for k in iter(c)]
        for a in entries:
            text.append(a[0])
            arg.append(a[1])
        conn.execute('INSERT INTO cards(' + ','.join(text) + ') VALUES(' + ','.join(len(arg) * '?') + ')', arg)
        conn.commit()
