from argparse import ArgumentParser
import gevent
import logging
from data_service.service import database
from data_service.database import dbi

logger = logging.getLogger(__name__)


def start_for_gevent(broker_url, database_url, rpc_queue, dbi_class=dbi.Dbi):
    try:
        worker = database.Worker(broker_url=broker_url, database_url=database_url, rpc_queue=rpc_queue,
                                 dbi_class=dbi_class)
        worker.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.info(str(e))


def start():
    parser = ArgumentParser()
    parser.add_argument("--broker-url", type=str, dest="broker_url", required=True, help="The url of mq broker.")
    parser.add_argument("--database-url", type=str, dest="database_url", required=True, help="The url of database")
    parser.add_argument("--max-worker", type=int, dest="max_worker", default=10,
                        help="Max number of database proccess.")
    parser.add_argument("--rpc-queue", type=str, dest="rpc_queue", default="happy_dinner_rpc_queue",
                        help="Name of receive message queue")
    args = parser.parse_args()
    broker_url = args.broker_url
    database_url = args.database_url
    max_worker = args.max_worker
    rpc_queue = args.rpc_queue

    event_list = []

    for i in range(max_worker):
        g = gevent.spawn(start_for_gevent, broker_url, database_url, rpc_queue)
        event_list.append(g)

    gevent.joinall(event_list)
