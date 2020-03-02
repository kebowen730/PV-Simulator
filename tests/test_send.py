from app.send import send_message, main
from unittest.mock import Mock, patch, call
import pika
import random
from datetime import datetime
from freezegun import freeze_time
from freezegun.api import FakeDatetime


@freeze_time('2019-01-02 03:04:05')
def test_send_message():
    mock_channel = Mock()
    random.seed(42)
    time = datetime.now()

    send_message(time, mock_channel)
    mock_channel.basic_publish.assert_called_once_with(body='2019-01-02 03:04:05   Meter Watts: 5754.841186120953', exchange='', routing_key='meter')

@freeze_time('2019-01-02 03:04:05')
@patch('pika.BlockingConnection')
@patch('app.send.send_message')
def test_main(mock_send_message, mock_blocking_connection):
    mock_conn = Mock()
    mock_channel = Mock()
    mock_conn.channel.return_value = mock_channel
    mock_blocking_connection.return_value = mock_conn

    main()

    mock_blocking_connection.assert_called_once_with(pika.ConnectionParameters(host='localhost'))
    mock_conn.channel.assert_called_once_with()
    mock_channel.queue_declare.assert_called_once_with(queue='meter')
    assert mock_send_message.call_count == 86400
    assert mock_send_message.call_args_list[0] == call(FakeDatetime(2019, 1, 2, 3, 4, 6), mock_channel)
    assert mock_send_message.call_args_list[1] == call(FakeDatetime(2019, 1, 2, 3, 4, 7), mock_channel)
    assert mock_send_message.call_args_list[86399] == call(FakeDatetime(2019, 1, 3, 3, 4, 5), mock_channel)
    mock_conn.close.assert_called_once_with()
    