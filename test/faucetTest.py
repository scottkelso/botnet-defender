import unittest
from utils.rule_writer import RuleWriter


class FaucetTest(unittest.TestCase):

    def setup(self):
        rw = RuleWriter()
        rw.flush_blacklist()
        blacklist = rw.read_blacklist()
        self.assertEqual(len(blacklist), 0)
        rw.blacklist_ip('10.0.0.5')
        rw.blacklist_ip('10.0.0.8')

    def test_write_to_yaml(self):
        self.setup()
        rw = RuleWriter('faucet.yaml')
        rw2 = RuleWriter('faucetExpected.yaml')
        original_config = rw.get_config()
        working_config = rw.get_config()
        expected_config = rw2.get_config()

        self.assertEqual(len(working_config['acls']), 1)
        self.assertEqual(len(expected_config['acls']), 2)

        rw.write_rules()
        working_config = rw.get_config()
        self.assertEqual(len(working_config['acls']), 2)
        self.assertEqual(len(working_config['acls']['block']), 4)

        # Reset
        rw.set_config(original_config)


if __name__ == '__main__':
    unittest.main()


# TODO(jk): Might need to reload faucet
# `sudo systemctl reload faucet`
