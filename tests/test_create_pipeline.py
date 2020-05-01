#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from unittest.mock import patch

from click.testing import CliRunner

from create_pipeline import create_pipeline

APP_NAME = "test"

PARAMS_MANDATORY = [
    APP_NAME,
]


def _invoke_runner(params):
    runner = CliRunner()
    result = runner.invoke(
        create_pipeline,
        params,
    )
    return result


@patch('create_pipeline.Pipeline')
def test_create_pipeline_minimal(pipeline_mock):
    result = _invoke_runner(PARAMS_MANDATORY)
    assert result.exit_code == 0
    assert pipeline_mock.call_args[0][0] == APP_NAME
    # CLI defaults
    assert pipeline_mock.call_args[1]["output_folder"] == "."

    assert pipeline_mock().create_pipeline.call_count == 1


@patch('create_pipeline.Pipeline')
def test_create_pipeline_optional_parameters(pipeline_mock):
    template_params = copy.deepcopy(PARAMS_MANDATORY)
    template_params += ["--output-folder", "output"]
    result = _invoke_runner(template_params)
    assert result.exit_code == 0
    assert pipeline_mock.call_args[1]["output_folder"] == "output"
    assert pipeline_mock().create_pipeline.call_count == 1


@patch("create_pipeline.Pipeline")
def test_create_pipeline_stdout(pipeline_mock):
    pipeline_mock().construct_folder_filename.return_value = "filename"
    result = _invoke_runner(PARAMS_MANDATORY)
    assert result.output == f"Wrote pipeline file (filename)\n"
    assert result.exit_code == 0
