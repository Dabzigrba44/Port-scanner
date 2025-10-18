<<<<<<< HEAD
# Port-scanner
=======
port_scanner_threaded.py
>>>>>>> 2196185 (Add threaded Python port scanner (educational))
# Port Scanner (Threaded) — Educational

A simple threaded TCP port scanner written in Python for educational and lawful testing only.

## Features
- Multi-threaded scanning for faster results
- Supports single ports, comma lists, and ranges (e.g. 22,80,443 or 1-1024)
- Save or redirect output to a file
- Example usage shown below

## Usage
```bash
# scan localhost common ports
python port_scanner_threaded.py 127.0.0.1

# scan a range with 200 threads and 0.3s timeout
python port_scanner_threaded.py scanme.nmap.org -p 20-1024 -t 200 -T 0.3

# save output to file
python port_scanner_threaded.py scanme.nmap.org -p 1-1024 > scan_results.txt
