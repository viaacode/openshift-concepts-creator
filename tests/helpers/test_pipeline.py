#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pytest
from unittest.mock import patch

import yaml

from helpers.pipeline import Pipeline, __name__ as pipeline_name


class TestPipeline:

    @pytest.fixture
    def pipeline(self):
        app_name = "test"

        return Pipeline(
            app_name,
        )

    def test_render_template(self, pipeline):
        app_name = pipeline.app_name
        pipeline_yaml = yaml.safe_load(pipeline.render_template())

        assert pipeline_yaml["metadata"]["labels"]["app"] == app_name
        assert pipeline_yaml["metadata"]["labels"]["name"] == f"{app_name}-pipeline"
        assert pipeline_yaml["metadata"]["name"] == f"{app_name}-pipeline"
        assert pipeline_yaml["spec"]["source"]["git"]["uri"] == (
            f"https://github.com/viaacode/{app_name}.git"
        )

    @patch(f"{pipeline_name}.open")
    def test_create_pipeline(self, open_mock, pipeline):
        app_name = pipeline.app_name
        output_folder = "output"
        pipeline.output_folder = output_folder
        pipeline.create_pipeline()
        assert open_mock.call_args[0][0] == os.path.join(output_folder, f"{app_name}-pipeline.yml")
        assert open_mock.call_args[0][1] == 'w'
        written_lines = open_mock().__enter__().writelines.call_args[0][0]
        pipeline_yaml = yaml.safe_load(written_lines)
        assert pipeline_yaml["metadata"]["labels"]["app"] == app_name

    def test_construct_folder_filename(self, pipeline):
        pipeline.output_folder = "output"
        assert pipeline.construct_folder_filename() == (
            os.path.join("output", "test-pipeline.yml")
        )
