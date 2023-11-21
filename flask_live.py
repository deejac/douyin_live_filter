from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory('/Users/deejac/tmp/m3u8', path)

if __name__ == '__main__':
    app.run(port=8000)