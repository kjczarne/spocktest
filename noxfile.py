import nox


@nox.session
def test(session: nox.Session):
    session.install('.')
    session.run('python', '-m', 'unittest')


@nox.session
def whl(session: nox.Session):
    session.install('wheel', 'setuptools')
    session.run('python', '-m', 'setup', 'bdist_wheel')


@nox.session
def send(session: nox.Session):
    session.install('twine')
    session.run('twine', 'upload', 'dist/*')
