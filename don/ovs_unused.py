#
# ovs.py: Runs ovs-appctl command to check if A -> B flow is working fine.
#
#
import sys
import re
import pprint
import argparse
from common import load_json, error, debug, settings
from common import get_port_ovs_id_tag, execute_cmd

params = {}

class OvsTester:
    def __init__ (self, src_vm, src_ip, dst_vm, dst_ip, json_file):
        self.info = load_json(json_file)
        vm_list = pprint.pformat(sorted(self.info['vms'].keys()))
        if not self.info['vms'].has_key(src_vm):
            error('VM [%s] does not exist in %s !' % (src_vm, vm_list))
            return None
        if not self.info['vms'].has_key(dst_vm):
            error('VM [%s] does not exist in %s !' % (dst_vm, vm_list))
            return None

        self.src_vm = src_vm
        self.src_ip = src_ip
        self.dst_vm = dst_vm
        self.dst_ip = dst_ip

        (self.src_port_id, self.src_port_tag) = get_port_ovs_id_tag(self.info, src_vm, src_ip)
        (self.dst_port_id, self.dst_port_tag) = get_port_ovs_id_tag(self.info, dst_vm, dst_ip)

        if not self.src_port_id:
            error('%s does not have port with IP %s' % (src_vm, src_ip))
            return None
        if not self.dst_port_id:
            error('%s does not have port with IP %s' % (dst_vm, dst_ip))
            return None

        debug(src_ip + ': ' + str(self.src_port_id))
        debug(dst_ip + ': ' + str(self.dst_port_id))

        pass

    # Learn a MAC on the dst port and then check if sending from the src port to
    # the learned MAC gives correct lookup
    def test (self):
        command_list = []
        smac = 'AA:BB:CC:DD:EE:11'
        dmac = 'AA:BB:CC:DD:EE:22'

        # Step 1. run command that will learn smac
        cmd = ''
        cmd += 'sudo ovs-appctl ofproto/trace br-int in_port=' + self.src_port_id
        cmd += ',dl_src=' + smac + ',dl_dst=' + dmac + ' -generate'
        output = execute_cmd(cmd, shell=True).split('\n')
        command_list.append((cmd, output))

        # Step 2. verify that the mac has been learnt
        cmd = ''
        cmd += 'sudo ovs-appctl fdb/show br-int'
        output = execute_cmd(cmd, shell=True).split('\n')
        command_list.append((cmd, output))

        port = None
        for line in output:
            m = re.search('(\d)\s+(\d+)\s+(\S+)\s+\d+', line)
            if m:
                mac = m.group(3)
                if mac.lower() == smac.lower():
                    port = m.group(1)
                    vlan = m.group(2)
                    debug(line)
                    break
        if not port:
            error('%s not learnt on port %s' % (smac, self.src_port_id))
            return False

        if vlan != self.src_port_tag:
            error('%s learnt on vlan %s but should have been learnt on vlan %s on port %s' % (smac, vlan, self.src_port_tag, port))
            return False
        debug('%s learnt on expected vlan %s on port %s' % (smac, vlan, port))

        # Step 3. now do a lookup using the dst port id and dmac as the smac of step 1.
        cmd = ''
        cmd += 'sudo ovs-appctl ofproto/trace br-int in_port=' + self.dst_port_id
        cmd += ',dl_src=' + dmac + ',dl_dst=' + smac + ' -generate'
        output = execute_cmd(cmd, shell=True).split('\n')
        command_list.append((cmd, output))

        forwarded = False
        egress_port = None
        for line in output:
            if re.search('forwarding to learned port', line):
                forwarded = True
                continue
            m = re.search('Datapath actions: (.*)', line)
            if m:
                egress_port = m.group(1)
                continue

        result = True
        if not forwarded:
            error('Packet for learnt mac not forwarded!')
            result = False
        else:
            debug('Packet for learnt mac forwarded properly')

        if egress_port:
            if egress_port == self.src_port_id:
                debug('Packet forwarded to correct port %s' % egress_port)
            else:
                error('Packet forwarded to incorrect port %s, expected %s' %
                        (egress_port, self.src_port_id))
                result = False
        else:
            error('No egress port assigned to packet! Expected %s' %
                    self.src_port_id)
            result = False

        debug(pprint.pformat(command_list))
        return result

def check_args():
    parser = argparse.ArgumentParser(description='Runs OVS test between a specified pair of ports')
    parser.add_argument('--src_vm', dest='src_vm',
                        help='VM name of source port',
                        type=str, required=True)
    parser.add_argument('--src_ip', dest='src_ip',
                        help='IP of port of vm specified with --src_vm',
                        type=str, required=True)
    parser.add_argument('--dst_vm', dest='dst_vm',
                        help='VM name of destination port',
                        type=str, required=True)
    parser.add_argument('--dst_ip', dest='dst_ip',
                        help='IP of port of vm specified with --dst_vm',
                        type=str, required=True)
    parser.add_argument('--json_file', dest='json_file',
                        help='JSON format input file containing info',
                        default="don.json", type=str, required=True)

    parser.add_argument('--debug', dest='debug', help='Enable debugging',
                        default=True, action='store_true')

    args = parser.parse_args()

    settings['debug'] = args.debug

    params['json_file'] = args.json_file
    params['src_vm']    = args.src_vm
    params['src_ip']    = args.src_ip
    params['dst_vm']    = args.dst_vm
    params['dst_ip']    = args.dst_ip

def main():
    check_args()
    ovs_tester  = OvsTester(params['src_vm'], params['src_ip'], params['dst_vm'],
                            params['dst_ip'], params['json_file'])
    ovs_success = ovs_tester.test()

    if ovs_success:
        print 'ovs %s (%s) -->  %s (%s): PASS' % (params['src_vm'], params['src_ip'], params['dst_vm'], params['dst_ip'])
    else:
        print 'ovs %s (%s) -->  %s (%s): FAIL' % (params['src_vm'], params['src_ip'], params['dst_vm'], params['dst_ip'])

if __name__ == "__main__":
    main()
