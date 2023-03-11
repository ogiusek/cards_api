from flask import jsonify
from getResult import get_result
from threads import threads
import time, threading, random, datetime, tryRemove

#   wait_matches    matches
def get_match(conn, req):
    try:
        invitee = True
        match_id = -1
        usr_id = get_result(conn.execute('SELECT id FROM users WHERE login = ?', [req.get('user')]))[0][0]
        if len(threads['wait_matches'].items()) > 0 and usr_id not in threads['wait_matches']:
            matches = sorted(threads['wait_matches'].items(), key=lambda x: x[1], reverse=False)
            match_id = create_match(conn, matches[0][0], usr_id, matches[0][1][2], req.get('deck'))["match_id"][0]
            matches[0][1][3] = match_id
            matches[0][1][0].set()
            invitee = False
        else:
            threads['wait_matches'][usr_id] = [threading.Event(), datetime.datetime.now(), req.get('deck'), -1]
            if not threads['wait_matches'][usr_id][0].wait(900):
                threads['wait_matches'].pop(usr_id)
                return jsonify({"value": "error"})
            match_id = threads['wait_matches'][usr_id][3]
            threads['wait_matches'].pop(usr_id)
            threads['matches'][match_id] = threading.Event()

        user_ids = get_result(conn.execute('SELECT invitee_id, invited_id FROM matches WHERE id = ?', [match_id]))[0]
        cards = get_result(conn.execute('SELECT invitee_cards, invited_cards FROM matches WHERE id = ?', [match_id]))[0][0 if not invitee else 1].split(',')
        int_cards = []
        for card in cards: int_cards.append(card)
        enemy_avatar = get_result(conn.execute('SELECT avatar FROM users WHERE id = ?', [usr_id]))[0][0]
        return jsonify({"value": "done", "match_id": match_id, "turn": invitee, "enemy_avatar": enemy_avatar, 
                        "invitee_id": user_ids[0], "invited_id": user_ids[1], "cards": int_cards})
    except:
        return jsonify({"value": "error"})

def stop_match(conn, req):
    try:
        usr_id = get_result(conn.execute('SELECT id FROM users WHERE login = ?', [req.get('user')]))[0][0]
        threads['wait_matches'].pop(usr_id)
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def get_random_cards(deck, exceptions, amount: int):
    array = deck.split(',')
    for exception in exceptions:
        tryRemove.tryremove(array, exception)

    allCards = random.sample(array, amount)
    convertedCards = ','.join(str(card) for card in allCards).split(',')
    return (','.join(convertedCards))

def create_match(conn, invitee_id, invited_id, invitee_deck, invited_deck):
    invitee_cards = get_random_cards(invitee_deck, [], 7)
    invited_cards = get_random_cards(invited_deck, [], 7)
    conn.execute('''INSERT INTO matches(invitee_id, invited_id, invitee_deck, invited_deck, 
        invitee_cards, invited_cards, last_move_cards) VALUES(?, ?, ?, ?, ?, ?, ?)''', [
        invitee_id, invited_id, invitee_deck, invited_deck, invitee_cards, invited_cards, ''])
    conn.commit()
    match_id = get_result(conn.execute('''SELECT id FROM matches WHERE invitee_id = ? AND invited_id = ? AND invitee_deck = ? AND invited_deck = ? AND 
        invitee_cards = ? AND invited_cards = ? AND last_move_cards = ? ORDER BY init_date''', [
        invitee_id, invited_id, invitee_deck, invited_deck, invitee_cards, invited_cards, '']))[0]
    threads['matches'][match_id] = threading.Event()
    threads['matches'][match_id].clear()
    return {"match_id": match_id, "invitee_cards": invitee_cards, "invited_cards": invited_cards}
