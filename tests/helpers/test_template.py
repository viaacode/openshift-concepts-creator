#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

import pytest
import yaml

from helpers.template import Template, __name__ as template_name


class TestTemplate:

    @pytest.fixture
    def template(self):
        app_name = "test"
        environment = "env"
        namespace = "ns"
        app_type = "web-app"

        return Template(
            app_name,
            namespace,
            environment,
            app_type
        )

    def test_render_template(self, template):

        template_yaml = yaml.safe_load(template.render_template())
        assert template_yaml["metadata"]["annotations"]["tags"] == f"{template.app_type}"
        assert template_yaml["metadata"]["name"] == f"{template.app_name}"
        # Template parameters
        assert template_yaml["parameters"][0]["name"] == "ENV"
        assert template_yaml["parameters"][0]["value"] == f"{template.environment}"
        assert template_yaml["parameters"][1]["name"] == "memory_requested"
        assert template_yaml["parameters"][1]["value"] == '0'
        assert template_yaml["parameters"][2]["name"] == "memory_limit"
        assert template_yaml["parameters"][2]["value"] == '0'
        assert template_yaml["parameters"][3]["name"] == "cpu_requested"
        assert template_yaml["parameters"][3]["value"] == '0'
        assert template_yaml["parameters"][4]["name"] == "cpu_limit"
        assert template_yaml["parameters"][4]["value"] == "0"

        # Service
        assert template_yaml["objects"][0]["metadata"]["labels"]["ENV"] == "${ENV}"
        assert template_yaml["objects"][0]["metadata"]["labels"]["app"] == template.app_name
        assert template_yaml["objects"][0]["metadata"]["name"] == f"{template.app_name}-${{ENV}}"
        assert template_yaml["objects"][0]["spec"]["selector"]["ENV"] == "${ENV}"
        assert template_yaml["objects"][0]["spec"]["selector"]["app"] == f"{template.app_name}"
        assert template_yaml["objects"][0]["spec"]["selector"]["type"] == template.app_type

        # DeploymentConfig
        assert template_yaml["objects"][1]["metadata"]["labels"]["ENV"] == "${ENV}"
        assert template_yaml["objects"][1]["metadata"]["labels"]["app"] == template.app_name
        assert template_yaml["objects"][1]["metadata"]["labels"]["type"] == template.app_type
        assert template_yaml["objects"][1]["metadata"]["name"] == f"{template.app_name}-${{ENV}}"
        assert template_yaml["objects"][1]["spec"]["selector"]["ENV"] == "${ENV}"
        assert template_yaml["objects"][1]["spec"]["selector"]["app"] == f"{template.app_name}"
        assert template_yaml["objects"][1]["spec"]["selector"]["type"] == template.app_type
        assert template_yaml["objects"][1]["spec"]["template"]["metadata"]["labels"]["ENV"] == "${ENV}"
        assert template_yaml["objects"][1]["spec"]["template"]["metadata"]["labels"]["app"] == template.app_name
        assert template_yaml["objects"][1]["spec"]["template"]["metadata"]["labels"]["type"] == template.app_type
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["livenessProbe"]
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["image"] == f"docker-registry.default.svc:5000/{template.namespace}/{template.app_name}"
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["name"] == template.app_name
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["cpu"] == "${cpu_limit}m"
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["memory"] == "${memory_limit}Mi"
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"]["cpu"] == "${cpu_requested}m"
        assert template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]["resources"]["requests"]["memory"] == "${memory_requested}Mi"
        assert template_yaml["objects"][1]["spec"]["triggers"][0]["imageChangeParams"]["containerNames"][0] == template.app_name
        assert template_yaml["objects"][1]["spec"]["triggers"][0]["imageChangeParams"]["from"]["name"] == f"{template.app_name}:${{ENV}}"
        assert template_yaml["objects"][1]["spec"]["triggers"][0]["imageChangeParams"]["from"]["namespace"] == f"{template.namespace}"
        assert not template_yaml['objects'][1]['spec']['template']['spec']['containers'][0].get('env')  # No env values

    def test_render_template_parameters(self, template):
        template.memory_requested = 256
        template.memory_limit = 512
        template.cpu_requested = 200
        template.cpu_limit = 400
        template.envs = ["env1", "env2"]

        template_yaml = yaml.safe_load(template.render_template())

        # Template parameters
        assert template_yaml["parameters"][1]["name"] == "memory_requested"
        assert template_yaml["parameters"][1]["value"] == '256'
        assert template_yaml["parameters"][2]["name"] == "memory_limit"
        assert template_yaml["parameters"][2]["value"] == '512'
        assert template_yaml["parameters"][3]["name"] == "cpu_requested"
        assert template_yaml["parameters"][3]["value"] == '200'
        assert template_yaml["parameters"][4]["name"] == "cpu_limit"
        assert template_yaml["parameters"][4]["value"] == '400'
        assert template_yaml["parameters"][4]["value"] == '400'
        assert template_yaml['objects'][1]['spec']['template']['spec']['containers'][0]['env'] == [
            {'name': 'env1', 'value': 'some_value'},
            {'name': 'env2', 'value': 'some_value'}
        ]

    def test_render_template_type_not_web(self, template):
        template.app_type = "exec"
        template_yaml = yaml.safe_load(template.render_template())

        # Does not exist because of type different than 'web-app'
        assert (template_yaml["objects"][1]["spec"]["template"]["spec"]["containers"][0]).get("livenessProbe") is None

    @patch(f"{template_name}.open")
    def test_create_template(self, open_mock, template):
        template.output_folder = "output"
        template.create_template()
        assert open_mock.call_args[0][0] == os.path.join("output", f"{template.app_name}-template-{template.environment}.yml")
        assert open_mock.call_args[0][1] == 'w'
        written_lines = open_mock().__enter__().writelines.call_args[0][0]
        template_yaml = yaml.safe_load(written_lines)
        assert template_yaml["metadata"]["name"] == (
            f"{template.app_name}"
        )

    def test_construct_folder_filename(self, template):
        template.output_folder = "output"
        assert template.construct_folder_filename() == (
            os.path.join("output", "test-template-env.yml")
        )
