#!/usr/bin/python3

import os
import unittest

import apt_pkg
apt_pkg.config.set("Dir", "./aptroot")
import apt

import unattended_upgrade

apt.apt_pkg.config.set("APT::Architecture", "amd64")


class MockOptions(object):
    debug = False
    verbose = False
    download_only = False
    dry_run = True
    apt_debug = False
    minimal_upgrade_steps = True


class TestRewindCache(unittest.TestCase):

    def setUp(self):
        rootdir = os.path.abspath("./root.rewind")
        dpkg_status = os.path.abspath(
            os.path.join(rootdir, "var", "lib", "dpkg", "status"))
        apt.apt_pkg.config.set("Dir::State::status", dpkg_status)
        self.allowed_origins = ["origin=Ubuntu,archive=lucid-security"]
        self.cache = unattended_upgrade.UnattendedUpgradesCache(
            rootdir=rootdir, allowed_origins=self.allowed_origins)

    def test_rewind_cache(self):
        """ Test that rewinding the cache works correctly, debian #743594 """
        options = MockOptions()
        blacklist = []
        whitelist = []
        to_upgrade, kept_back = unattended_upgrade.calculate_upgradable_pkgs(
            self.cache, options, self.allowed_origins, blacklist, whitelist)
        self.assertEqual(to_upgrade, [self.cache[p] for p
                                      in ["test-package", "test2-package",
                                          "test3-package"]])
        self.assertEqual(kept_back["Ubuntu lucid-security"], {"z-package"})
        unattended_upgrade.rewind_cache(self.cache, to_upgrade)
        self.assertEqual(self.cache['test-package'].candidate.version, "2.0")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
