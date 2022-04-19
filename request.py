
import requests

url = "http://192.168.199.86:5000/infer"
payload = {
            'audio_file_path': './vad_test.wav', 
            'threshold': 0.5, 
            'max_segment_silence_time': 5,
            'output_timestamp_path': './time_stamp.txt'
            }

                    # files={"audio_file": open('./vad_test.wav','rb')})

with open('data.lst', 'r') as f:
    audio_list = f.readlines()
    for audio_path in audio_list:
        audio_path = audio_path.split()
        payload['audio_file_path'] = audio_path
        resp = requests.post(url, data=payload)
        # print(resp.text)


