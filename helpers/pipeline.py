#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from helpers.jinja_template import JinjaTemplate


class Pipeline:
    """
    Represents and creates an OpenShift Jenkins pipeline project.

    Args:
        app_name: The name of the app.
    """

    def __init__(self, app_name):
        self.app_name = app_name

    def render_template(self):
        """Loads in the jinja2 template and renders it."""
        jinja = JinjaTemplate(os.path.join(os.getcwd(), "templates", "openshift"))
        return jinja.render_template("pipeline.yml", app_name=self.app_name)

    def create_pipeline(self):
        with open(os.path.join(os.getcwd(), "pipeline.yml"), "w") as f:
            f.writelines(self.render_template())
