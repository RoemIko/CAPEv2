# Copyright (C) 2010-2015 Cuckoo Foundation, Optiv, Inc. (brad.spengler@optiv.com)
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import base64
import logging
import struct
from typing import Dict

log = logging.getLogger(__name__)


# TODO: this probably can be replaced by vbe_decoder
class EncodedScriptFile:
    """Deobfuscates and interprets Windows Script Files."""

    encoding = (
        1,
        2,
        0,
        1,
        2,
        0,
        2,
        0,
        0,
        2,
        0,
        2,
        1,
        0,
        2,
        0,
        1,
        0,
        2,
        0,
        1,
        1,
        2,
        0,
        0,
        2,
        1,
        0,
        2,
        0,
        0,
        2,
        1,
        1,
        0,
        2,
        0,
        2,
        0,
        1,
        0,
        1,
        1,
        2,
        0,
        1,
        0,
        2,
        1,
        0,
        2,
        0,
        1,
        1,
        2,
        0,
        0,
        1,
        1,
        2,
        0,
        1,
        0,
        2,
    )

    lookup = (
        (
            0x00,
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x07,
            0x08,
            0x7B,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
            0x10,
            0x11,
            0x12,
            0x13,
            0x14,
            0x15,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
            0x1F,
            0x32,
            0x30,
            0x21,
            0x29,
            0x5B,
            0x38,
            0x33,
            0x3D,
            0x58,
            0x3A,
            0x35,
            0x65,
            0x39,
            0x5C,
            0x56,
            0x73,
            0x66,
            0x4E,
            0x45,
            0x6B,
            0x62,
            0x59,
            0x78,
            0x5E,
            0x7D,
            0x4A,
            0x6D,
            0x71,
            0x00,
            0x60,
            0x00,
            0x53,
            0x00,
            0x42,
            0x27,
            0x48,
            0x72,
            0x75,
            0x31,
            0x37,
            0x4D,
            0x52,
            0x22,
            0x54,
            0x6A,
            0x47,
            0x64,
            0x2D,
            0x20,
            0x7F,
            0x2E,
            0x4C,
            0x5D,
            0x7E,
            0x6C,
            0x6F,
            0x79,
            0x74,
            0x43,
            0x26,
            0x76,
            0x25,
            0x24,
            0x2B,
            0x28,
            0x23,
            0x41,
            0x34,
            0x09,
            0x2A,
            0x44,
            0x3F,
            0x77,
            0x3B,
            0x55,
            0x69,
            0x61,
            0x63,
            0x50,
            0x67,
            0x51,
            0x49,
            0x4F,
            0x46,
            0x68,
            0x7C,
            0x36,
            0x70,
            0x6E,
            0x7A,
            0x2F,
            0x5F,
            0x4B,
            0x5A,
            0x2C,
            0x57,
        ),
        (
            0x00,
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x07,
            0x08,
            0x57,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
            0x10,
            0x11,
            0x12,
            0x13,
            0x14,
            0x15,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
            0x1F,
            0x2E,
            0x47,
            0x7A,
            0x56,
            0x42,
            0x6A,
            0x2F,
            0x26,
            0x49,
            0x41,
            0x34,
            0x32,
            0x5B,
            0x76,
            0x72,
            0x43,
            0x38,
            0x39,
            0x70,
            0x45,
            0x68,
            0x71,
            0x4F,
            0x09,
            0x62,
            0x44,
            0x23,
            0x75,
            0x00,
            0x7E,
            0x00,
            0x5E,
            0x00,
            0x77,
            0x4A,
            0x61,
            0x5D,
            0x22,
            0x4B,
            0x6F,
            0x4E,
            0x3B,
            0x4C,
            0x50,
            0x67,
            0x2A,
            0x7D,
            0x74,
            0x54,
            0x2B,
            0x2D,
            0x2C,
            0x30,
            0x6E,
            0x6B,
            0x66,
            0x35,
            0x25,
            0x21,
            0x64,
            0x4D,
            0x52,
            0x63,
            0x3F,
            0x7B,
            0x78,
            0x29,
            0x28,
            0x73,
            0x59,
            0x33,
            0x7F,
            0x6D,
            0x55,
            0x53,
            0x7C,
            0x3A,
            0x5F,
            0x65,
            0x46,
            0x58,
            0x31,
            0x69,
            0x6C,
            0x5A,
            0x48,
            0x27,
            0x5C,
            0x3D,
            0x24,
            0x79,
            0x37,
            0x60,
            0x51,
            0x20,
            0x36,
        ),
        (
            0x00,
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x07,
            0x08,
            0x6E,
            0x0A,
            0x0B,
            0x0C,
            0x0D,
            0x0E,
            0x0F,
            0x10,
            0x11,
            0x12,
            0x13,
            0x14,
            0x15,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
            0x1F,
            0x2D,
            0x75,
            0x52,
            0x60,
            0x71,
            0x5E,
            0x49,
            0x5C,
            0x62,
            0x7D,
            0x29,
            0x36,
            0x20,
            0x7C,
            0x7A,
            0x7F,
            0x6B,
            0x63,
            0x33,
            0x2B,
            0x68,
            0x51,
            0x66,
            0x76,
            0x31,
            0x64,
            0x54,
            0x43,
            0x00,
            0x3A,
            0x00,
            0x7E,
            0x00,
            0x45,
            0x2C,
            0x2A,
            0x74,
            0x27,
            0x37,
            0x44,
            0x79,
            0x59,
            0x2F,
            0x6F,
            0x26,
            0x72,
            0x6A,
            0x39,
            0x7B,
            0x3F,
            0x38,
            0x77,
            0x67,
            0x53,
            0x47,
            0x34,
            0x78,
            0x5D,
            0x30,
            0x23,
            0x5A,
            0x5B,
            0x6C,
            0x48,
            0x55,
            0x70,
            0x69,
            0x2E,
            0x4C,
            0x21,
            0x24,
            0x4E,
            0x50,
            0x09,
            0x56,
            0x73,
            0x35,
            0x61,
            0x4B,
            0x58,
            0x3B,
            0x57,
            0x22,
            0x6D,
            0x4D,
            0x25,
            0x28,
            0x46,
            0x4A,
            0x32,
            0x41,
            0x3D,
            0x5F,
            0x4F,
            0x42,
            0x65,
        ),
    )

    unescape = {
        "#": "\r",
        "&": "\n",
        "!": "<",
        "*": ">",
        "$": "@",
    }

    def __init__(self, filepath: str):
        self.filepath = filepath

    def run(self) -> Dict[str, str]:
        try:
            with open(self.filepath, "rb") as f:
                source = f.read()
        except UnicodeDecodeError:
            return {}
        source = self.decode(source)
        if not source:
            return {}
        results = {"enscript": source[:65536]}
        if len(source) > 65536:
            results["encscript"] += "\r\n<truncated>"
        return results

    def decode(self, source: bytes, start: bytes = b"#@~^", end: bytes = b"^#~@") -> str:
        if start not in source or end not in source:
            return

        o = source.index(start) + len(start) + 8
        end = source.index(end) - 8
        c, m, r = bytes([]), 0, []

        while o < end:
            ch = source[o]
            if ch == 64:  # b"@":
                r.append(self.unescape.get(source[o + 1], b"?"))
                c += r[-1]
                o, m = o + 1, m + 1
            elif ch < 128:
                r.append(self.lookup[self.encoding[m % 64]][ch])
                c += r[-1]
                m += 1
            else:
                r.append(ch)
            o += 1

        if (c % 2**32) != base64.b64decode(struct.unpack("=I", source[o : o + 4]))[0]:
            log.info("Invalid checksum for Encoded WSF file!")

        return b"".join(r).decode("latin-1")
