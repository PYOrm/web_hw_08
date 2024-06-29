import random
import faker
from models import Contact, db_connection
from queue_ import QueueConnection
import configparser


class FakeContacts(Contact):
    fkr = faker.Faker()

    def new_contact(self, qty) -> Contact:
        for _ in range(0, qty):
            cont = dict()
            cont["fullname"] = self.fkr.name()
            cont["email"] = self.fkr.email()
            cont["phone"] = self.fkr.phone_number()
            cont["address"] = self.fkr.address()
            cont["sms_prefer"] = random.choice([True, False])
            yield Contact(**cont)


def main():
    config = configparser.ConfigParser()
    config.read('.env')

    rmq_user = config.get('RabbitMQ', 'user')
    rmq_pass = config.get('RabbitMQ', 'password')
    rmq_host = config.get('RabbitMQ', 'host')
    rmq_port = int(config.get('RabbitMQ', 'port'))

    db_connection()
    fake_contact_generator = FakeContacts()
    with QueueConnection(rmq_user, rmq_pass, rmq_host, rmq_port) as qc:
        for new_contact in fake_contact_generator.new_contact(10):
            new_contact = new_contact.save()
            qc.push_to_queue(new_contact)


if __name__ == "__main__":
    main()
