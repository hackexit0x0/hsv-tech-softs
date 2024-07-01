import argparse
import sys
import requests
import threading
from queue import Queue
import os

def request_url(url):
    try:
        response = requests.get(url, timeout=args.timeout)
        if response.status_code == 200:
            print(f"[{response.status_code}] {url}")
        elif args.verbose:
            print(f"[{response.status_code}] {url}")
    except requests.RequestException as e:
        if args.verbose:
            print(f"Error: {e}")

def worker():
    while not q.empty():
        directory = q.get()
        url = f"http://{args.hostname}/{directory}"
        request_url(url)
        q.task_done()

def main():
    global args, q
    parser = argparse.ArgumentParser(
        description="Web Directory Fuzzer",
        usage=f"python3 {sys.argv[0]} -H [IP] -w [WORDLIST FILE] -t [THREAD] -v [VERBOSE] -oN [OUTPUT]"
    )
    parser._optionals.title = "Basic Help Menu"
    parser.add_argument('-H', '--host', action="store", dest='hostname', help='Target IP Address', required=True)
    parser.add_argument('-w', '--wordlist', action="store", default="dir.txt", dest='wordlist', help='Wordlist File Path')
    parser.add_argument('-v', '--verbose', action="store_true", help='Enable verbose mode')
    parser.add_argument('-t', '--threads', action="store", type=int, default=9, dest='threads', help='No of threads (Default 9)')
    parser.add_argument('-T', '--timeout', action="store", default=5, type=int, dest='timeout', help='Request timeout (Default 5)')
    parser.add_argument('-oN', '--output', action="store", dest='output', help='Output file name')

    args = parser.parse_args()

    q = Queue()

    if not os.path.isfile(args.wordlist):
        print(f"Error: The wordlist file '{args.wordlist}' does not exist.")
        sys.exit(1)

    with open(args.wordlist, 'r') as wordlist_file:
        for line in wordlist_file:
            q.put(line.strip())

    for i in range(args.threads):
        t = threading.Thread(target=worker)
        t.start()

    q.join()

if __name__ == "__main__":
    main()
