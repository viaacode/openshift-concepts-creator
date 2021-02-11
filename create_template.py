#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import click

from helpers.template import Template


@click.command()
@click.argument("app")
@click.argument("environment")
@click.option(
    "--namespace",
    default="viaa-tools",
    help="Name of the namespace.",
    type=str,
    show_default=True,
)
@click.option(
    "--app-type",
    default="exec",
    help="Type of the app.",
    type=click.Choice(["web-app", "exec"], case_sensitive=False),
    show_default=True,
)
@click.option(
    "-o",
    "--output-folder",
    default=".",
    help="Folder to write the template to",
    type=str,
    show_default=True,
)
@click.option(
    "--memory-requested",
    default=128,
    help="Minimum requested memory in Mebibytes.",
    type=int,
    show_default=True,
)
@click.option(
    "--cpu-requested",
    default=100,
    help="Minimum requested CPU.",
    type=int,
    show_default=True,
)
@click.option(
    "--memory-limit",
    default=328,
    help="Maximum limit of memory in Mebibytes.",
    type=int,
    show_default=True,
)
@click.option(
    "--cpu-limit",
    default=300,
    help="Maximum limit of CPU.",
    type=int,
    show_default=True,
)
@click.option(
    "--env-file",
    help="Env file",
    type=click.File('r'),
)
def create_template(
    app,
    namespace,
    environment,
    app_type,
    output_folder,
    memory_requested,
    cpu_requested,
    memory_limit,
    cpu_limit,
    env_file,
):
    """
    APP: The name of the app.\n
    ENVIRONMENT: Abbreviated name of environment e.g. qas.
    """
    envs = []
    if env_file:
        try:
            envs = [env.split("=")[0] for env in env_file.readlines()]
        except Exception as e:
            raise click.ClickException(f"Error parsing the env file: {e}")

    template = Template(
        app,
        namespace,
        environment,
        app_type,
        output_folder=output_folder,
        memory_requested=memory_requested,
        cpu_requested=cpu_requested,
        memory_limit=memory_limit,
        cpu_limit=cpu_limit,
        envs=envs,
    )
    template.create_template()
    click.echo(f"Wrote template file ({template.construct_folder_filename()})")


if __name__ == "__main__":
    create_template()
