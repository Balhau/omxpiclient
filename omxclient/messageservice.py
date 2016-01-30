from kafka import SimpleProducer,KafkaClient

class MessageService:

    def __init__(self,kafkaBroker,kafkaTopic):
        self.broker=kafkaBroker
        self.topic=kafkaTopic;
        self.client=KafkaClient(self.broker)
        self.producer=SimpleProducer(self.client)

    def sendMessage(self,message):
        self.producer.send_messages(self.topic,message)
