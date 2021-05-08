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
def mypy(session):
    session.install(
        "mypy",
        "django-stubs",
        "django-environ",
        "psycopg2-binary",
        "django-rest-framework",
    )
    session.run("mypy", "coffee_roaster_market")


@nox_poetry.session
def tests(session):
    session.install(
        "coverage",
        "Django",
        "django-rest-framework",
        "django-environ",
        "factory-boy",
        "pytest",
        "pytest-django",
        "psycopg2-binary",
    )
    session.run("coverage", "run", "-m", "pytest")  # TODO: run pytest
