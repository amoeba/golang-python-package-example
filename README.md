# golang-python-package-example

Working example of how to publish a Golang executable as a Python package on PyPi.
Golang is great at building platform native binaries and PyPi one of the most widely available software distribution platforms.

## How This Works

The process to create wheels has two steps:

1. Run the `release_binaries.yml` workflow manually to build binaries for various platforms.

    The workflow has two parameters:

    - `ref`: The git ref to build from (e.g., `main` or any branch/tag)
    - `version`: A version for the Python package, must start with a number. (e.g., `0.1`)

    Note: In this repo, the code for the binaries is included. In a more realistic scenario, you might produce your binaries somewhere totally different.

2. Locally, run `create_wheels.py` to create wheels for each of the platforms in (1)

## Related Work

- <https://simonwillison.net/2022/May/23/bundling-binary-tools-in-python-wheels/>
- <https://github.com/ziglang/zig-pypi/blob/de14cf728fa35c014821f62a4fa9abd9f4bb560e/make_wheels.py>
