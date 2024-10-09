import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from src.game.game_logic import Game
from src.data.session_manager import SessionManager
from config import Config

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='../../../static')
    app.config.from_object(Config)

    @app.context_processor
    def inject_sessions():
        sessions = SessionManager.load_sessions()
        return dict(sessions=sessions['sessions'])

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/play')
    def play():
        session_id = session.get('game_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            session['game_id'] = session_id
        game = Game(session_id)
        stimulus_word = game.get_stimulus_word()
        return render_template('play.html', stimulus_word=stimulus_word)

    @app.route('/submit_response', methods=['POST'])
    def submit_response():
        response = request.form['response']
        session_id = session.get('game_id')
        if not session_id:
            return jsonify({"error": "No active game session"}), 400
        game = Game(session_id)
        result = game.process_response(response)
        if result["game_ended"]:
            session.pop('game_id', None)  # Clear the game_id from the session
            result["redirect"] = url_for('index')  # Add the redirect URL
        return jsonify(result)

    @app.route('/graph')
    def graph():
        # Implement graph visualization here
        return render_template('graph.html')
    
    @app.route('/session/<session_id>')
    def show_session(session_id):
        session_data = SessionManager.load_session(session_id)
        return render_template('session.html', session=session_data)

    return app