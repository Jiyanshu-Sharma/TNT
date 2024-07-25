# -*- coding: utf-8 -*-
import sys
import time
import socket
from colorama import Fore, Style
from Tools.Port_Detection import PortScanner
from Tools.HoneyPot import Honeypot_pb
from Tools.EndPoint_Detection import EndpointDetector
from Tools.Network_Monitoring import NetworkMonitor


# ASCII art for TNT
tnt_art = """
 /$$$$$$$$ /$$   /$$ /$$$$$$$$
|__  $$__/| $$$ | $$|__  $$__/
   | $$   | $$$$| $$   | $$   
   | $$   | $$ $$ $$   | $$   
   | $$   | $$  $$$$   | $$   
   | $$   | $$\  $$$   | $$   
   | $$   | $$ \  $$   | $$   
   |__/   |__/  \__/   |__/   
                     
                     The Network Toolkit                            
"""

def display_art_with_delay(art, delay=2):    # Displaying the art with a delay 
    lines = art.strip().split('\n')
    delay_per_line = delay / len(lines)
    for line in lines:
        print(Fore.RED + line + Style.RESET_ALL)
        time.sleep(delay_per_line)

def get_service_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, int(port)))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None
    
def main():
    # Display ASCII art
    #display_art_with_delay(tnt_art)
    
    while True:
        print(Fore.GREEN + "\nChoose an option:" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Port Detection" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Endpoint Detection" + Style.RESET_ALL)
        print(Fore.GREEN + "3. HoneyPot" + Style.RESET_ALL)
        print(Fore.GREEN + "4. Network Fuzzer" + Style.RESET_ALL)
        print(Fore.GREEN + "5. Network Monitoring" + Style.RESET_ALL)
        print(Fore.GREEN + "6. Exit" + Style.RESET_ALL)
        
        choice = input(Fore.GREEN + "Enter your choice: " + Style.RESET_ALL).strip()
        
        if choice == '1':
            scanner = PortScanner()
            scanner.run()
            pause()
        
        elif choice == '2':
            EndpointDetector()
            pause()
        
        elif choice == '3':
            Honeypot_pb();
        
        elif choice == '4':
            print(Fore.GREEN + "Under Maintenance" + Style.RESET_ALL)
        
        elif choice == '5':
            monitor = NetworkMonitor()
            monitor.run()
            pause()

        
        elif choice == '6':
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            sys.exit()
        
        else:
            print(Fore.GREEN + "Invalid choice. Please try again." + Style.RESET_ALL)


def pause():
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()
