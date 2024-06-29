import time
import pika
from models import Contact

class QueueConnection:

    def __init__(self, user, password, host, port):
        credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='send_email', durable=True)
        self.channel.queue_declare(queue='send_sms', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='send_sms', on_message_callback=self.do_job)
        self.channel.basic_consume(queue='send_email', on_message_callback=self.do_job)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def push_to_queue(self, obj: Contact):
        if obj.sms_prefer:
            self.channel.basic_publish(exchange='', routing_key='send_sms', body=str(obj.id).encode(),
                                       properties=pika.BasicProperties(
                                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        else:
            self.channel.basic_publish(exchange='', routing_key='send_email', body=str(obj.id).encode(),
                                       properties=pika.BasicProperties(
                                           delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    def do_job(self, ch, method, properties, body):
        contact = Contact.objects(id=body.decode())[0]
        time.sleep(1)
        match method.routing_key:
            case 'send_sms':
                print(f"sms was send for {contact.phone}")
                contact.update(msg_send=True)
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
            case 'send_email':
                print(f"email was send for {contact.email}")
                contact.update(msg_send=True)
                self.channel.basic_ack(delivery_tag=method.delivery_tag)
            case _:
                print(f'No callback function set for queue "{ch}"')
