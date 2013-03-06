#!/usr/bin/env python
from __future__ import with_statement
from cStringIO import StringIO
import os
import sys
import tarfile
import zipfile


"""Creates a zoneinfo.zip archive from the zoneinfo data inside a pytz
distribution file (.tar.gz or .zip). Reads from STDIN, writes to STDOUT.
"""


def filter_tzfiles(name_list):
    """Returns a list of tuples for names that are tz data files."""
    for src_name in name_list:
        # pytz-2012j/pytz/zoneinfo/Indian/Christmas
        parts = src_name.split('/')
        if len(parts) > 3 and parts[2] == 'zoneinfo':
            dst_name = '/'.join(parts[2:])
            yield src_name, dst_name


def extract_zip(fileobj):
    """Yields 3-tuples of (name, modified, bytes)."""
    archive = zipfile.ZipFile(fileobj, mode='r')
    filenames = archive.namelist()

    for src_name, dst_name in filter_tzfiles(filenames):
        modified = archive.getinfo(src_name).date_time
        bytes = archive.read(src_name)

        yield dst_name, modified, bytes


def extract_tar(fileobj):
    """Yields 3-tuples of (name, modified, bytes)."""
    import time

    archive = tarfile.open(fileobj=fileobj)
    filenames = [info.name for info in archive.getmembers() if info.isfile()]

    for src_name, dst_name in filter_tzfiles(filenames):
        mtime = archive.getmember(src_name).mtime
        modified = tuple(time.gmtime(mtime)[:6])
        bytes = archive.extractfile(src_name).read()

        yield dst_name, modified, bytes


def main(src):
    try:
        zonefiles = list(extract_zip(src))
    except zipfile.BadZipfile:
        src.seek(0)
        zonefiles = list(extract_tar(src))

    dst = StringIO()
    file_mode = 0600 << 16

    with zipfile.ZipFile(dst, 'w') as dst_archive:
        for name, modified, data in zonefiles:
            info = zipfile.ZipInfo(filename=name, date_time=modified)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = file_mode

            dst_archive.writestr(info, data)

    sys.stdout.write(dst.getvalue())


if __name__ == "__main__":

    if len(sys.argv) > 1:
        sys.stderr.write("""Usage: makezoneinfo.py < SRC_ARCHIVE > DST_ARCHIVE

Reads a zip or tar archive from stdin and writes a zip archive to stdout,
containing just the zoneinfo files.
""")
        raise SystemExit(1)

    src = StringIO(sys.stdin.read())
    main(src)
