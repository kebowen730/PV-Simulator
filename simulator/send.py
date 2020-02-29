import pika
import random
from datetime import datetime, timedelta


def main():
    second = timedelta(seconds=1)
    time = datetime.now()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='meter')

    for i in range(86400):
        time = time + second
        send_message(time, channel)
    connection.close()


def send_message(time, channel):
    watts = random.random()*9000
    message = '{}   Meter Watts: {}'.format(time, watts)
    channel.basic_publish(exchange='', routing_key='meter', body=message)
    print('Sent  {}'.format(watts))




if __name__ == '__main__':
    main()