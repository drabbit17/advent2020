from invoke import task

APPS_TO_CHECK = "solutions/"

@task
def check(c):
    c.run(f"black --line-length 110 {APPS_TO_CHECK}")
    c.run(f"flake8 {APPS_TO_CHECK}")


