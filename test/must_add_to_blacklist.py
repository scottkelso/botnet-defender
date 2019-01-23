from utils.rule_writer import RuleWriter


def must_blacklist_ip():
    rw = RuleWriter('/etc/faucet/faucet.yaml')
    rw.blacklist_ip('10.0.0.5')


must_blacklist_ip()

# TODO(jk): Might need to reload faucet
# `sudo systemctl reload faucet`
