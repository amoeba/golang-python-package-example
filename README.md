# golang-python-package-example

Working example of how to publish a Golang executable as a Python package on PyPi.
Golang is great at building platform native binaries and PyPi one of the most widely available software distribution platforms.

## How This Works

The workflow has two steps:

1. Run the `release_binaries.yml` workflow manually to build binaries for various platforms
2. Locally, run `create_wheels.py` to create wheels for each of the platforms in (1)

## Related Work

- <https://simonwillison.net/2022/May/23/bundling-binary-tools-in-python-wheels/>
- <https://github.com/ziglang/zig-pypi/blob/de14cf728fa35c014821f62a4fa9abd9f4bb560e/make_wheels.py>
