from kombu import Connection, Queue
from kombu.mixins import ConsumerProducerMixin
import pickle
from data_service.database import Base
from data_service.utils import exception


class Worker(ConsumerProducerMixin):

    def __init__(self, broker_url, database_url, rpc_queue, dbi_class):
        self.connection = Connection(broker_url)
        self.rpc_queue = Queue(rpc_queue)
        self.dbi_class = dbi_class
        self.database_url = database_url

    def get_consumers(self, Consumer, channel):
        return [Consumer(
            queues=[self.rpc_queue],
            on_message=self.on_request,
            accept={'application/json'},
            prefetch_count=1,
        )]

    def on_request(self, message):
        try:
            payload = message.payload
            func_name, args, kwargs = pickle.loads(payload)
            if issubclass(self.dbi_class, Base):
                dbi_obj = self.dbi_class(database_url=self.database_url)
                if hasattr(dbi_obj, func_name):
                    func = getattr(dbi_obj, func_name)
                    result = pickle.dumps(func(*args, **kwargs))
                else:
                    e = exception.RpcHasNotMethod("Rpc has not method named: {}".format(func_name))
                    result = pickle.dumps(e)
            else:
                result = pickle.dumps(exception.NotImplementBaseClass("{} is not sub class of Base".format(self.dbi_class)))
        except Exception as e:
            result = pickle.dumps(e)
        self.producer.publish(
            result,
            exchange='', routing_key=message.properties['reply_to'],
            correlation_id=message.properties['correlation_id'],
            serializer='pickle',
            retry=True,
        )
        message.ack()
