# spocktest

Spocktest is a Python tool that runs tests for code snippets defined in standard Python files and injects them into documentation. Think of it as [doctest](https://docs.python.org/3/library/doctest.html) but the other way around.

## Motivation

The primary motivation behind Spocktest is the poor debuggability of tests generated with `sphinx-doctest`. While the standard `doctest` module does a good job of running code snippets against expected output, I've had much less luck with debugging `sphinx-doctest`.

I am currently of the belief that example code should be injected into documentation instead of the documentation to serve as a place to keep any tests and this repo will serve both as an experiment and as a potentially useful tool for building well-tested Wikis for Python software.

## Current status

Spocktest is in early stages of development. If used in production, it's **recommended you always create a copy of the output documentation with `--output` flag** to prevent any latent bugs from clobbering your documentation source files. Apart from that make sure to **keep your documentation under VCS**!

## How it works

* A **snippet** is defined as a portion of code in a unit test file between an ID portion and a comment that ends the snippet, e.g.

    ```python
    def test_snippet_1(self):
        a = 1
        a += 1
        # SNIPPET_END
        self.assertEqual(a, 2)
    ```

    As you can see the ending tag is useful to focus the snippet on the relevant code and omit testing boilerplate.

* A **placeholder** is defined as a pattern that will be substituted with a concrete snippet, e.g.

    ````markdown
    # Doc1

    ```python
    # --Snippet--: 1
    ```
    ````

* The **defaults are configured for Python** but nearly all behavior is configurable with Regex patterns:

  * By default all snippet tests should be named: `test_snippet_{{ID}}`.
    * Can be overridden with `--pattern` flag.
  * By default `# SNIPPET_END` is the default ending tag.
    * Can be overridden with `--end` flag.
  * **All patterns must be matched exactly** e.g. `#SNIPPET_END` will not work!
  * By default placeholders are written as `# --Snippet--: {{ID}}`.
    * Can be overridden with `--target-pattern` flag.
  * By default `.md` and `.rst` files are supported for substitution.
    * Can be overridden with `--exts` flag.
  * By default the `{{ID}}` value needs to match `(\w+)` regex pattern, i.e spaces are not supported, unless overridden.
    * Can be overridden with `--id-regex-ovd` flag.

## Installation and Usage

1. Run `pip install spocktest`.
2. Run `spocktest <path to test folder> <path to docs folder> -o <path to output folder>`.

As of now it's recommended to use the `-o` flag at all times but if you're brave you can try modifying your docs in-place. If you omit the `-o` flag the docs folder will be replaced with an interpolated version.

To fine-tune extra configuration options use `spocktest --help`.
