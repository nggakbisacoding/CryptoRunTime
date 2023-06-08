import json
from os import path

PATH_DATA = path.join(path.dirname(__file__), r'data.json')

def load_json(path_data):
    try:
        with open(path_data, 'r') as f:
            data = json.load(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'File database tidak ditemukan', keep_on_top=True, background_color='red', text_color='white')
        data = {}
    return data
    
data = load_json(PATH_DATA)
splitx = data['status']['timestamp'].split(':')
clock = splitx[0].split('T')
sec = splitx[2].split('.')
print(clock[0])
print(clock[0],str(int(clock[1])+7),":",str(splitx[1]),":",str(sec[0]))