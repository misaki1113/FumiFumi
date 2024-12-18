from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

import threading
import time

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.setup_routes()
        self.data = {
            "score": 0,
            "level": 1,
            "bonus": 0,
            "next_point": 0,
            "ranking": [0, 0, 0],
        }

    def setup_routes(self):
        app = self.app

        @app.route('/')
        def home():
            return render_template('home.html')

        @app.route('/countdown')
        def countdown():
            return render_template('countdown.html')

        @app.route('/score')
        def score():
            return render_template('score.html')

        @app.route('/bonus')
        def bonus():
            return render_template('bonus.html')

        @app.route('/gameover')
        def gameover():
            return render_template('gameover.html')
        
        @app.route('/api/data', methods=['GET'])
        def get_data():
            self.data["score"] += 1
            return jsonify(self.data)
        
        @self.socketio.on("connect")
        def on_connect():
            print("client connected")

    def change_page(self, page_name):
        """
        サーバー側からクライアントにページ変更指示を送信する関数
        """
        valid_pages = {
            "home": "/",
            "countdown":"/countdown",
            "score":"/score",
            "bonus":"/bonus",
            "gameover":"/gameover"
        }

        if page_name in valid_pages:
            print(f"Changing page to: {page_name}")
            self.socketio.emit("navigate",{"url": valid_pages[page_name]})
        else:
            print(f"Invalid page:{page_name}")
    
    def background_task(self):
        # サーバー起動と並行して動作するバックグラウンドタスク
        pages = ["home", "countdown", "score", "bonus", "gameover"]
        while True:
            for page in pages:
                self.change_page(page)
                time.sleep(10)  # 5秒ごとにページを切り替え
    
    def run(self):
        threading.Thread(target=self.background_task, daemon=True).start()
        self.socketio.run(self.app, host="0.0.0.0" , port=5000, debug=True)

# Initialize and run the app
if __name__ == '__main__':
    app_instance = App()
    app_instance.run()
