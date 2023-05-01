from typer.testing import CliRunner

from demo_cookiecutter_api.cli import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello, data science." in result.stdout
