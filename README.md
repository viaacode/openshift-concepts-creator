# OpenShift concept creator

## Synopsis

A CLI Application which can create certain `OpenShift` concepts:

- Template existing of a service and a deploymentconfig.
  Represents an environment of an app (e.g. meemoo-app-qas).
- A Jenkins pipeline project in OpenShift.

At the moment, the application will only create yaml files which need to be loaded in in OpenShift.
It would be nice to have to automatically create these in OpenShift via API.

## Prerequisites

- Git
- Python 3.6+

## Usage

TODO

### Create pipeline

```bash
$ python create_pipeline.py --help
Usage: create_pipeline.py [OPTIONS]

Options:
  --app-name TEXT  Name of the app  [required]
  --help           Show this message and exit.
```

`python create_pipeline.py meemoo-app`

### Create template

```bash
$ python create_template.py --help
Usage: create_template.py [OPTIONS] APP ENVIRONMENT

  APP: The name of the app.

  ENVIRONMENT: Abbreviated name of environment e.g. qas

Options:
  --namespace TEXT            Name of the namespace.  [default: viaa-tools]
  --app-type [flask|exec]     Type of the app.  [required]
  --memory-requested INTEGER  Minimum requested memory in Mebibytes.
                              [default: 128]

  --cpu-requested INTEGER     Minimum requested CPU.  [default: 100]
  --memory-limit INTEGER      Maximum limit of memory in Mebibytes.  [default:
                              328]

  --cpu-limit INTEGER         Maximum limit of CPU.  [default: 300]
  --help                      Show this message and exit.
```

`python create_template.py --app-type=flask meemoo-app qas`

### Create jenkinsfile

```bash
$ python create_jenkinsfile.py --help
Usage: create_jenkinsfile.py [OPTIONS] APP

  APP: The name of the app.

Options:
  --namespace TEXT          Name of the namespace.  [default: viaa-tools]
  -o, --output-folder PATH  Folder to write the files to.  [default: .]
  --help                    Show this message and exit.
```

`python create_template.py meemoo-app`

## Tutorial

TODO