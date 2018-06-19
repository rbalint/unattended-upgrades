#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import unittest

from mock import (
    Mock,
)

from unattended_upgrade import calculate_upgradable_pkgs


class TestBlacklistedWrongOrigin(unittest.TestCase):

    @unittest.skipIf(sys.version_info[0] != 3, "only works on py3")
    def test_if_origin_does_not_match_then_blacklist_is_not_checked(self):
        origin = Mock()
        origin.origin = "some-other-origin"

        pkg = Mock()
        pkg.name = "postgresql"
        pkg.is_upgradable = True
        pkg.candidate = Mock()
        pkg.candidate.origins = [origin]

        options = Mock()

        pkgs_to_upgrade, pkgs_kept_back = \
            calculate_upgradable_pkgs([pkg],
                                      options,
                                      ["o=allowed-origin"],
                                      ["postgresql"],
                                      [])

        self.assertListEqual([], pkgs_to_upgrade)
        self.assertListEqual([], pkgs_kept_back)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
