FROM python:3.9

COPY application /dash-app/

WORKDIR /dash-app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "./index.py" ]