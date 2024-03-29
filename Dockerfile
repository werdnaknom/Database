FROM python:3.11

ENV HTTP_PROXY "http://proxy.jf.intel.com:912"
ENV HTTPS_PROXY "http://proxy.jf.intel.com:912"

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY app app
COPY Entities Entities
#COPY database_functions database_functions
COPY flaskweb.py boot.sh config.py ./
RUN chmod +x boot.sh

ENV FLASK_APP flaskweb.py

EXPOSE 5000

ENTRYPOINT [ "./boot.sh" ]

