"""Entrypoint for nox."""

import nox

PYTHON_VERSION = '3.9.12'
POETRY_VERSION = '1.1.13'


@nox.session(reuse_venv=True, python=PYTHON_VERSION)
def cop(session: nox.Session) -> None:
    """Run all pre-commit hooks."""
    session.install(f"poetry=={POETRY_VERSION}")
    session.run("poetry", "install")
    session.run("poetry", "run", "pre-commit", "install")
    session.run(
        "poetry", "run", "pre-commit", "run", "--show-diff-on-failure", "--all-files"
    )
