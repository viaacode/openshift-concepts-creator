#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from helpers.jinja_template import JinjaTemplate


class Pipeline:
    """
    Represents and creates an OpenShift Jenkins pipeline project.

    Args:
        app_name: The name of the app.
        output_folder: Folder to write the pipeline file to.
    """

    def __init__(self, app_name: str, output_folder: str = os.getcwd()):
        self.app_name = app_name
        self.output_folder = output_folder

    def render_template(self):
        """Loads in the jinja2 template and renders it."""
        jinja = JinjaTemplate(os.path.join(os.getcwd(), "templates", "openshift"))
        return jinja.render_template("pipeline.yml", app_name=self.app_name)

    def construct_folder_filename(self) -> str:
        name = f"{self.app_name}-pipeline.yml"
        return os.path.join(self.output_folder, name)

    def create_pipeline(self):
        with open(self.construct_folder_filename(), "w") as f:
            f.writelines(self.render_template())
