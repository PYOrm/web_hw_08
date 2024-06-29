from models import Contact, db_connection
from queue_ import QueueConnection
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('.env')

    rmq_user = config.get('RabbitMQ', 'user')
    rmq_pass = config.get('RabbitMQ', 'password')
    rmq_host = config.get('RabbitMQ', 'host')
    rmq_port = int(config.get('RabbitMQ', 'port'))

    db_connection()
    with QueueConnection(rmq_user, rmq_pass, rmq_host, rmq_port) as qc:
        qc.channel.start_consuming()


if __name__ == "__main__":
    main()
