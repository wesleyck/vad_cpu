import torch
import torchaudio
import math
from flask import Flask, jsonify, request

torch.set_num_threads(1)

from pprint import pprint

SAMPLING_RATE = 16000

USE_ONNX = True # change this to True if you want to test onnx model

app = Flask(__name__)
# load model
# repo_path = '/home/houck/project/silero-vad'
repo_path = '/home/'
model, utils = torch.hub.load(repo_or_dir=repo_path, source='local', model='silero_vad', onnx=USE_ONNX)
(get_speech_timestamps,
save_audio,
read_audio,
VADIterator,
collect_chunks) = utils

def merge_timestamps(speech_timestamps, time_seg, output_txt):
    time_stamp = []
    start_time = 0.0
    end_time = 0.0
    seg_dic = {}
    if not speech_timestamps:
        print('no speech in audio file! ')
        return 0
    else:
        start_time = speech_timestamps[0]['start']
        end_time = speech_timestamps[0]['end']
        if(len(speech_timestamps) == 1):
            time_stamp.append({'start': start_time, 'end': end_time})
            pprint(time_stamp)
            return 1
    for i in range(1, len(speech_timestamps)):
        cur_start = speech_timestamps[i]['start']
        cur_end =  speech_timestamps[i]['end']
        if (cur_start - end_time  < time_seg):
            end_time = cur_end
            # 处理最后一组
            if(i == len(speech_timestamps)-1):
                seg_dic = {}
                seg_dic['start'] = start_time
                seg_dic['end'] = end_time
                time_stamp.append(seg_dic)
            continue
        else:
            seg_dic = {}
            seg_dic['start'] = start_time
            seg_dic['end'] = end_time
            time_stamp.append(seg_dic)
            start_time = cur_start
            end_time = cur_end
            if(i == len(speech_timestamps)-1):
                seg_dic = {}
                seg_dic['start'] = start_time
                seg_dic['end'] = end_time
                time_stamp.append(seg_dic)
    string_timestamp = []
    with open(output_txt, 'w') as f:
        for time_seg_dic in time_stamp:
            line = 'start time: ' + str(math.floor(float(time_seg_dic['start']) / 60)) + 'm' + str(int(time_seg_dic['start']) % 60) + 's' + '   end time is: '\
            + str(math.floor(float(time_seg_dic['end']) / 60)) + 'm' + str(int(time_seg_dic['end']) % 60) + 's' + '\n'
            f.writelines(line)
            string_timestamp.append(line)
    # pprint(time_stamp)

    # return string_timestamp
    return time_stamp


@app.route('/')
def index():
    return "<p>welcome to audio vad model! </p>"

@app.route('/infer', methods=['POST', 'PUT'])
def inference():
    if request.method == 'POST':
        audio_file_path = request.form['audio_file_path']
        threshold = float(request.form['threshold'])
        max_segment_silence_time = float(request.form['max_segment_silence_time'])
        out_path = request.form['output_timestamp_path']
        assert 0.0 < threshold < 1.0
        # audio_data = request.get(file_link)
        wav = read_audio(audio_file_path)
        speech_timestamps = get_speech_timestamps(wav, model, threshold, sampling_rate=SAMPLING_RATE, return_seconds=True)
        timestamp = merge_timestamps(speech_timestamps, max_segment_silence_time, out_path)

        # 返回json数据结果，或者put上传到指定位置
        return jsonify({
            "success": 1,
            "audio_file_path": audio_file_path,
            "time_stamp": timestamp
            })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





