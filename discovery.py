from endpoint import Endpoint
from utils import run_command, get_client_net_info

import re
from netaddr import IPAddress, AddrFormatError

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

def get_private_ips() -> list[IPAddress]:
    tracert_output = run_command(['tracert', '8.8.8.8'])
    hops = _parse_tracert(tracert_output)
    internal_ips = []
    for hop in hops:
        if hop.is_private():
            internal_ips.append(hop)

    return internal_ips

def get_internal_endpoints() -> list[Endpoint]:
    private_ips: list[IPAddress] = get_private_ips()
    client_info = get_client_net_info()
    
    
def get_localhost_ip() -> str:
    pass

if __name__ == '__main__':
    print(get_internal_endpoints())
