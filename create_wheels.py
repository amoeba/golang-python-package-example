# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "wheel",
# ]
# ///

# Adapted from https://github.com/ziglang/zig-pypi/blob/main/make_wheels.py

import argparse
from email.message import EmailMessage
import hashlib
import io
import os
import urllib
import urllib.request
import json
from wheel.wheelfile import WheelFile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


GITHUB_ORG = "amoeba"
GITHUB_REPO = "golang-python-package-example"
PACKAGE_NAME = "mybin"


def get_latest_github_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        release_info = {
            "tag_name": data["tag_name"],
            "name": data["name"],
            "published_at": data["published_at"],
            "assets": [],
        }

        for asset in data["assets"]:
            release_info["assets"].append(
                {
                    "name": asset["name"],
                    "download_url": asset["browser_download_url"],
                    "digest": asset["digest"],
                }
            )

        return release_info
    except Exception as e:
        print(f"Error fetching release data: {e}")
        return None


def iter_archive_contents(archive):
    with ZipFile(io.BytesIO(archive)) as zip_file:
        for entry in zip_file.infolist():
            if not entry.is_dir():
                yield entry.filename, entry.external_attr >> 16, zip_file.read(entry)


def make_message(headers, payload=None):
    msg = EmailMessage()
    for name, value in headers:
        if isinstance(value, list):
            for value_part in value:
                msg[name] = value_part
        else:
            msg[name] = value
    if payload:
        msg.set_payload(payload)
    return msg


class ReproducibleWheelFile(WheelFile):
    def writestr(self, zinfo_or_arcname, data, *args, **kwargs):
        if isinstance(zinfo_or_arcname, ZipInfo):
            zinfo = zinfo_or_arcname
        else:
            assert isinstance(zinfo_or_arcname, str)
            zinfo = ZipInfo(zinfo_or_arcname)
            zinfo.file_size = len(data)
            zinfo.external_attr = 0o0644 << 16
            if zinfo_or_arcname.endswith(".dist-info/RECORD"):
                zinfo.external_attr = 0o0664 << 16

        # TODO: Understand what these are actually doing
        zinfo.compress_type = ZIP_DEFLATED
        zinfo.date_time = (1980, 1, 1, 0, 0, 0)
        zinfo.create_system = 3
        super().writestr(zinfo, data, *args, **kwargs)


def write_wheel_file(filename, contents):
    with ReproducibleWheelFile(filename, "w") as wheel:
        for member_info, member_source in contents.items():
            wheel.writestr(member_info, bytes(member_source))
    return filename


def write_wheel(out_dir, *, name, version, tag, metadata, description, contents):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    wheel_name = f"{name}-{version}-{tag}.whl"
    dist_info = f"{name}-{version}.dist-info"
    filtered_metadata = []
    for header, value in metadata:
        filtered_metadata.append((header, value))

    return write_wheel_file(
        os.path.join(out_dir, wheel_name),
        {
            **contents,
            f"{dist_info}/entry_points.txt": make_message(
                [],
                f"[console_scripts]\npython-{PACKAGE_NAME} = {PACKAGE_NAME}.__main__:dummy",  # TODO: Rename dummy
            ),
            f"{dist_info}/METADATA": make_message(
                [
                    ("Metadata-Version", "2.4"),  # TODO: Is 2.4 right?
                    ("Name", name),
                    ("Version", version),
                    *filtered_metadata,
                ],
                description,
            ),
            f"{dist_info}/WHEEL": make_message(
                [
                    ("Wheel-Version", "1.0"),
                    ("Generator", f"{PACKAGE_NAME} create_wheels.py"),
                    ("Root-Is-Purelib", "false"),
                    ("Tag", tag),
                ]
            ),
        },
    )


def create_wheel(version: str, archive: bytes):
    contents = {}
    contents[f"{PACKAGE_NAME}/__init__.py"] = b""

    # TODO: Scan all files? How do I want to scan?
    bin_prefix = "mybin"
    for entry_name, entry_mode, entry_data in iter_archive_contents(archive):
        # TODO: Why did zig do this next line?
        # entry_name = "/".join(entry_name.split("/")[1:])

        if not entry_name:
            continue
        if entry_name.startswith("doc/"):
            continue

        zip_info = ZipInfo(f"{PACKAGE_NAME}/{entry_name}")
        zip_info.external_attr = (entry_mode & 0xFFFF) << 16
        contents[zip_info] = entry_data

        if entry_name.startswith(bin_prefix):
            bin_path = entry_name

    # __init__.py
    # TODO

    # __main__.py
    contents[f"{PACKAGE_NAME}/__main__.py"] = (
        f'''\
import os, sys
argv = [os.path.join(os.path.dirname(__file__), "{bin_path}"), *sys.argv[1:]]
if os.name == 'posix':
    os.execv(argv[0], argv)
else:
    import subprocess; sys.exit(subprocess.call(argv))

def dummy(): """Dummy function for an entrypoint. Zig is executed as a side effect of the import."""
'''.encode(
            "ascii"
        )
    )
    platform = "TODO"
    description = "TOOD"
    write_wheel(
        "./out",
        name=PACKAGE_NAME,
        version=version,
        tag=f"py3-none-{platform}",
        metadata=[
            (
                "Summary",
                "TODO",
            ),
        ],
        description=description,
        contents=contents,
    )


def get_and_verify_zip(version: str) -> bytes:
    release_info = get_latest_github_release(GITHUB_ORG, GITHUB_REPO)
    asset = release_info["assets"][0]
    archive_url = asset["download_url"]
    print(f"Creating wheel for asset: {asset}")

    with urllib.request.urlopen(archive_url) as request:
        archive = request.read()
        actual_hash = hashlib.sha256(archive).hexdigest()
        expected_hash = asset["digest"].split(":")[1]
        if actual_hash != expected_hash:
            raise Exception(
                f"Hash mismatch. Expected {expected_hash}, got {actual_hash}."
            )

    return archive


def create_wheels(version):
    # TODO: Create wheels for each platform we pass in
    archive = get_and_verify_zip(version)
    create_wheel(version, archive)


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        default="latest",
        help="Version to package. Use 'latest' for latest release or 'main' for the latest build on the main branch.",
    )

    return parser


def main():
    args = parse_args().parse_args()
    create_wheels(args.version)


if __name__ == "__main__":
    main()
