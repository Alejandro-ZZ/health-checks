#!/usr/bin/env python3
import os
import sys
import shutil
import socket
import psutil

def check_reboot():
    """Returns True id the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Returns True if there isn't enough disk space, Fase otherwise"""
    du = shutil.disk_usage(disk)
    #Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    #Calculate how many free gigabytes
    gigabytes_free = du.free / 2**30

    if gigabytes_free < min_gb or percent_free < min_percent:
        return True
    return False

def check_root_full():
    """Returns True if the root partition is full, False otherwise"""
    return check_disk_full(disk="/", min_gb=2, min_percent=10)

def check_cpu_constrained():
    """Returns  True if the cpu is having too much usage, False otherwise"""
    return psutil.cpu_percent(1) > 75

def checks_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks = [
        (check_reboot, "Pending Reboot."),
        (check_root_full, "Root partition full"),
        (checks_no_network, "No working network."),
        (check_cpu_constrained, "CPU load too high."),
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if not everything_ok:
        sys.exit(1)

main()
