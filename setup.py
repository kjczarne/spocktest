from setuptools import setup, find_packages

DEPENDENCIES = [
    'toolz',
    'loguru'
]

with open("README.md", "r") as f:
    readme = f.read()


setup(
    name='spocktest',
    entry_points={
        'console_scripts': [
            'spocktest = spocktest.main:main',
        ],
    },
    version='1.0.3',
    description='Embed unit test snippets into human-readable documentation',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Krzysztof Czarnecki',
    author_email='kjczarne@gmail.com',
    install_requires=DEPENDENCIES,
    packages=find_packages()
)
