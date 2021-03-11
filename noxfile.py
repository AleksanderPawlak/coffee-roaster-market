import nox_poetry


@nox_poetry.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "coffee_roaster_market", "manage.py")


@nox_poetry.session
def black(session):
    session.install("black")
    session.run("black", "--check", "coffee_roaster_market")


@nox_poetry.session
def tests(session):
    session.run("poetry", "install", external=True)
    # session.run('pytest')  # TODO: run pytest
