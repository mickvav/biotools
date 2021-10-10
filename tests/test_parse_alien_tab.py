#!/usr/bin/env python3

import unittest
import tempfile
import subprocess


class TestParseIntergration(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(suffix=".out", buffering=0)

    def test_normal(self):
        self.tempfile.seek(0)
        self.tempfile.write(
            b"""
FT   misc_fearute    12..34
FT                   /note="threshold: 1.2"
FT                   /score=123.3
FT                   /contig_start="contstart"
FT                   /contig_end="sontend"
FT                   /start_relative_position="start_rp"
FT                   /end_relative_position="end_rp"
"""
        )
        expected_output = (
            self.tempfile.name
            + "\t\t1.2\t123.3\tcontstart\tsontend\tstart_rp\tend_rp\n"
        )
        res = subprocess.run(
            f"python3 parse_alien_tab.py -i {self.tempfile.name}",
            shell=True,
            capture_output=True,
        )
        self.assertEqual(
            res.stdout, expected_output.encode("ascii"), f"Failure:  f{res.stdout}  "
        )
