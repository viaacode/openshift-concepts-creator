#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List

from helpers.jinja_template import JinjaTemplate


class Template:
    """
    Represents and creates an OpenShift template existing
    of a service and deploymentconfig. Concretely this models
    an environment of an app e.g. meemoo-app-qas

    Args:
        app_name: The name of the app.
        namespace: The OpenShift project to create the template in.
        environment: The environment (qas, int, prd).
        app_type: The type of app.
        output_folder: Folder to write the template file to.
        memory_requested: The requested memory allowed in OpenShift.
        cpu_requested: The requested CPU allowed in OpenShift
        memory_limit: The memory limit allowed in OpenShift
        cpu_limit: The CPU limit allowed in OpenShift.
    """

    def __init__(
        self,
        app_name: str,
        namespace: str,
        environment: str,
        app_type: str,
        output_folder: str = os.getcwd(),
        memory_requested: int = 0,
        cpu_requested: int = 0,
        memory_limit: int = 0,
        cpu_limit: int = 0,
        envs: List = [],
    ):
        self.app_name = app_name
        self.namespace = namespace
        self.environment = environment
        self.app_type = app_type
        self.output_folder = output_folder
        self.memory_requested = memory_requested
        self.cpu_requested = cpu_requested
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.envs=envs

    def render_template(self):
        """Loads in the jinja2 template and renders it."""
        jinja = JinjaTemplate(os.path.join(os.getcwd(), "templates", "openshift"),)
        return jinja.render_template(
            "template.yml",
            app_name=self.app_name,
            namespace=self.namespace,
            environment=self.environment,
            type=self.app_type,
            memory_requested=self.memory_requested,
            cpu_requested=self.cpu_requested,
            memory_limit=self.memory_limit,
            cpu_limit=self.cpu_limit,
            envs=self.envs,
        )

    def construct_folder_filename(self) -> str:
        name = f"{self.app_name}-template-{self.environment}.yml"
        return os.path.join(self.output_folder, name)

    def create_template(self):
        with open(self.construct_folder_filename(), "w") as f:
            f.writelines(self.render_template())
