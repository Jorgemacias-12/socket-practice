import random
import socket
import psutil
import os
import re

from tabulate import tabulate

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
  
  filtered_ips = []
  for ip in ips:
    if not ip.startswith("127."):
      for iface, addrs in psutil.net_if_addrs().items():
        if "vEthernet" not in iface:
          for addr in addrs:
            if addr.address == ip:
              filtered_ips.append(ip)
  
  return filtered_ips[:1][0] if filtered_ips else None

def list_folder_contents():
  user_docs = os.path.join(os.environ['USERPROFILE'], 'Documents')
  
  folder_name = "udp_documents"
  
  folder_path = os.path.join(user_docs, folder_name)
  
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  
  files = os.listdir(folder_path)
  
  file_details = []
  
  for file in files:
    file_path = os.path.join(folder_path, file)
    
    if not os.path.isfile(file_path):
      continue
    
    size = os.path.getsize(file_path)
    file_details.append([file, f"{size / 1024:.2f} KB"])
  
  return file_details

def create_download_folder():
  user_docs = os.path.join(os.environ['USERPROFILE'], 'Documents')
  
  folder_name = "udp_downloads"
  
  folder_path = os.path.join(user_docs, folder_name)
  
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  

def convert_to_table(data):
  
  data = [[index] + row for index, row in enumerate(data)]
  
  headers = ["Index","Filename", "Size"]
  
  table = tabulate(data, headers, tablefmt="grid")
  
  return table

def get_file_full_path(file_name):
  return os.path.join(os.path.join(os.environ['USERPROFILE'], 'Documents'), 'udp_documents', file_name)

def get_downloads_folder():
  return os.path.join(os.path.join(os.environ['USERPROFILE'], 'Documents'), 'udp_downloads')

def get_file_name(string):
  pattern = r'\[(.+?)\]'
  
  match = re.search(pattern, string)
  
  if match:
    return match.group(1)