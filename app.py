from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import re

app = Flask(__name__)

def extract_video_id(url):
    video_id = re.search(r"(?<=v=)[^&]+", url)
    if not video_id:
        video_id = re.search(r"(?<=be/)[^&]+", url)
    return video_id.group(0) if video_id else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    url = request.form['url']
    try:
        yt = YouTube(url)
        video_id = extract_video_id(url)
        video_details = {
            'title': yt.title,
            'streams': yt.streams.filter(progressive=True) if request.form['download_type'] == 'video' else yt.streams.filter(only_audio=True)
        }
        return render_template('download.html', video_details=video_details, download_type=request.form['download_type'], video_id=video_id, url=url)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_type = request.form['download_type']
    itag = request.form['itag']
    
    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        
        download_path = stream.download()
        
        return send_file(download_path, as_attachment=True)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
