from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

# import threading
import time
import concurrent.futures

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.setup_routes()
        self.state_data = {
            "score": 0,
            "level": 0,
            "bonus": 0,
            "next_point": 2000,
            "ranking": [0, 0, 0],
        }
        self.bonus_data = [0, 0, 0]

    def setup_routes(self):
        app = self.app

        @app.route('/css/<path:filename>')
        def serve_css(filename):
            return send_from_directory('templates/css', filename)
        
        # templates/js内のJSファイルを提供するルート
        @app.route('/js/<path:filename>')
        def serve_js(filename):
            return send_from_directory('templates/js', filename)
        
        @app.route('/img/<path:filename>')
        def serve_img(filename):
            return send_from_directory('templates/img', filename)

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
            self.data["score"] += 3.5
            return jsonify(self.data)
        
        @self.socketio.on("connect")
        def on_connect():
            print("client connected")

    def change_page(self, page_name):
        """
        サーバー側からクライアントにページ変更指示を送信する関数
        """
        time.sleep(5)
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
    
    # def background_task(self):
    #     # サーバー起動と並行して動作するバックグラウンドタスク
    #     pages = ["home", "countdown", "bonus", "gameover"]
    #     while True:
    #         for page in pages:
    #             self.change_page(page)
    #             if(page == "countdown"):
    #                 time.sleep(10)
    #             time.sleep(10)  
    
    def run(self):
        # threading.Thread(target=self.background_task, daemon=True).start()
        self.socketio.run(self.app, host="0.0.0.0" , port=5000, debug=True)

# Initialize and run the app
if __name__ == '__main__':
    app_instance = App()

   
