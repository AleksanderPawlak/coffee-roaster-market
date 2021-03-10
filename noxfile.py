from nox_poetry import session


@session
def lint(session):
    session.install("flake8")
    session.run("flake8", "coffee_roaster_market", "manage.py")
