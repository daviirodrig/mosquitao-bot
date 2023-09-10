FROM python:3.10-slim

WORKDIR /usr/app

COPY requirements.txt ./

RUN apt-get update

RUN apt-get install curl -y

RUN mkdir models

RUN curl -JL -o ./models/ptBRfabermedium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
RUN curl -JL -o ./models/ptBRfabermedium.onnx.json https://huggingface.co/rhasspy/piper-voices/raw/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json

RUN apt-get install ffmpeg -y

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "src/main.py" ]
