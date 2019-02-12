# portal_client

Python-based client for downloading data files hosted by the an instance of
the portal software developed by the GDC and further modified by the
Institute for Genome Sciences (IGS). There are several portals running on the
internet to support various research efforts. Notably, the Human Microbiome
Project Data Analysis and Coordination Center (hmpdacc.org) uses the portal
to enable data exploration and download. The client accepts a *manifest file*
as an input. This file contains URLs to the files to be downloaded. Manifest
files can be generated using the shopping cart functionality of the portal's
query interface.

## Installation

There are 2 basic ways to install portal_client:

1. Traditional installation
2. Using Docker

## 1. Traditional installation

The portal client requires Python 3 and the Boto library:

- [Python 3.6](https://www.python.org/downloads/release/python-361/)

- [boto](https://pypi.python.org/pypi/boto)

An easy way to install Python 3 and the necessary dependencies is to use Virtualenv.

### 2. Using Docker

The portal_client code comes bundled with a Dockerfile, which, when used, will
build a docker image with Python 3.6 as well as the dependencies specific to
the portal client. One can then use this Docker image to execute the client
using the following steps:

1. Build the image. Change to the directory containing the Dockerfile and execute:

```bash
docker build -t portal_client .
```

2. Use the built image to start a container and execute the client:

```bash
docker run -ti --rm portal_client portal_client --help
```

3. Test the container by downloading a few small files. The command below should
download two files to your current directory ($PWD). This works because we have
mapped your current working directory to the /tmp directory in the container with
the -v option, and we are executing the client in the /tmp directory with the use
of the -w option.

```bash
docker run -v "$PWD:/tmp" -w /tmp -ti --rm portal_client portal_client --url=https://raw.githubusercontent.com/IGS/portal_client/master/example_manifests/example_manifest.tsv
```

  * If running on EC2, this will automatically be detected and S3 will be the preferred endpoint. Example:

```bash
docker run -ti --rm -v "$PWD":/tmp -w /tmp portal_client portal_client --url=https://raw.githubusercontent.com/IGS/portal_client/master/example_manifests/example_manifest.tsv
```

  * If you wish to control which protocol/endpoint to prioritize, you can pass
a single endpoint or a comma-separated list (e.g. 'HTTP' or 'HTTP,S3,FTP').
For example, to override the S3 prioritized endpoint on an AWS EC2 instance with
the HTTP endpoint:

```bash
docker run -ti --rm -v "$PWD:/tmp" -w /tmp portal_client portal_client --url=https://raw.githubusercontent.com/IGS/portal_client/master/example_manifests/example_manifest.tsv --endpoint-priority=HTTP
```
