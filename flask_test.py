from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def play_video():
    # video_path = '/path/to/your/video.mp4'
    video_path = 'D:\\anime\\hositsuku\\1.mp4'
    video_path = 'C:\\Users\\AAO\\Videos\\123.mp4'
    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
