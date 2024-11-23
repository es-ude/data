# UDE Intelligent Embedded Systems (IES) Data

The library collects utilities to download data used for research and teaching.
In the future we might add some very basic tools for preprocessing.

## Installation

### Simple Approach

Make sure you have at least `python3.10` installed.
Then you can install the package via

```bash
$ pip install git+ssh://git@github.com:es-ude/data.git
```

### Recommended Approach

We recommend to install the [uv package manager](https://docs.astral.sh/uv/#getting-started).
Afterwards you can use

```bash
$ uv init --python 3.12 my-project
$ cd my-project
$ uv python install python3.12
$ uv add git+ssh://git@github.com:es-ude/data.git
$ uv sync
$ source .venv/bin/activate
```

## Usage


### Downloading

You can use

```python
from iesude.data import MitBihAtrialFibrillationDataSet as AFDataSet

d = AFDataSet.download("my_data_dir")
```

This will download the data from our public sciebo share into a tmp directory
and extract the contents into a folder called `my_data_dir`.

### Adding Your Data

You need write access to our [sciebo share](https://uni-duisburg-essen.sciebo.de/s/pWPghcaiYFhz6BW).
Upload your dataset, preferrably as a zip file, since support for compressed tar archives is not implemented yet.
Assuming you stored your data under `"myproject/dataset01.zip"`.
You define your new dataset like so

```python
from iesude.data import DataSet, Zip as ZipArchive

class MyNewDataSet(DataSet):
    file_path = "myproject/dataset01.zip"
    file_type = ZipArchive
```



## Features

- automatic download from UDE IES sciebo share
- automatic archive extraction into a given folder
- supported file types are
  * `.zip` archive
  * uncompressed `.tar` archive
  * plain files (download a file directly to your folder without extraction)


## Todo

- [ ] `tar.gz`
- [ ] `tar.xz`
- [ ] override share endpoint in user config
- [ ] upload data sets
- [ ] automatically put descriptions/readmes for uploaded datasets in github repo
- [ ] autogenerate classes when uploading a data set


## Contribution

To contribute, clone the repository and install uv (link in the install section).
Additionally also install pre-commit, e.g., like so

```bash
$ uv tool install pre-commit
```

Alternatively you can use [devenv](https://devenv.sh/) environment for reproducible, declarative and easy to use setup. It will take care of

- installing `uv` and calling it to install python and the dev dependencies
- most importantly it will install and setup pre-commit

Follow the 2 steps from the devenv [getting started guide](https://devenv.sh/getting-started/).

Additionally, we recommend you use [direnv](https://direnv.net/docs/installation.html#from-system-packages) to activate devenv automatically upon entering the project in a shell (also supported by several IDE/Editor plugins).
