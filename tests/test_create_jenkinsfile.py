#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from unittest.mock import patch

from click.testing import CliRunner

from create_jenkinsfile import create_jenkinsfile, __name__ as create_jenkinsfile_name


@patch("shutil.copy")
@patch(f"{create_jenkinsfile_name}.open", create=True)
def test_create_jenkinsfile(open_mock, copy_mock):
    runner = CliRunner()
    result = runner.invoke(
        create_jenkinsfile, ["test", "--namespace", "namespace"]
    )
    assert result.exit_code == 0
    assert open_mock.call_count == 1
    assert open_mock().__enter__().writelines.call_count == 1

    assert copy_mock.call_count == 2
    assert copy_mock.call_args_list[0][0][0] == os.path.join(
        os.getcwd(), "templates", "jenkins", "Jenkinsfile"
    )
    assert copy_mock.call_args_list[0][0][1] == "./openshift/Jenkinsfile"
    assert copy_mock.call_args_list[1][0][0] == os.path.join(
        os.getcwd(), "templates", "jenkins", "wait4rollout.sh"
    )
    assert copy_mock.call_args_list[1][0][1] == "./openshift/wait4rollout.sh"
