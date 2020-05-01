#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from helpers.pipeline import Pipeline


@click.command()
@click.argument('app')
@click.option(
    "-o",
    "--output-folder",
    default=".",
    help="Folder to write the pipeline to",
    type=str,
    show_default=True,
)
def create_pipeline(app, output_folder):
    """ APP: The name of the app. """
    pipeline = Pipeline(app, output_folder=output_folder)
    pipeline.create_pipeline()
    click.echo(f"Wrote pipeline file ({pipeline.construct_folder_filename()})")


if __name__ == "__main__":
    create_pipeline()
