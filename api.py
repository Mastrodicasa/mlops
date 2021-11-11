import argparse

from confluent_kafka import Consumer
from confluent_kafka import Producer

import ccloud_lib


def create_topics(params_conf, topic1, topic2):
    """
    Create the topics/ queues that will have the messages.

    :param params_conf: Parameters of the config file
    :param topic1: Name of the first topic
    :param topic2: Name of the second topic
    :return:
    """
    ccloud_lib.create_topic(params_conf, topic1)
    ccloud_lib.create_topic(params_conf, topic2)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
             description="Confluent Python Client example to produce messages \
                  to Confluent Cloud")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-f',
                          dest="config_file",
                          help="path to the configuration file",
                          required=True)
    required.add_argument('-t1',
                          dest="topic1",
                          help="1st topic name",
                          required=True)
    required.add_argument('-t2',
                          dest="topic2",
                          help="2nd topic name",
                          required=True)
    required.add_argument('-c',
                          dest="cloud_name",
                          help="either gc or kafka",
                          required=True)
    args = parser.parse_args()

    return args


def read_config(config_file, cloud_name):
    """Reads the config file"""
    if cloud_name == "kafka":
        conf = ccloud_lib.read_ccloud_config(config_file)
        # 'auto.offset.reset=earliest' to start reading from the beginning of the
        #   topic if no committed offsets exist
        params_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    else:
        params_conf = None
    return params_conf

# Optional per-message on_delivery handler (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    """Delivery report handler called on
    successful or failed delivery of message
    """
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))


def create_consumer(params_conf, cloud_name, consumer_group, auto_offset_reset="earliest"):
    if cloud_name == "kafka":
        consumer_conf = params_conf.copy()
        consumer_conf['group.id'] = consumer_group
        consumer_conf['auto.offset.reset'] = auto_offset_reset
        consumer = Consumer(consumer_conf)
    elif cloud_name == "gc":
        consumer = None
    else:
        consumer = None

    return consumer


def create_producer(params_conf, cloud_name):
    if cloud_name == "kafka":
        return Producer(params_conf)
    else:
        return None


def produce(producer, topic, record_key, record_value, callback, cloud_name):
    if cloud_name == "kafka":
        producer.produce(topic, key=record_key, value=record_value, on_delivery=callback)
    else:
        pass
