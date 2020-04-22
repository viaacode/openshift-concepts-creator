#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader


class JinjaTemplate:
    """ Helper class which facilitates in loading in and rendering Jinja2 templates"""

    def __init__(self, template_base_folder: str):
        self.env = Environment(
            loader=FileSystemLoader(template_base_folder),
        )

    def render_template(self, filename: str, **kwargs):
        return self.env.get_template(filename).render(**kwargs)
