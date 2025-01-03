from confluent_kafka import Producer
import asyncio
import psycopg2

class IngesionData:
    def kafka_producer(data, topic, kafka_config):
        producer = Producer(kafka_config)
        producer.produce(topic, value=data)
        producer.flush

    