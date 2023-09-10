FROM python:3.11-slim

WORKDIR /usr/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y gcc python3-dev curl ffmpeg \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir models

RUN curl -JL -o ./models/ptBRfabermedium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
RUN curl -JL -o ./models/ptBRfabermedium.onnx.json https://huggingface.co/rhasspy/piper-voices/raw/v1.0.0/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "src/main.py" ]
