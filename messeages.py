from flask import jsonify
from getResult import get_result
from threads import threads
import time, threading

def get(conn, req):
    try:
        result = get_result(conn.execute('''SELECT messeage, invitee_id, invited_id FROM messeages
            WHERE (invitee_id = ? AND invited_id = ?) OR (invitee_id = ? AND invited_id = ?)''', [
            int(req.get('invitee')), int(req.get('invited')), int(req.get('invited')), int(req.get('invitee'))]))
        return jsonify(result)
    except:
        return jsonify({"value": "error"})

def post(conn, req):
    try:
        id = get_result(conn.execute('SELECT id FROM messeages WHERE (invitee_id = ? AND invited_id = ?) OR (invitee_id = ? AND invited_id = ?)', [
            int(req.get('invitee')), int(req.get('invited')), int(req.get('invited')), int(req.get('invitee'))]))[0][0]
        threads['messeages'].get(id).clear()
        conn.execute('''INSERT INTO messeages(messeage, invitee_id, invited_id) VALUES(?, ?, ?)''', [
            req.get('messeage'), int(req.get('invitee')), int(req.get('invited'))])
        threads['messeages'].get(id).set()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def get_contacts(conn, req):
    try:
        result = conn.execute('''SELECT users.avatar, users.login, invites.invitee_id, invites.intited_id
            FROM friends WHERE friends.invitee_id = ? OR friends.invited_id = ?
            LEFT JOIN users ON invites.invitee_id = users.id OR invites.invited_id = users.id
            ORDER BY invites.init_date''', [int(req), int(req)])
        return jsonify(result)
    except:
        return jsonify({"value": "error"})

def wait(conn, req):
    try:
        id = get_result(conn.execute('SELECT id FROM messeages WHERE (invitee_id = ? AND invited_id = ?) OR (invitee_id = ? AND invited_id = ?)', [
        int(req.get('invitee')), int(req.get('invited')), int(req.get('invited')), int(req.get('invitee'))]))[0][0]
        threads["wait_messeages"].get(id).clear()
        threads['messeages'].get(id).clear()
        while not threads["wait_messeages"].get(id).is_set():
            if not threads['messeages'].get(id).wait(300):
                return jsonify({"value": "error"})
            return get(conn, req)
    except:
        return jsonify({"value": "error"})