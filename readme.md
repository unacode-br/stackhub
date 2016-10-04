# Stackhub Py

## How to run it

Pull the Python image from Docker Hub:

`docker pull python:3.5.2`

Clone this repo. We will consider that your folder name is `unacode`.

Run the Docker container with this command:

`$ docker run -it -v ~/unacode:/python python:3.5.2 bash`

After, enter on the `python` folder at the root on container bash.

Run the following commands:

```
$ sh setup.sh
$ source venv/bin/activate
$ pip install -r requirements.txt
```
