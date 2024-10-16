#!/usr/bin/env python3

import os
import shutil
import sys
import socket
import psutil

print("hi my friend")
def check_reboot():
  return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
  du = shutil.disk_usage(disk)
  percent_free = 100 * du.free / du.total
  gigabytes_free = du.free / 2**30
  if percent_free < min_percent or gigabytes_free < min_gb:
    return True
  return False
def check_root_full():
  return check_disk_full (disk="/", min_gb=2, min_percent=10)

def check_no_network():
  try:
    socket.gethostbyname("www.google.com")
    return False
  except: 
    return True

def check_cpu_constrained():
  return psutil.cpu_percent(1)>75


def main():
  check = [
    (check_reboot, "Pending Reboot"),
    (check_root_full, "Root partition full"),
    (check_no_network, "No working network"),
    (check_cpu_constrained, "CPU load too high")
  ]
  everything_ok = True
  for check, msg in check:
    if check():
      print(msg)
      everything_ok=False

  if not everything_ok:
    sys.exit(1)

  print("everythin is good koxu")
  sys.exit(0)
main()
