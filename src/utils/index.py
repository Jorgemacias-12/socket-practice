import random
import socket

def generate_random_port():
  return random.randint(1024, 65535)
  
def validate_ip(ip):
  try:
    socket.inet_aton(ip)
    
    return True
  except socket.error:
    return False

minimal_port = 1
maximum_port = 65535
  
def validate_port(port):
  try:
    port = int(port)
    
    return minimal_port <= port <= maximum_port
  except ValueError:
    return False

def get_machine_ip():
  local_hostname = socket.gethostname()
  
  ips = socket.gethostbyname_ex(local_hostname)[2]
  
  filtered_ips = [ip for ip in ips if not ip.startswith("127.")]
  
  return filtered_ips[:1][0]
  