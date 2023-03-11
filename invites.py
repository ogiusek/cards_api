from flask import jsonify
from getResult import get_result
import threading
from threads import threads

def invite(conn, req):
    try:
        conn.execute('''IF NOT EXISTS(SELECT * FROM invites WHERE invitee_id = ? AND invited_id = ?)
        INSERT INTO invites(invitee_id, invited_id) VALUES(?, ?)''', [
            int(req.get('invitee')), int(req.get('invited')), int(req.get('invitee')), int(req.get('invited'))])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def cancel(conn, req):
    try:
        conn.execute('''DELETE FROM invites WHERE invited_id = ? AND invitee_id = ?''', [
            int(req.get('invited')), int(req.get('invitee'))])
        conn.commit()
        return jsonify({"value":"done"})
    except:
        return jsonify({"value": "error"})


def accept(conn, req):
    try:
        conn.execute('''IF NOT EXISTS(SELECT * FROM invites WHERE invitee_id = ? AND invited_id = ?) BEGIN
            DELETE FROM invites WHERE invitee_id = ? AND invited_id = ?
            INSERT INTO friends(invitee_id, invited_id) VALUES(?, ?)
        END''',[int(req.get('invitee')), int(req.get('invited')), 
            int(req.get('invitee')), int(req.get('invited')), 
            int(req.get('invitee')), int(req.get('invited'))])
        conn.commit()
        id = get_result(conn.execute('SELECT id FROM messeages WHERE (invitee_id = ? AND invited_id = ?) OR (invitee_id = ? AND invited_id = ?)', [
            int(req.get('invitee')), int(req.get('invited')), int(req.get('invited')), int(req.get('invitee'))]))[0][0]
        threads['messeages'][id] = threading.Event()
        threads['wait_messeages'][id] = threading.Event()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})


def remove_friend(conn, req):
    try:
        conn.execute('''DELETE FROM friends WHERE invitee_id = ? AND invited_id = ?''',[
            int(req.get('invitee')), int(req.get('invited'))])
        conn.commit()
        id = get_result(conn.execute('SELECT id FROM messeages WHERE (invitee_id = ? AND invited_id = ?) OR (invitee_id = ? AND invited_id = ?)', [
            int(req.get('invitee')), int(req.get('invited')), int(req.get('invited')), int(req.get('invitee'))]))[0][0]
        threads['messeages'].pop(id)
        threads['wait_messeages'].pop(id)
        return jsonify({"value":"done"})
    except:
        return jsonify({"value": "error"})

def get_invited(conn, req):
    try:
        result = get_result(conn.execute('''SELECT users.id, users.login, users.avatar 
        FROM invites WHERE invites.invitee_id = ?
        LEFT JOIN users ON invites.invited_id = users.id''', [int(req)]))
        return jsonify({"value": result})
    except:
        return jsonify({"value": "error"})

def get_invites(conn, req):
    try:
        result = get_result(conn.execute('''SELECT users.id, users.login, users.avatar 
        FROM invites WHERE invites.invited_id = ?
        LEFT JOIN users ON invites.invited_id = users.id''', [int(req)]))
        return jsonify({"value": result})
    except:
        return jsonify({"value": "error"})

def get_friends(conn, req):
    try:
        result = get_result(conn.execute('''SELECT users.id, users.login, users.avatar 
        FROM friends WHERE friends.invited_id = ? OR friends.invitee_id = ?
        LEFT JOIN users ON friends.invited_id = users.id''', [int(req), int(req)]))
        return jsonify({"value": result})
    except:
        return jsonify({"value": "error"})