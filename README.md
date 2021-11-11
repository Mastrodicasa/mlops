# MLOps

This code represents a requestor/replier situation like the one represented in `requestor_replier.png`.

The requestor sends packages of images (requests), the replier picks them up, predict the class of each image, and sends back the predictions (replies).

## Prepare your virtual environment

Create your virtual environment and then run

```bash
poetry install
```

## Run

Open a terminal and run 

```bash
python3 requestor.py -f kafka.config -t1 requests -t2 replies -c kafka
```

Arguments:
- -f: config file
- -t1: name of the first topic
- -t2: name of the second topic
- -c: cloud name


Open a second terminal and run

```bash
python3 replier.py -f kafka.config -t1 requests -t2 replies -c kafka
```

Arguments:
- -f: config file
- -t1: name of the first topic
- -t2: name of the second topic
- -c: cloud name

## What is happening?
The 2 queues are created if they don't exist.

Every set period of time, the requestor produces a package of 5 images is sent with a hash in the requests queue.

The replier polls the requests queue, and when a message arrives, the replier predicts the classes, and puts the prediction in the replies queue.

The requestor polls the replies queue and when a message arrives, it prints it.

## Config files fields
Kafka:
```python
bootstrap.servers= X
security.protocol=SASL_SSL 
sasl.mechanisms=PLAIN 
sasl.username=X
sasl.password=X
```

Google Cloud:
```python
{
  "type": "service_account",
  "project_id": X,
  "private_key_id": X,
  "private_key": X,
  "client_email": X,
  "client_id": X,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": X
}
```

## Train the CNN Model
```python
from cnn_minst import CNNFashion

cf = CNNFashion()
# If no data given by the user
cf.fit()
# If data given by the user
cf.fit(trainX, trainY)
```
If the data is given by user,
- trainX must be a numpy.ndarray, with shape (X, 28, 28)
- trainY must be a numpy.ndarray, with shape (X)