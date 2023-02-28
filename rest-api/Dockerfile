From python:3.10.6-alpine3.16

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .

ENV HOST=0.0.0.0 PORT=8080

CMD ["python3", "entry_point.py"]
