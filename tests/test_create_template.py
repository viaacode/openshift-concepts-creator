#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from unittest.mock import patch

from click.testing import CliRunner

from create_template import create_template

APP_NAME = "test"
NAMESPACE = "ns"
ENVIRONMENT = "env"
APP_TYPE = "flask"
PARAMS_MANDATORY = [
    APP_NAME,
    ENVIRONMENT,
    "--namespace", NAMESPACE,
    "--app-type", APP_TYPE,
]


def _invoke_runner(params):
    runner = CliRunner()
    result = runner.invoke(
        create_template,
        params,
    )
    return result


@patch("create_template.Template")
def test_create_template_minimal(template_mock):
    result = _invoke_runner(PARAMS_MANDATORY)
    assert result.exit_code == 0
    assert template_mock.call_args[0][0] == APP_NAME
    assert template_mock.call_args[0][1] == NAMESPACE
    assert template_mock.call_args[0][2] == ENVIRONMENT
    assert template_mock.call_args[0][3] == APP_TYPE

    # CLI defaults
    assert template_mock.call_args[1]["memory_requested"] == 128
    assert template_mock.call_args[1]["cpu_requested"] == 100
    assert template_mock.call_args[1]["memory_limit"] == 328
    assert template_mock.call_args[1]["cpu_limit"] == 300
    assert template_mock().create_template.call_count == 1


@patch("create_template.Template")
def test_create_template_parameters(template_mock):
    template_params = copy.deepcopy(PARAMS_MANDATORY)
    template_params += [
        "--memory-requested", 256,
        "--memory-limit", 512,
        "--cpu-requested", 200,
        "--cpu-limit", 400,
    ]
    result = _invoke_runner(template_params)
    assert result.exit_code == 0

    assert template_mock.call_args[1]["memory_requested"] == 256
    assert template_mock.call_args[1]["cpu_requested"] == 200
    assert template_mock.call_args[1]["memory_limit"] == 512
    assert template_mock.call_args[1]["cpu_limit"] == 400
    assert template_mock().create_template.call_count == 1
