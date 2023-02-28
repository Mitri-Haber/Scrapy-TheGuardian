From python:3.10.6-alpine3.16

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY . .

CMD ["python3", "entry_point.py"]