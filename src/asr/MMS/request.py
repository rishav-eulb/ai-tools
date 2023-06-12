import subprocess
import urllib.request
import wave
import base64
import json
import os

class MMSModelRequest():
    def __init__(self, audio_path, lang):
        """ Initializes the request object with the given parameters"""
        self.audio_path = load_data(
            audio_path, of='raw')  # Call the load_data function here to set the audio_path attribute
        self.lang = lang

    def to_json(self):
        """ Returns the JSON representation of the object"""
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def load_data(wavpath, of='raw', **extra):
    if of == 'raw':
        orig = wavpath
        tmp_file = orig + "_temp.wav"
        subprocess.call(['ffmpeg', '-i', orig, '-ar', '16k', '-ac',
                        '1', '-hide_banner', '-loglevel', 'error', tmp_file])
        os.rename(tmp_file, orig)

        return orig
    elif of == 'url':
        lang = extra['lang']
        if not os.path.exists('../downloaded/' + lang + '/'):
            os.makedirs('../downloaded/' + lang + '/')
        urllib.request.urlretrieve(
            wavpath, '../downloaded/' + lang + '/' + os.path.split(wavpath)[1])
        print('url downloaded')
        return load_data('../downloaded/' + lang + '/' + os.path.split(wavpath)[1])
    elif of == 'bytes':
        lang = extra['lang']
        name = extra['bytes_name']
        if not os.path.exists('../downloaded/' + lang + '/'):
            os.makedirs('../downloaded/' + lang + '/')
        with wave.open('../downloaded/' + lang + '/' + name, 'wb') as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(16000)
            file.writeframes(base64.b64decode(wavpath))
        return '../downloaded/' + lang + '/' + name
    else:
        raise "Not implemented"
