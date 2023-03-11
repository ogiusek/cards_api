from flask import jsonify
from getResult import get_result
from threads import threads
from wait_matches import get_random_cards
import threading, random, numpy

def play(conn, req):
    try:
        if req.get('match_id') not in threads['matches']:
            threads['matches'][req.get('match_id')] = threading.Event()
        usr_id = get_result(conn.execute('SELECT id FROM users WHERE login = ?', [req.get('user')]))[0][0]
        result = get_match(conn, req)
        user_key = 'invitee_' if result['invitee_turn'] == 1 else 'invited_'
        enemy_key = 'invitee_' if result['invitee_turn'] == 0 else 'invited_'
        for_turn = get_result(conn.execute('SELECT invitee_id, invited_id, invitee_turn FROM matches WHERE id = ?', [req.get('match_id')]))[0]
        turn = (for_turn[0] == usr_id) if for_turn[2] == 1 else (for_turn[1] == usr_id)
        if not turn:
            threads['matches'][req.get('match_id')].clear()
            if not threads['matches'][req.get('match_id')].wait(300):
                threads['matches'].pop(req.get('match_id'))
            for element in get_result(conn.execute('SELECT invitee_hp, invited_hp FROM matches WHERE id = ?', [req.get('match_id')]))[0]:
                if element <= 0:
                    threads['matches'].pop(req.get('match_id'))
        else:
            deal_effects_damage(conn, req)
            result = get_match(conn, req)

            for i, card in enumerate(req.get('cards')):
                affected = (get_result(conn.execute('SELECT affect_next FROM cards WHERE id = ?', [req.get('cards')[i - 1]]))[0][0] \
                    if i - 1 >= 0 else 1) * \
                    (get_result(conn.execute('SELECT affect_next FROM cards WHERE id = ?', [req.get('cards')[i + 1]]))[0][0]\
                    if i + 1 < len(req.get('cards')) else 1)
                deal_card_damage(conn, result, card, affected)
            
            result[enemy_key + 'defense'] = 0
            result['invitee_turn'] = 1 if result['invitee_turn'] == 0 else 0
            
            filtered = [card for card in result[user_key + 'cards'].split(',') if int(card) not in req.get('cards')]
            nCards = get_random_cards(result[user_key + 'deck'], result[user_key + 'cards'].split(','), \
                                    (7 - len(filtered))).split(',')
            if nCards[0] == '':
                nCards.remove()
            result[user_key + 'cards'] = ','.join(nCards + filtered)
            set_values(conn, result)
            threads['matches'][req.get('match_id')].set()
        result = get_match(conn, req)
        if usr_id == result['invitee_id']:
            result['invited_cards'] = ''
            result['cards'] = result['invitee_cards']
        else:
            result['invitee_cards'] = ''
            result['cards'] = result['invited_cards']

        return jsonify({"value": "done", "result": result,
        "winner": 'you' if result[enemy_key + 'hp'] <= 0 else 'enemy' if result[user_key + 'hp'] <= 0 else ''})
    except:
        return jsonify({"value": "error"})

def deal_card_damage(conn, result, card, affected):
    ccard = get_result(conn.execute('''SELECT damage, 0 as crit_chance, fire_damage, fire_time, poison_damage, poison_time, 
                                        defense, affect_next, affect_last FROM cards WHERE id = ?''', [card]))[0]
    ccard = {"damage": ccard[0], "crit_chance": ccard[1], "fire_damage": ccard[2], "fire_time": ccard[3], "poison_damage": ccard[4],
        "poison_time": ccard[5], "defense": ccard[6], "affect_next": ccard[7], "affect_last": ccard[8]}
    user_key = 'invitee_' if result['invitee_turn'] == 1 else 'invited_'
    enemy_key = 'invitee_' if result['invitee_turn'] == 0 else 'invited_'

    # result[enemy_key + 'hp'] -= max([ccard['damage'] - result[enemy_key + 'defense'], 0]) * \
    #     affected * \
    #     random.sample([1] * (40 - ccard['crit_chance']) + ([2] * ccard['crit_chance']), 1)[0]
    result[enemy_key + 'hp'] -= max([ccard['damage'] - result[enemy_key + 'defense'], 0]) * affected

    if ccard['fire_time'] > 0:
        fire_damage = numpy.floor(ccard['fire_damage'] if result[user_key + 'fire_damage'] == 0 else \
            (ccard['fire_damage'] + result[user_key+ 'fire_damage']) / 2)
        fire_time = numpy.floor(ccard['fire_time'] if result[user_key + 'fire_time'] == 0 else \
            (ccard['fire_time'] + result[user_key+ 'fire_time']) / 2)
        
        result[user_key + 'fire_damage'] = fire_damage
        result[user_key + 'fire_time'] = fire_time

    if ccard['poison_time'] > 0:
        poison_damage = numpy.floor(ccard['poison_damage'] if result[user_key + 'poison_damage'] == 0 else \
            (ccard['poison_damage'] + result[user_key+ 'poison_damage']) / 2)
        poison_time = numpy.floor(ccard['poison_time'] if result[user_key + 'poison_time'] == 0 else \
            (ccard['poison_time'] + result[user_key+ 'poison_time']) / 2)

        result[user_key + 'poison_damage'] = poison_damage
        result[user_key + 'poison_time'] = poison_time

    result[user_key + 'defense'] += ccard['defense']

def deal_effects_damage(conn, req):
    result = get_match(conn, req)
    user_key = 'invitee_' if result['invitee_turn'] == 1 else 'invited_'
    enemy_key = 'invitee_' if result['invitee_turn'] == 0 else 'invited_'
    if result[user_key + 'fire_time'] > 0:
        result[enemy_key + 'hp'] -= result[user_key + 'fire_damage']
        result[user_key + 'fire_time'] -= 1
        if result[user_key + 'fire_time'] < 1: result[user_key + 'fire_damage'] = 0
    if result[user_key + 'poison_time'] > 0:
        if len(result['last_move_cards']) > 3: result[enemy_key + 'hp'] -= result[user_key + 'poison_damage']
        result[user_key + 'poison_time'] -= 1
        if result[user_key + 'poison_time'] < 1: result[user_key + 'poison_damage'] = 0
    result['last_move_cards'] = ','.join([str(x) for x in req.get('cards')])
    set_values(conn, result)

def set_values(conn, result):
    conn.execute('''UPDATE matches SET
        invitee_turn = ?, invitee_cards = ?, invited_cards = ?, invitee_hp = ?, invited_hp = ?,
        invitee_fire_damage = ?, invitee_fire_time = ?, invited_fire_damage = ?, invited_fire_time = ?,
        invitee_poison_damage = ?, invitee_poison_time = ?, invited_poison_damage = ?, invited_poison_time = ?,
        invitee_defense = ?, invited_defense = ?, last_move_cards = ?
        WHERE id = ?''', [
            result['invitee_turn'], result['invitee_cards'], result['invited_cards'],
            result['invitee_hp'], result['invited_hp'], result['invitee_fire_damage'], result['invitee_fire_time'],
            result['invited_fire_damage'], result['invited_fire_time'], result['invitee_poison_damage'], result['invitee_poison_time'],
            result['invited_poison_damage'], result['invited_poison_time'], result['invitee_defense'], result['invited_defense'],
            result['last_move_cards'], result['id']])
    conn.commit()

def get_match(conn, req):
    result = get_result(conn.execute('''SELECT id, invitee_id, invited_id,
        invitee_deck, invited_deck, invitee_turn, invitee_cards, invited_cards, invitee_hp, invited_hp,
        invitee_fire_damage, invitee_fire_time, invited_fire_damage, invited_fire_time,
        invitee_poison_damage, invitee_poison_time, invited_poison_damage, invited_poison_time,
        invitee_defense, invited_defense, last_move_cards FROM matches WHERE id = ?''', [req.get('match_id')]))[0]
    
    result = { "id": result[0], "invitee_id": result[1], "invited_id": result[2], "invitee_deck": result[3], "invited_deck": result[4],
        "invitee_turn": result[5], "invitee_cards": result[6], "invited_cards": result[7], "invitee_hp": result[8], "invited_hp": result[9],
        "invitee_fire_damage": result[10], "invitee_fire_time": result[11], "invited_fire_damage": result[12], "invited_fire_time": result[13], 
        "invitee_poison_damage": result[14], "invitee_poison_time": result[15],"invited_poison_damage": result[16], "invited_poison_time": result[17], 
        "invitee_defense": result[18], "invited_defense": result[19], "last_move_cards": result[20]}
    return result