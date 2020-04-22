#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from helpers.pipeline import Pipeline


@click.command()
@click.argument('app')
def create_pipeline(app):
    """ APP: The name of the app. """
    Pipeline(app).create_pipeline()


if __name__ == "__main__":
    create_pipeline()
