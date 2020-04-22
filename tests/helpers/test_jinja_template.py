#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import pytest
import yaml
from jinja2 import TemplateNotFound

from helpers.jinja_template import JinjaTemplate


class TestJinjaTemplate:
    @pytest.fixture
    def jinja_template(self):
        return JinjaTemplate(os.path.join(os.getcwd(), "tests", "resources"))

    def test_render_template(self, jinja_template):
        render = jinja_template.render_template(
            "jinja_template_example.yml", test="value"
        )
        render_yaml = yaml.safe_load(render)
        assert render_yaml["test"] == "value"

    def test_render_template_not_found(self, jinja_template):
        with pytest.raises(TemplateNotFound):
            jinja_template.render_template("doesnotexist.yml")
