from flask import jsonify

def change_avatar(conn, req):
    try:
        conn.execute('''UPDATE users SET avatar = ? WHERE login = ?''', 
        [req.get('new_avatar'), req.get('login')])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def change_password(conn, req):
    try:
        conn.execute('''UPDATE users SET password = ? WHERE login = ?''', 
        [req.get('new_password'), req.get('login')])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})

def change_login(conn, req):
    try:
        conn.execute('''UPDATE users SET login = ? WHERE login = ?''', 
        [req.get('new_login'), req.get('login')])
        conn.commit()
        return jsonify({"value": "done"})
    except:
        return jsonify({"value": "error"})