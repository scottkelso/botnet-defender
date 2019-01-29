import unittest
from utils.rule_writer import RuleWriter


class BlacklistTest(unittest.TestCase):

    def test_setup(self):
        rw = RuleWriter('/etc/faucet/faucet.yaml')
        rw.flush_blacklist()
        blacklist = rw.read_blacklist()
        self.assertEqual(len(blacklist), 0)
        rw.blacklist_ip('10.0.0.5')
        rw.blacklist_ip('10.0.0.8')

    def test_read_blacklist(self):
        rw = RuleWriter('/etc/faucet/faucet.yaml')
        blacklist = rw.read_blacklist()
        self.assertEqual(len(blacklist), 2)
        self.assertEqual(blacklist[0], '10.0.0.5')
        self.assertEqual(blacklist[1], '10.0.0.8')

    def test_add_to_blacklist(self):
        rw = RuleWriter('/etc/faucet/faucet.yaml')
        blacklist_before = rw.read_blacklist()
        response = rw.blacklist_ip('10.0.0.9')
        blacklist_after = rw.read_blacklist()
        self.assertTrue(response)
        self.assertEqual(len(blacklist_before), len(blacklist_after)-1)

    def test_add_to_blacklist_only_if_not_exists(self):
        rw = RuleWriter('/etc/faucet/faucet.yaml')
        blacklist_before = rw.read_blacklist()
        response = rw.blacklist_ip('10.0.0.9')
        blacklist_after = rw.read_blacklist()
        self.assertFalse(response)
        self.assertEqual(blacklist_before, blacklist_after)

    # TODO(jk)
    def test_remove_from_blacklist(self):
        self.assertTrue(True)

    # TODO(jk)
    def test_block_ip_with_faucet(self):
        # rw = RuleWriter('/etc/faucet/faucet.yaml')
        # rw.block_ip('10.0.0.5')
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


# TODO(jk): Might need to reload faucet
# `sudo systemctl reload faucet`
