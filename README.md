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

## Example

```sh
$ uv run python create_wheels.py
Creating wheel for asset: {'name': 'mybin-darwin-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-darwin-amd64-0.1.zip', 'digest': 'sha256:1eb18e810fda41874c61473341a05d5dcf4b3569276c9059b5d8cd354f1df19f'}
Creating wheel for asset: {'name': 'mybin-linux-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-linux-amd64-0.1.zip', 'digest': 'sha256:598b2f972875ada397ef4cd61a8f9045288005d5145c4db890465878c18fddc3'}
Creating wheel for asset: {'name': 'mybin-windows-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-windows-amd64-0.1.zip', 'digest': 'sha256:08e2ab308f73c6b41eeff99253307bb5632448b917ee169b71c1ffda8c044ed2'}

~/src/amoeba/golang-python-package-example main*
$ ls -1 out
mybin-0.1-py3-none-macosx_12_0_x86_64.whl
mybin-0.1-py3-none-manylinux_2_12_x86_64.whl
mybin-0.1-py3-none-win_amd64.whl
```

## Related Work

- <https://simonwillison.net/2022/May/23/bundling-binary-tools-in-python-wheels/>
- <https://github.com/ziglang/zig-pypi/blob/de14cf728fa35c014821f62a4fa9abd9f4bb560e/make_wheels.py>
