FROM python:3.11

WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./files /src/files

CMD ["python3", "files/run_all.py"]