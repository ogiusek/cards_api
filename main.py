from flask import Flask, request
from flask_cors import CORS
import sqlite3

import messeages, invites, cards, decks, wait_matches
from init import init
from users import change, login_register
import match

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': ['http://gallery.simplecreator.pl', 'http://localhost:3000']}})
conn = sqlite3.connect('./database/database.db', check_same_thread=False)

# @app.before_request
# def block_other_origins():
#     if request.headers.get('origin') != 'http://localhost:3000' and \
#         request.headers.get('origin') != 'http://gallery.simplecreator.pl':
#         return 'Invalid origin', 403

@app.route('/register/', methods=["POST"])
def register():
    return login_register.register(conn, request.json)

@app.route('/login/', methods=["POST"])
def login():
    return login_register.login(conn, request.json)

@app.route('/guest/create/', methods=["POST"])
def create_guest():
    return login_register.create_guest(conn, request.json)

@app.route('/change/login/', methods=["POST"])
def change_login():
    return change.change_login(conn, request.json)

@app.route('/change/password/', methods=["POST"])
def change_password():
    return change.change_password(conn, request.json)

@app.route('/change/avatar/', methods=["POST"])
def change_avatar():
    return change.change_avatar(conn, request.json)

@app.route('/invite/', methods=["POST"])
def invite_():
    return invites.invite(conn, request.json)

@app.route('/invite/cancel/', methods=["POST"])
def cancel_invite():
    return invites.cancel(conn, request.json)

@app.route('/invite/accept/', methods=["POST"])
def accept_invite():
    return invites.accept(conn, request.json)

@app.route('/friends/remove/', methods=["POST"])
def remove_friend():
    return invites.remove_friend(conn, request.json)

@app.route('/invited/', defaults={'path': ''})
@app.route('/invited/<int:path>', methods=['GET'])
def get_invited(path):
    return invites.get_invited(conn, path)

@app.route('/invites/', defaults={'path': ''})
@app.route('/invites/<int:path>', methods=['GET'])
def get_invites(path):
    return invites.get_invites(conn, path)

@app.route('/friends/', defaults={'path': ''})
@app.route('/friends/<int:path>', methods=['GET'])
def get_friends(path):
    return invites.get_friends(conn, path)

@app.route('/contacts/', defaults={'path': ''})
@app.route('/contacts/<int:path>', methods=['GET'])
def get_contacts(path):
    return messeages.get_contacts(conn, path)

@app.route('/messeages/post/', methods=["POST"])
def post_messeage():
    return messeages.post(conn, request.json)

@app.route('/messeages/get/', defaults={'path': ''})
@app.route('/messeages/get/<path:path>', methods=['GET'])
def get_messeage(path):
    req = { 'invitee': path.split('/')[0], 'invited': path.split('/')[1]}
    return messeages.get(conn, req)

@app.route('/messeages/wait/', defaults={'path': ''})
@app.route('/messeages/wait/<path:path>', methods=['GET'])
def messeage_wait(path):
    req = { 'invitee': path.split('/')[0], 'invited': path.split('/')[1]}
    return messeages.get(conn, req)

@app.route('/cards/get/', methods=['GET'])
def get_card():
    return cards.get(conn)

@app.route('/cards/post/', methods=['POST'])
def post_card():
    return cards.post(conn, request.json)

@app.route('/cards/delete/', methods=['DELETE'])
def delete_card():
    return cards.remove(conn, request.json)

@app.route('/decks/get/', defaults={'path':''})
@app.route('/decks/get/<int:path>', methods=['GET'])
def get_deck(path):
    return decks.get(conn, path)

@app.route('/decks/post/', methods=['POST'])
def post_deck():
    return decks.post(conn, request.json)

@app.route('/decks/update/', methods=['PATCH'])
def update_deck():
    return decks.update(conn, request.json)

@app.route('/decks/delete/', methods=['DELETE'])
def delete_deck():
    return decks.delete(conn, request.json)

@app.route('/match/find/', methods=['POST'])
def find_match():
    return wait_matches.get_match(conn, request.json)

@app.route('/match/stop/', methods=['DELETE'])
def stop_match():
    return wait_matches.stop_match(conn, request.json)

@app.route('/match/play/', methods=['POST'])
def play_match():
    return match.play(conn, request.json)

if __name__ == '__main__':
    init.init(app, conn)