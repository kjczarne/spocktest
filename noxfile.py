import nox
import shutil


@nox.session
def test(session: nox.Session):
    session.install('.')
    session.run('python', '-m', 'unittest')


@nox.session
def clear(session: nox.Session):
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)


@nox.session
def whl(session: nox.Session):
    session.install('wheel', 'setuptools')
    session.run('python', '-m', 'setup', 'bdist_wheel')


@nox.session
def send(session: nox.Session):
    session.install('twine')
    session.run('twine', 'upload', 'dist/*')
