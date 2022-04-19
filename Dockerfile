# FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime
# RUN  pip install -i https://mirrors.cloud.tencent.com/pypi/simple flask onnxruntime
# # pip3 install torch==1.10.2+cpu torchvision==0.11.3+cpu torchaudio==0.10.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html\
# COPY vad.py utils_vad.py hubconf.py  files/ /home/ 
# # COPY files/ /home/
# CMD [ "python", "vad.py" ]
# # RUN pip install  onnxruntime

RUN sed -i "s/archive.ubuntu./mirrors.aliyun./g" /etc/apt/sources.list
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "s/security.debian.org/mirrors.aliyun.com\/debian-security/g" /etc/apt/sources.list
FROM python:3.8-slim 
RUN  pip install --no-cache-dir -i https://mirrors.cloud.tencent.com/pypi/simple flask onnxruntime 
RUN  pip install --no-cache-dir -i https://mirrors.cloud.tencent.com/pypi/simple torch torchvision torchaudio
# RUN  pip install ffmpeg 
# COPY vad.py util_vad.py hubconf.py files/ /home/ 
# CMD  python vad.py 