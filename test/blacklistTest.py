import unittest
from utils.rule_writer import RuleWriter


class BlacklistTest(unittest.TestCase):

    def setup(self):
        rw = RuleWriter()
        rw.flush_blacklist()
        blacklist = rw.read_blacklist()
        self.assertEqual(len(blacklist), 0)
        rw.blacklist_ip('10.0.0.5')
        rw.blacklist_ip('10.0.0.8')

    def test_read_blacklist(self):
        self.setup()
        rw = RuleWriter()
        blacklist = rw.read_blacklist()
        self.assertEqual(len(blacklist), 2)
        self.assertEqual(blacklist[0], '10.0.0.5')
        self.assertEqual(blacklist[1], '10.0.0.8')

    def test_add_to_blacklist(self):
        self.setup()
        rw = RuleWriter()
        blacklist_before = rw.read_blacklist()
        response = rw.blacklist_ip('10.0.0.9')
        blacklist_after = rw.read_blacklist()
        self.assertTrue(response)
        self.assertEqual(len(blacklist_before), len(blacklist_after)-1)

    def test_add_to_blacklist_only_if_not_exists(self):
        self.setup()
        rw = RuleWriter()
        blacklist_before = rw.read_blacklist()
        response = rw.blacklist_ip('10.0.0.5')
        blacklist_after = rw.read_blacklist()
        self.assertFalse(response)
        self.assertEqual(blacklist_before, blacklist_after)

    def test_flush_blacklist(self):
        self.setup()
        rw = RuleWriter()
        blacklist_before = rw.read_blacklist()
        self.assertGreater(len(blacklist_before), 0)
        response = rw.flush_blacklist()
        blacklist_after = rw.read_blacklist()
        self.assertTrue(response)
        self.assertEqual(len(blacklist_after), 0)

    # TODO(jk)
    def test_remove_from_blacklist(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


# TODO(jk): Might need to reload faucet
# `sudo systemctl reload faucet`
