[![Build Status](https://travis-ci.org/arXain/pyXain.svg?branch=master)](https://travis-ci.org/arXain/pyXain)
[![Coverage Status](https://coveralls.io/repos/github/arXain/pyXain/badge.svg?branch=master)](https://coveralls.io/github/arXain/pyXain?branch=master)

**Getting Started**

Make sure you have the following packages installed on a python3 environment
* ipfsapi
* flask
* requests

Using anaconda you can do this with
```
conda create -n pyxain python=3.6
source activate pyxain
pip install flask requests ipfsapi
```

Then in the pyXain/ directory, run

```
pip install --editable .
export FLASK_APP=pyxain.api
export FLASK_DEBUG=true
flask run
```

to install the pyxain package and run the api server at `localhost:5000`.

You also must run have an ipfs daemon running in a separate terminal

```
ipfs daemon
```

You can now view the landing page on (http:///127.0.0.1:5000)

Note: every time you open a new terminal session and want to run the node, you need to enter both of the export statements.

**Testing**

All code should be tested and placed in the pyXain/tests/ directory in their respective files. Each module
has its own test module.
