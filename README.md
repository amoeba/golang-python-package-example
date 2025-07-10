# golang-python-package-example

Working example of how to publish a Golang executable as a Python package on PyPi.
Golang is great at building platform native binaries and PyPi one of the most widely available software distribution platforms.

## How This Works

The process to create wheels has just a few steps:

1. Run the `release_binaries.yml` workflow manually to build binaries for various platforms.

    The workflow has two parameters:

    - `ref`: The git ref to build from (e.g., `main` or any branch/tag)
    - `version`: A version for the Python package, must start with a number. (e.g., `0.1`)

    Note: In this repo, the code for the binaries is included. In a more realistic scenario, you might produce your binaries somewhere totally different and pull them in.

2. Locally, run `create_wheels.py` to create wheels for each of the platforms in (1)
3. Publish the created wheels to Test PyPi

    ```sh
    twine upload --repository testpypi out/*
    ```

4. Verify the wheels work by running the `test_wheels.yml` workflow.

    The workflow has two parameters:

    - `package_name`: The name of the package on Test PyPi (e.g., `mybin`)
    - `version`: The version of the package on Test PyPi to test (e.g., `0.1`)

## Example Output

create_wheels.py:

```sh
$ python create_wheels.py --binary_version 0.1 --wheel_version 0.1.1
https://api.github.com/repos/amoeba/golang-python-package-example/releases/tags/0.1
Creating wheel for asset: {'name': 'mybin-darwin-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-darwin-amd64-0.1.zip', 'digest': 'sha256:481a9e1459c8fad72672423355b76e50b835bec1adaa630b4dbbb0b20a062bb0'}
Creating wheel for asset: {'name': 'mybin-darwin-arm64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-darwin-arm64-0.1.zip', 'digest': 'sha256:5db36129c294f9acb12e3d726420b4336893705c10410e9beac29d83159bb13c'}
Creating wheel for asset: {'name': 'mybin-linux-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-linux-amd64-0.1.zip', 'digest': 'sha256:095a53fe7d4a67f36a27e1e5b2d7f75e5e243f2e57251ac85db1b623679b797e'}
Creating wheel for asset: {'name': 'mybin-linux-arm64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-linux-arm64-0.1.zip', 'digest': 'sha256:c18813b6b160462285f164c50fd89999eaa676d9fc71972dce03a5f5f3a1c97d'}
Creating wheel for asset: {'name': 'mybin-windows-amd64-0.1.zip', 'download_url': 'https://github.com/amoeba/golang-python-package-example/releases/download/0.1/mybin-windows-amd64-0.1.zip', 'digest': 'sha256:703eaea33ca75d79e931ad2f2140330a0615d1b27360c4bd2cb9fd981c12db3c'}
```

Which produces:

```sh
$ ls -1 dist
mybin-0.1.1-py3-none-macosx_12_0_arm64.whl
mybin-0.1.1-py3-none-macosx_12_0_x86_64.whl
mybin-0.1.1-py3-none-manylinux_2_12_x86_64.whl
mybin-0.1.1-py3-none-manylinux_2_17_aarch64.whl
mybin-0.1.1-py3-none-win_amd64.whl
```

## Related Work

- <https://simonwillison.net/2022/May/23/bundling-binary-tools-in-python-wheels/>
- <https://github.com/ziglang/zig-pypi/blob/de14cf728fa35c014821f62a4fa9abd9f4bb560e/make_wheels.py>
