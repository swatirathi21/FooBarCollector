FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY foo_bar_collector.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python" , "./foo_bar_collector.py $SERVERS $ELASTICSEARCH_SERVER $ELASTICSEARCH_USERNAME $ELASTICSEARCH_PASSWORD"]