#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

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
        memory_requested: The requested memory allowed in OpenShift.
        cpu_requested: The requested CPU allowed in OpenShift
        memory_limit: The memory limit allowed in OpenShift
        cpu_limit: The CPU limit allowed in OpenShift.
    """

    def __init__(
        self,
        app_name,
        namespace,
        environment,
        app_type,
        memory_requested=0,
        cpu_requested=0,
        memory_limit=0,
        cpu_limit=0,
    ):

        self.app_name = app_name
        self.namespace = namespace
        self.environment = environment
        self.app_type = app_type
        self.memory_requested = memory_requested
        self.cpu_requested = cpu_requested
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit

    def render_template(self):
        """Loads in the jinja2 template and renders it."""
        jinja = JinjaTemplate(os.path.join(os.getcwd(), "templates", "openshift"))
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
        )

    def create_template(self):
        with open(os.path.join(os.getcwd(), f"template-{self.environment}.yml"), "w") as f:
            f.writelines(self.render_template())
