#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

import yaml

from helpers.pipeline import Pipeline, __name__ as pipeline_name


class TestPipeline:

    def test_render_template(self):
        app_name = "test"
        pipeline = Pipeline(app_name)
        pipeline_yaml = yaml.safe_load(pipeline.render_template())

        assert pipeline_yaml["metadata"]["labels"]["app"] == app_name
        assert pipeline_yaml["metadata"]["labels"]["name"] == f"{app_name}-pipeline"
        assert pipeline_yaml["metadata"]["name"] == f"{app_name}-pipeline"
        assert pipeline_yaml["spec"]["source"]["git"]["uri"] == (
            f"https://github.com/viaacode/{app_name}.git"
        )

    @patch(f"{pipeline_name}.open")
    def test_create_pipeline(self, open_mock):
        app_name = "test"
        pipeline = Pipeline(app_name)
        pipeline.create_pipeline()
        assert open_mock.call_args[0][0] == os.path.join(os.getcwd(), "pipeline.yml")
        assert open_mock.call_args[0][1] == 'w'
        written_lines = open_mock().__enter__().writelines.call_args[0][0]
        pipeline_yaml = yaml.safe_load(written_lines)
        assert pipeline_yaml["metadata"]["labels"]["app"] == app_name
