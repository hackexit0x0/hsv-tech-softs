# Python Port Scanner
# Version : beta
# Devlop : HackExit0x0 
# Link : https://github.com/hackexit0x0

# import lib
import socket
import threading
import time
import os
import platform
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to check if IP is active
def is_ip_active(ip):
    # Use different ping command options based on the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"
    response = os.system(f"ping {param} 1 {ip}")
    if response == 0:
        print(f"{Fore.GREEN}[+] host ip : {ip} is up Host.")
        return True
    else:
        print(f"{Fore.RED}[-] host ip : {ip} is down HOst.")
        return False

# Function to scan a single port
def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        try:
            service_name = socket.getservbyport(port)
        except:
            service_name = "Unknown"
        
        try:
            s.send(b'Hello\r\n')
            banner = s.recv(1024).decode().strip()
        except:
            banner = "Unknown"
        
        print(f"{Fore.GREEN}[+] Port {port} is open - Service: {service_name} - Version: {banner}")
    except:
        pass
    finally:
        s.close()

# Function to handle multithreading
def threader(ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

# Main function
if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    
    if is_ip_active(target_ip):
        start_port = 0
        end_port = 65535
        
        start_time = time.time()
        print(f"{Fore.CYAN}[+] Scan started at {time.ctime(start_time)}{Style.RESET_ALL}")
        
        threader(target_ip, start_port, end_port)
        
        end_time = time.time()
        print(f"{Fore.CYAN}[+] Scan ended at {time.ctime(end_time)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Total scan time: {end_time - start_time} seconds{Style.RESET_ALL}")
