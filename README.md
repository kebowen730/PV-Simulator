# PV-Simulator
Uses a RabbitMQ message broker to simulate electrical power values.


# Running the Simulator

Clone this repository, open a terminal and navigate to the PV-Simulator directory.

Create a Python3 virtual environment and run:
`pip3 install -r requirements.txt`


Start RabbitMQ with the following command:
`service rabbitmq-server start`


To run the simulator:
`python3 simulator/receive.py`
`python3 simulator/send.py`


# Running unit tests

Run the unit tests with:
`python3 -m pytest`