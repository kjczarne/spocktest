from setuptools import setup, find_packages

DEPENDENCIES = [
    'toolz',
    'loguru'
]

with open("README.md", "r") as f:
    readme = f.read()


setup(
    name='spocktest',
    version='1.0.0',
    description='Embed unit test snippets into human-readable documentation',
    long_description=readme,
    author='Krzysztof Czarnecki',
    author_email='kjczarne@gmail.com',
    install_requires=DEPENDENCIES
)
