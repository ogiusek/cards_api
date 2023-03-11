from flask import jsonify
from getResult import get_result

def get(conn):
    try:
        res = get_result(conn.execute("SELECT * FROM cards"))
        result = []
        for element in res:
            result.append({'id': element[0], 'title': element[1], 'image': element[2], 'card_pos': element[3],
                'damage': element[4], 'crit_chance': element[5], 'fire_damage': element[6],
                'fire_time': element[7], 'poison_damage': element[8], 'poison_time': element[9],
                'defense': element[10], 'affect_next': element[11], 'affect_last': element[12]})
        return jsonify(result)
    except:
        return jsonify({"value": "error"})

def post(conn, req):
    try:
        conn.execute('''INSERT INTO cards(
            title, image, card_pos, damage, crit_chance, 
            fire_damage, fire_time, venom_damage, venom_time, defense, affect_next, affect_last) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', [
                req.get('title'), req.get('image'), req.get('card_pos'), req.get('damage'), req.get('crit_change'),
                req.get('fire_damage'), req.get('fire_time'), req.get('venom_damage'), req.get('venom_time'), req.get('defense'), 
                req.get('affect_next'), req.get('affect_last')])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def remove(conn, req):
    try:
        conn.execute('''DELETE FROM cards WHERE id = ?''', [int(req.get('id'))])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})