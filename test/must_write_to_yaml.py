from utils.rule_writer import RuleWriter


def must_write_rule_to_yaml():
    rw = RuleWriter('/etc/faucet/faucet.yaml')
    rw.write_rules()


must_write_rule_to_yaml()

# TODO(jk): Might need to reload faucet
# `sudo systemctl reload faucet`
