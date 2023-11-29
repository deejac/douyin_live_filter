from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
app = Flask(__name__)

@app.route('/')
def home():
    # 加载 HTML 文件
    template = 'hls_player.html'
    return render_template(template)

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('/root/code/douyin_live_filter', path)

if __name__ == '__main__':
    #app.run(port=8000)
    app.run(host="0.0.0.0", port=8088, debug=True)
    CORS(app)