#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest.mock import patch

from click.testing import CliRunner

from create_pipeline import create_pipeline


@patch('create_pipeline.Pipeline')
def test_create_pipeline(pipeline_mock):
    app_name = "test"
    runner = CliRunner()
    result = runner.invoke(create_pipeline, [app_name])
    assert result.exit_code == 0
    assert pipeline_mock.call_args[0][0] == app_name
    assert pipeline_mock().create_pipeline.call_count == 1
