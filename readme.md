# Stackhub Py

## How to run it

Pull the Python image from Docker Hub:

`docker pull python:3.5.2`

Clone this repo. We will consider that your folder name is `stackhub`.

Run the Docker container with this command:

`$ docker run -it -v ~/stackhub:/python python:3.5.2 bash`

After, enter on the `python` folder at the root on container bash.

Run the following commands:

```
$ sh setup.sh
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install .
```

Run an example:

`$ python example.py`

If you exit the container and enter it again, make sure that you have run the source command.

