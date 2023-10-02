from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_project.settings")
django.setup()

from sales_app.models import ProductVO


def update_product_vo(ch, method, properties, body):
    content = json.loads(body)
    title = content["title"]
    price = content["price"]
    description = content["description"]
    image = content["image"]
    category = content["category"]

    if title:
        ProductVO.objects.update_or_create(
            title=title,
            defaults={
                "price": price,
                "description": description,
                "image": image,
                "category": category
            },
        )
    else:
        ProductVO.objects.filter(title= title).delete()
while True:
    try:
        parameters = pika.ConnectionParameters(host="localhost", port=5672)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.exchange_declare(
            exchange="product_info",
            exchange_type="fanout",
        )

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange="product_info", queue=queue_name)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_product_vo,
            auto_ack=True,
        )

        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
