import json

import numpy as np

from cnn_minst import CNNFashion
import api


if __name__ == '__main__':

    # Initialise the model
    cf = CNNFashion()
    cf.fit()

    # Read arguments and configurations
    args = api.parse_args()
    config_file = args.config_file
    topic1 = args.topic1
    topic2 = args.topic2
    cloud_name = args.cloud_name
    params_conf = api.read_config(config_file, cloud_name)

    # CREATE CONSUMER
    consumer = api.create_consumer(params_conf, cloud_name, "replier_group", auto_offset_reset="earliest")

    # CREATE PRODUCER
    producer = api.create_producer(params_conf, cloud_name)

    # POLL TOPIC 1
    # Subscribe to topic
    consumer.subscribe([topic1])
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
                # Read the message
                record_key = msg.key()
                record_value = msg.value()
                data = json.loads(record_value)
                header = data['header']
                value = data['value']
                value = np.array(value)
                print("In replier, consumed record with hash {}".format(header))

                # Predict the classes
                predictions = cf.predict(value)
                print("Prediction made")

                # Create the message: predictions and the hash
                record_key = "rep"
                record_value = json.dumps({"header": header, "predictions": predictions.tolist()})
                print("Predictions sent for message with hash: {}".format(header))

                # Publish the message on the second topic
                api.produce(producer, topic2, record_key, record_value, api.acked, cloud_name)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
        producer.flush()