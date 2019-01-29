# https://github.com/jaiken06/poseidon/blob/master/poseidon/poseidonMonitor/Config/Rule_Ops.py
import yaml


def represent_none(dumper, _):
    return dumper.represent_scalar('tag:yaml.org,2002:null', '')


class RuleWriter:

    def __init__(self, config_file):
        self.config_file = config_file
        self.blacklist_file = '../main/blacklist.txt'

    def write_rules(self):

        try:
            stream = open(self.config_file, 'r')
            obj_doc = yaml.safe_load(stream)
            stream.close()

            found = False
            for rules in obj_doc['acls']:
                # Temporary check if the single rule is already there
                if rules == "Block":
                    print("Block rule already active!")
                    found = True
                    break

            # Decide block rule
            if found:
                return
            else:
                obj_doc['acls']['block'] = \
                    [{'rule': {'actions': {'allow': False}}}]

                stream = open(self.config_file, 'w')
                yaml.add_representer(type(None), represent_none)
                yaml.dump(obj_doc, stream, default_flow_style=False)
                print("Block rule activated!")

        except Exception as e:
            print("ERROR: Failed to load config file!")
            print(str(e))
            return False

        return True

    def block_ip(self, ip):

        try:
            stream = open(self.config_file, 'r')
            obj_doc = yaml.safe_load(stream)
            stream.close()

            # found = False
            # for rules in obj_doc['acls']:
            #     # Temporary check if the single rule is already there
            #     if rules == "block":
            #         print("Block rule already active!")
            #         found = True
            #         break
            #
            # # Decide block rule
            # if found:
            #     return
            # else:
            obj_doc['acls']['blocked'] = \
                [{'rule': {'dl_type': 0x0800, 'nw_dst': ip, 'actions': {'allow': 0}}}]

            # rules = []
            #
            # # for ip in blocked_set:
            # #     rules.append({'rule': {'dl_type': 0x0800, 'nw_dst': ip, 'actions': {'allow': 0}}})
            # rules.append({'rule': {'dl_type': 0x0800, 'nw_dst': ip, 'actions': {'allow': 0}}})

            stream = open(self.config_file, 'w')
            yaml.add_representer(type(None), represent_none)
            yaml.dump(obj_doc, stream, default_flow_style=False)
            print("IP address ", str(ip), " activated!")

        except Exception as e:
            print("ERROR: Failed to load config file!")
            print(str(e))
            return False

        return True

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
                f.write(ip+'\n')
            return True
        else:
            return False

    def flush_blacklist(self):
        open(self.blacklist_file, 'w').close()
        return True
