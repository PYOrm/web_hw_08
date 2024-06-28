import random

import pika
import faker
from models import Contact


class FakeContacts(Contact):
    fkr = faker.Faker()

    def __init__(self):
        super.__init__(cls)

    def new_contact(self):
        while True:
            self.fullname = self.fkr.name()
            self.email = self.fkr.email()
            self.phone = self.fkr.phone_number()
            self.address = self.fkr.address()
            self.sms_prefer = random.choice([True, False])
            yield Contact(**self.__dict__)


class QueueConnection:

    def __init__(self, user='guest', password='guest', host='localhost', port=5672):
        credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials))
        self.channel = connection.channel()

        self.channel.queue_declare(queue='send_email')
        self.channel.queue_declare(queue='send_sms')

    def __enter__(self, user, password, host, port):
        self.__init__(user, password, host, port)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def push_to_queue(self, obj: Contact):
        if obj.sms_prefer:
            self.channel.basic_publish(exchange='', routing_key='send_sms', body=obj.id.encode())
        else:
            self.channel.basic_publish(exchange='', routing_key='send_email', body=obj.id.encode())


def main():
    fake_contact_generator = FakeContacts()
    with QueueConnection() as qc:
        for _ in range(1, 10):
            new_contact = fake_contact_generator.new_contact()
            new_contact.save()
            qc.push_to_queue(new_contact)


if __name__ == "__main__":
    main()
