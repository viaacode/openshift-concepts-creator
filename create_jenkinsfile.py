#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

import click
from pathlib import Path

from helpers.jinja_template import JinjaTemplate


@click.command()
@click.argument("app")
@click.option(
    "--namespace",
    default="viaa-tools",
    type=str,
    help="Name of the namespace.",
    show_default=True
)
@click.option(
    "-o",
    "--output-folder",
    default=".",
    type=click.Path(),
    help="Folder to write the files to.",
    show_default=True
)
def create_jenkinsfile(app, namespace, output_folder):
    """ APP: The name of the app. """
    # Assemble openshift folder to write to.
    output_folder = os.path.join(output_folder, "openshift")
    # Create openshift subfolder if not yet exists.
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    input_folder = os.path.join(os.getcwd(), "templates", "jenkins")

    # Load in and render Makefile with CLI parameters.
    jinja = JinjaTemplate(input_folder)
    makefile_string = jinja.render_template(
        "Makefile",
        app_name=app,
        namespace=namespace
    )
    with open(os.path.join(output_folder, "Makefile"), "w") as f:
        f.writelines(makefile_string)

    # Jenkinsfile and wait4rollout have no variables so just copy.
    shutil.copy(
        os.path.join(input_folder, "Jenkinsfile"),
        os.path.join(output_folder, "Jenkinsfile"),
    )
    shutil.copy(
        os.path.join(input_folder, "wait4rollout.sh"),
        os.path.join(output_folder, "wait4rollout.sh"),
    )


if __name__ == "__main__":
    create_jenkinsfile()
