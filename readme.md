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
$ sh configure.sh
```

Run an example:

`$ python example.py`

If you exit the container and enter it again, make sure that you have run the source command.

### Importer

To import the JSON data automatically to your MongoDB collections, run this command:

`$ python importer.py -l LOAD [-t TRUNCATE|-nt NOT TRUNCATE]`

The `-l|--load` argument must contain a string with the methods who will be run.

**Accepted methods:**

* github
* stackoverflow
* learning_curve
* lc_lang
* trends
* radar
* tiobe

e.g.:

`$ python importer.py -l 'github stackoverflow trends'`

The `-t|--truncate` argument is **optional** and delete all the documents from collection. **This argument is the default**.

The `-nt|--not-truncate` argument is **optional** and not delete the collection documents.

To show the help menu, type the `-h` flag.
