# Local imports
from utils.operating_system import legacy_run_command
from utils.network import Endpoint, is_same_24_subnet
from data_collectors.network.local import get_client_net_info

# 3rd party imports
import re
from netaddr import IPAddress, AddrFormatError
from PyQt5.QtCore import QProcess


def _parse_tracert(command_output:str) -> list[IPAddress]:
    route_pattern = r"over a maximum of 30 hops:\s+(.*)\nTrace complete."
    output = re.search(route_pattern, command_output, flags=re.MULTILINE|re.DOTALL).group(1)
    lines = output.splitlines()
    
    hops = []
    for line in lines:
        if line:
            ip_field = line.split()[-1].replace('[', '').replace(']', '')
            if re.match(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', ip_field):
                try:
                    hops.append(IPAddress(ip_field))
                except AddrFormatError:
                    raise Exception(f'Invalid IP address {ip_field}')
    
    return hops

def get_private_ips(console_process: QProcess) -> list[IPAddress]:
    tracert_output = legacy_run_command(['tracert', '8.8.8.8'])
    hops = _parse_tracert(tracert_output)
    internal_ips = []
    for hop in hops:
        if hop.is_private():
            internal_ips.append(hop)

    return internal_ips

def get_internal_endpoints(console_process: QProcess) -> list[Endpoint]:
    private_ips: list[IPAddress] = get_private_ips(console_process)
    client_info:dict[str:str] = get_client_net_info()

    for ip in private_ips:
        if is_same_24_subnet(ip, client_info.get('ip')):
            router_endpoint = Endpoint('router', ip)
    
def get_localhost_ip() -> str:
    pass

if __name__ == '__main__':
    print(get_internal_endpoints("TODO"))