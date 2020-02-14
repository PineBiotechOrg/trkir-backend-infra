import os
import psycopg2 as psql
from kafka import KafkaProducer

DECODE_FORMAT = 'utf-8'
BUFFER_END = '\r\n'

# Списком через "," перечислять
KAFKA_SERVERS_TEXT = os.getenv('TRKIR_KAFKA_SERVERS')
KAFKA_SERVERS = KAFKA_SERVERS_TEXT.split(',')
PRODUCER = KafkaProducer(
    bootstrap_servers=KAFKA_SERVERS
)

DB_NAME = os.getenv('TRKIR_DB_NAME')
DB_USER = os.getenv('TRKIR_DB_USER')
DB_PASSWORD = os.getenv('TRKIR_DB_PASSWORD')
DB_HOST = os.getenv('TRKIR_DB_HOST')
DB_PORT = os.getenv('TRKIR_DB_PORT')

PSQL_CONN = psql.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

PSQL_CUR = PSQL_CONN.cursor()
