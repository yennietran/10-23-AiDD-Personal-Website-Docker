import os
import pytest


def test_projects_template_exists():
    """Check that the projects template file exists in templates/"""
    repo_root = os.path.dirname(os.path.dirname(__file__))
    template_path = os.path.join(repo_root, 'templates', 'projects.html')
    assert os.path.exists(template_path), f"Missing template: {template_path}"
