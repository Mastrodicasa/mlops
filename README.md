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
