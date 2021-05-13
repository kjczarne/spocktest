# spocktest

Spocktest is a Python tool that runs tests for code snippets defined in standard Python files and injects them into documentation. Think of it as [doctest](https://docs.python.org/3/library/doctest.html) but the other way around.

## Motivation

The primary motivation behind Spocktest is the poor debuggability of tests generated with `sphinx-doctest`. While the standard `doctest` module does a good job of running code snippets against expected output, I've had much less luck with debugging `sphinx-doctest`.

I am currently of the belief that example code should be injected into documentation instead of the documentation to serve as a place to keep any tests and this repo will serve both as an experiment and as a potentially useful tool for building well-tested Wikis for Python software.

## Current status

Spocktest is in very early stages of development. Currently only a basic `assertEqual` and `assertNotEqual` `unittest` functions work with the test generation pattern. Documentation injection is pending and will likely be developed in the next few days.
