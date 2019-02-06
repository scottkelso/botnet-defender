# https://github.com/jaiken06/poseidon/blob/master/poseidon/poseidonMonitor/Config/Rule_Ops.py
import yaml


def represent_none(dumper, _):
    return dumper.represent_scalar('tag:yaml.org,2002:null', '')


class RuleWriter:

    def __init__(self, config_file='../setup/faucet.yaml', blacklist_file='../main/blacklist.txt'):
        self.config_file = config_file
        self.blacklist_file = blacklist_file

    def write_rules(self):

        blacklist = self.read_blacklist()

        try:
            stream = open(self.config_file, 'r')
            obj_doc = yaml.safe_load(stream)
            stream.close()

            obj_doc['acls']['block'] = []
            blocking_rules = obj_doc['acls']['block']

            print("Writing " + str(len(blacklist)) + " rules...")
            for ip in blacklist:
                blocking_rules.extend(
                    self.new_rule(ip)
                )

            stream = open(self.config_file, 'w')
            yaml.add_representer(type(None), represent_none)
            yaml.dump(obj_doc, stream, default_flow_style=False)
            stream.close()
            print("Blocking rules written!")

        except Exception as e:
            print("ERROR: Failed to load config file!")
            print(str(e))
            return False

        return True

    @staticmethod
    def new_rule(ip):
        return [
            {
                'rule': {
                    'dl_type': '0x800',  # ipv4
                    'ipv4_dst': ip,  # host not to send to
                    'actions': {
                        'allow': 0
                    }
                }
            },
            {
                'rule': {
                    'dl_type': '0x800',  # ipv4
                    'ipv4_src': ip,  # host being blocked
                    'actions': {
                        'allow': 1
                    }
                }
            }]

    def read_blacklist(self):
        with open(self.blacklist_file, 'r') as f:
            blacklist = f.readlines()
        blacklist = [x.strip() for x in blacklist]
        # if len(blacklist) > 0:
        #     blacklist.pop()
        return blacklist

    def blacklist_ip(self, ip):
        blacklist = self.read_blacklist()
        if ip not in blacklist:
            with open(self.blacklist_file, 'a') as f:
                f.write(ip + '\n')
            return True
        else:
            return False

    def block_ip(self, ip):
        if self.blacklist_ip(ip):
            return self.write_rules()
        else:
            return False

    def flush_blacklist(self):
        open(self.blacklist_file, 'w').close()
        return True

    def get_config(self):
        try:
            stream = open(self.config_file, 'r')
            obj_doc = yaml.safe_load(stream)
            stream.close()
            return obj_doc

        except Exception as e:
            print("ERROR: Failed to load config file!")
            print(str(e))
            return None

    def set_config(self, config):
        try:

            stream = open(self.config_file, 'w')
            yaml.add_representer(type(None), represent_none)
            yaml.dump(config, stream, default_flow_style=False)
            stream.close()
            print("New config file loaded!")

        except Exception as e:
            print("ERROR: Failed to write config file!")
            print(str(e))
            return False

        return True
