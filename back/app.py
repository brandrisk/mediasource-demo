import os
import json
import uuid
import subprocess
from flask import Flask, send_from_directory, Response, request
from dotenv import load_dotenv

load_dotenv()

ORIGIN = os.getenv('ORIGIN') or 'http://localhost:3000'

app = Flask(__name__)

TEMP_DIR = 'temp'
VIDEOS_DIR = 'videos'
BENTO_DIR = 'bento'

def get_path(*args):
    return os.path.join(os.getcwd(), *args)

@app.route('/list')
def get_video_list():
    vids = []

    for _, _, files in os.walk(get_path(VIDEOS_DIR)):
        vids.extend(files)

    resp = Response(json.dumps(vids))
    resp.headers['Access-Control-Allow-Origin'] = ORIGIN
    return resp

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        file = request.files['video']
        filename = f'{str(uuid.uuid4())}.mp4'

        while os.path.exists(get_path(VIDEOS_DIR, filename)):
            filename = f'{str(uuid.uuid4())}.mp4'

        path_in = get_path(TEMP_DIR, filename)
        file.save(path_in)
        mp4fragment_path = get_path(BENTO_DIR, 'bin', 'mp4fragment.exe')
        path_out = get_path(VIDEOS_DIR, filename)
        p = subprocess.Popen([mp4fragment_path, path_in, path_out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        os.remove(path_in)

        if stderr and not os.path.exists(path_out):
            raise Exception()

        resp = Response(filename)
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp
    except:
        os.remove(path_in)
        resp = Response('')
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp


@app.route('/codecs/<videoname>')
def get_codecs(videoname):
    mp4info_path = get_path(BENTO_DIR, 'bin', 'mp4info.exe')
    path = get_path(VIDEOS_DIR, videoname)

    try:
        p = subprocess.Popen([mp4info_path, '--fast', '--format', 'json', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        
        if stderr:
            raise Exception()
        
        data = json.loads(stdout.decode())
        tracks = data['tracks']
        codecs = [track['sample_descriptions'][0]['codecs_string'] for track in tracks if track['type'] in ['Audio', 'Video']]
        codecs_string = ','.join(codecs)

        resp = Response(codecs_string)
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp
    except:
        resp = Response('')
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp

@app.route('/video/<filename>')
def get_video(filename):
    try:
        resp = send_from_directory(VIDEOS_DIR, filename)
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp
    except:
        resp = Response('')
        resp.headers['Access-Control-Allow-Origin'] = ORIGIN
        return resp

@app.before_first_request
def start():
    if not os.path.exists(get_path(TEMP_DIR)):
        os.mkdir(get_path(TEMP_DIR))
    if not os.path.exists(get_path(VIDEOS_DIR)):
        os.mkdir(get_path(VIDEOS_DIR))

if __name__ == '__main__':
    app.run()
