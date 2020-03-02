import pika
import random


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='meter')

    channel.basic_consume(
        queue='meter', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    pv = random.random()*9000
    decoded_body = body.decode()
    watts = float(decoded_body.split()[-1])
    total = pv + watts
    print('Received Body: {}'.format(decoded_body))
    log = '{}   PV Watts: {}   Total Watts: {} \n'.format(decoded_body, pv, total)
    with open('results.txt', 'a') as file:
        file.write(log)


if __name__ == '__main__':
    main()
