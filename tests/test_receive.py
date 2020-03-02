from simulator.receive import callback, main
from unittest.mock import Mock, patch, call
import pika
import random


def test_callback():
    random.seed(42)
    open('results.txt', 'w').close()

    callback(None, None, None, b'TESTDATE   Meter Watts: 4573')

    with open('results.txt') as file:
        test_line = file.readline()
        assert test_line == 'TESTDATE   Meter Watts: 4573   PV Watts: 5754.841186120953   Total Watts: 10327.841186120953 \n'




@patch('pika.BlockingConnection')
@patch('simulator.receive.callback')
def test_main(mock_callback, mock_blocking_connection):
    mock_conn = Mock()
    mock_channel = Mock()
    mock_conn.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_conn

    main()

    mock_blocking_connection.assert_called_once_with(pika.ConnectionParameters(host='localhost'))
    mock_conn.channel.assert_called_once_with()
    mock_channel.queue_declare.assert_called_once_with(queue='meter')
    mock_channel.basic_consume.assert_called_once_with(queue='meter', on_message_callback=mock_callback, auto_ack=True)
    mock_channel.start_consuming.assert_called_once_with()
