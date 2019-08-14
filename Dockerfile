FROM python:3.7

RUN apt-get update
RUN apt-get install -y \
            gcc \
            libc6-dev \
            python3-dev \
            libffi-dev \
            python-dev \
            sqlite3 \
            wkhtmltopdf \
            muscle

COPY requirements /requirements
RUN pip install -r /requirements/requirements.txt

COPY wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR /code
COPY . .

ENTRYPOINT ["/entrypoint.sh"]
