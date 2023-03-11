from flask import jsonify
from getResult import get_result

def get(conn, req):
    try:
        result = get_result(conn.execute('''SELECT * FROM decks WHERE user_id = ? ORDER BY init_date DESC''', [int(req)]))
        return jsonify(result)
    except:
        return jsonify({"value": "error"})

def post(conn, req):
    deck = req.get('deck').split(',') if isinstance(req.get('deck'), str) else req.get('deck')
    try:
        if len(deck) == 14:
            strDeck = ",".join([str(x) for x in deck])
            conn.execute('DELETE FROM decks WHERE user_id = ? AND deck = ?', [int(req.get('user_id')), strDeck])
            conn.execute('INSERT INTO decks(user_id, deck) VALUES(?, ?)', [int(req.get('user_id')), strDeck])
            conn.commit()
            newDeckId = get_result(conn.execute('SELECT id from decks WHERE user_id = ? AND deck = ?', [int(req.get('user_id')), strDeck]))[0][0]
            return jsonify({"value": "done", "id": newDeckId})
        else:
            return jsonify({"value": "error"})
    except:
        return jsonify({"value": "error"})

def update(conn, req):
    try:
        deck = req.get('deck') if isinstance(req.get('deck'), str) else ','.join(str(num) for num in req.get('deck'))
        if len(deck.split(',')) == 14:
            conn.execute('DELETE FROM decks WHERE deck = ? AND user_id = ?', [deck, int(req.get('user_id'))])
            conn.execute('UPDATE decks SET deck = ? WHERE id = ?', [deck, int(req.get('id'))])
            conn.commit()
            return jsonify({"value": "done"})
        else:
            return jsonify({"value": "error"})
    except:
        return jsonify({"value": "error"})

def delete(conn, req):
    try:
        conn.execute('''DELETE FROM decks WHERE id = ?''', [int(req.get('id'))])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})