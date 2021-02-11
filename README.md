# OpenShift concepts creator

## Synopsis

A CLI Application which can create certain `OpenShift` concepts:

- Template existing of a service and a deploymentconfig.
  Represents an environment of an app (e.g. meemoo-app-qas).
- A Jenkins pipeline project in OpenShift.

It also provides generating a `Jenkinsfile` containing the declarative steps and the `Makefile` and additional script(s)
to run the steps.

At the moment, the application will only create yaml files which need to be loaded in in OpenShift.
It would be nice to have to automatically create these in OpenShift via API.

## Prerequisites

- Git
- Python 3.6+

## Usage

* Start by creating a virtual environment:

```bash
$ python -m venv ./venv
```

* Activate the virtual environment:

```bash
$ source ./venv/bin/activate
```

* Install the external modules:

```bash
$ (venv) pip install -r requirements.txt && pip install -r requirements-test.txt
```

### Create pipeline

```bash
$ python create_pipeline.py --help
Usage: create_pipeline.py [OPTIONS] APP

  APP: The name of the app.

Options:
  -o, --output-folder TEXT  Folder to write the pipeline to  [default: .]
  --help                    Show this message and exit.
```

`python create_pipeline.py meemoo-app`

### Create template

```bash
$ python create_template.py --help
Usage: create_template.py [OPTIONS] APP ENVIRONMENT

  APP: The name of the app.

  ENVIRONMENT: Abbreviated name of environment e.g. qas.

Options:
  --namespace TEXT            Name of the namespace.  [default: viaa-tools]
  --app-type [web-app|exec]   Type of the app.  [default: exec]
  -o, --output-folder TEXT    Folder to write the template to  [default: .]
  --memory-requested INTEGER  Minimum requested memory in Mebibytes.
                              [default: 128]
  --cpu-requested INTEGER     Minimum requested CPU.  [default: 100]
  --memory-limit INTEGER      Maximum limit of memory in Mebibytes.  [default:
                              328]
  --cpu-limit INTEGER         Maximum limit of CPU.  [default: 300]
  --env-file FILENAME         Env file
  --help                      Show this message and exit.
```

`python create_template.py meemoo-app qas`

### Create jenkinsfile

```bash
$ python create_jenkinsfile --help
Usage: create_jenkinsfile.py [OPTIONS] APP

  APP: The name of the app.

Options:
  --namespace TEXT          Name of the namespace.  [default: viaa-tools]
  -o, --output-folder PATH  Folder to write the files to.  [default: .]
  --help                    Show this message and exit.
```

`python create_jenkinsfile.py meemoo-app`

## Tutorial

TODO