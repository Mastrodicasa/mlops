import json
import hashlib
import time

from keras.datasets import fashion_mnist
import numpy as np

import api


if __name__ == '__main__':

    # Read arguments and configuration file
    args = api.parse_args()
    print(args)
    config_file = args.config_file
    topic1 = args.topic1
    topic2 = args.topic2
    cloud_name = args.cloud_name
    params_conf = api.read_config(config_file, cloud_name)

    # Create topic if needed
    api.create_topics(params_conf, topic1, topic2)

    # Create Producer instance
    producer = api.create_producer(params_conf, cloud_name)

    # load dataset
    (train_x, train_y), (test_x, test_y) = fashion_mnist.load_data()
    test_x = test_x.reshape((test_x.shape[0], 28, 28, 1))

    # If you want to have a smaller dataset
    test_x = test_x[0:100, :, :, :]

    # Create a hash to be able to distinguish
    hash_dict = {}
    hash = hashlib.sha1()
    # step is the number of images in each message
    step = 5
    for i in range(0, len(test_x) - step, step):
        hash.update(str(time.time()).encode('utf-8'))
        value = test_x[i:i + step, :, :, 0].tolist()
        header = hash.hexdigest()
        hash_dict[header] = np.array(value)

        record_key = "req"
        record_value = json.dumps({"header": header, "value": value})
        print("Producing record: {}\t{}".format(record_key, header))
        api.produce(producer, topic1, record_key, record_value, api.acked, cloud_name)
        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        producer.poll(0)
        time.sleep(2)

    producer.flush()

    print("Create Consumer")
    consumer = api.create_consumer(params_conf, cloud_name, 'requestor_group', auto_offset_reset="earliest")

    # Subscribe to topic
    consumer.subscribe([topic2])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                data = json.loads(record_value)
                header = data['header']
                predictions = data['predictions']
                predictions = np.array(predictions)

                print("Consumed record with key {}, prediction {}".format(record_key, predictions))

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()