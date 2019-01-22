from utils.rule_writer import RuleWriter

rw = RuleWriter('/etc/faucet/faucet.yaml')
rw.write_rules()

# Might need to reload faucet
# `sudo systemctl reload faucet`
