#!/usr/bin/env python3
# port_scanner_threaded.py
# Simple threaded TCP port scanner (educational). Use only on targets you are allowed to test.

import socket
import threading
import queue
import argparse
from datetime import datetime

def worker(q, host, timeout, results):
    while True:
        try:
            port = q.get_nowait()
        except queue.Empty:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            res = sock.connect_ex((host, port))
            if res == 0:
                results.append(port)
            sock.close()
        except Exception:
            pass
        finally:
            q.task_done()

def make_port_list(ports_arg):
    if not ports_arg:
        # default common ports
        return [21,22,23,25,53,80,110,139,143,161,389,443,445,3306,3389]
    ports = set()
    parts = ports_arg.split(",")
    for part in parts:
        if "-" in part:
            a,b = part.split("-")
            ports.update(range(int(a), int(b)+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def scan(host, ports, threads=100, timeout=0.5):
    q = queue.Queue()
    for p in ports:
        q.put(p)
    results = []
    thread_list = []
    for _ in range(min(threads, q.qsize())):
        t = threading.Thread(target=worker, args=(q, host, timeout, results))
        t.daemon = True
        t.start()
        thread_list.append(t)
    q.join()
    return sorted(results)

def parse_args():
    parser = argparse.ArgumentParser(description="Threaded TCP port scanner (educational).")
    parser.add_argument("target", help="Target hostname or IP (example: 127.0.0.1 or scanme.nmap.org)")
    parser.add_argument("-p", "--ports", help="Comma-separated ports or range (e.g. 20-1024 or 22,80,443).")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default 100)")
    parser.add_argument("-T", "--timeout", type=float, default=0.5, help="Socket timeout seconds (default 0.5)")
    return parser.parse_args()

def main():
    args = parse_args()
    host = args.target
    ports = make_port_list(args.ports)
    print(f"Scanning {host} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ports to scan: {len(ports)} (first 20 shown): {ports[:20]}{'...' if len(ports) > 20 else ''}")
    open_ports = scan(host, ports, threads=args.threads, timeout=args.timeout)
    if open_ports:
        print(f"Open ports on {host}: {open_ports}")
    else:
        print(f"No open ports found on {host} within scanned set.")

if __name__ == "__main__":
    main()
