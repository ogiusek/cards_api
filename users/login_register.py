from flask import jsonify
from getResult import get_result

def login(conn, req):
    try:
        result = get_result(conn.execute('''SELECT * FROM users
                        WHERE login = ? AND password = ?''', [ req.get('login'),  req.get('password')]))
        if len(result) == 1:
            res = result[0]
            return jsonify({"value": res})
        else:
            return jsonify({"value": "error"})
    except:
        return jsonify({"value": "error"})


def register(conn, req):
    try:
        if len(req.get('login')) > 4:
            result = get_result(conn.execute('''SELECT * FROM users
                WHERE login = ? AND password = ?''', [
                req.get('login'), req.get('password')]))
            if len(result) > 0:
                return jsonify({"value": "exists"})
            
            conn.execute('''INSERT INTO users(login, password) VALUES(?, ?)''',[
                req.get('login'), req.get('password')])
            conn.commit()
            return jsonify({"value": result})
        else:
            return jsonify({"value": "error"})
    except:
        return jsonify({"value": "error"})

def create_guest(conn, req):
    try:
        user = "guest" + str(get_result(conn.execute('SELECT COUNT(*) FROM users'))[0][0])
        conn.execute('''INSERT INTO users(login, password) VALUES(?,?)''',[
            user, 0])
        conn.commit()
        return jsonify({"value": "done", "user": user})
    except:
        return jsonify({"value": "error"})