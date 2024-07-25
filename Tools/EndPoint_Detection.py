import sys
import csv
import logging
import os
from datetime import datetime
from scapy.all import ARP, Ether, srp, conf
from colorama import Fore, Style 

class EndpointDetector:
    def __init__(self, ip=None, interface=None, output="results.csv", verbose=False):
        self.ip = ip
        self.interface = interface
        self.output = output
        self.verbose = verbose
        self.clients = []
        self.setup_logging()
        self.run()

    def setup_logging(self):
        # Ensure the Logs directory exists
        logs_dir = 'Logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Set up logging configuration
        log_file = os.path.join(logs_dir, 'arp_scanner.log')
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(filename=log_file, level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    def scan_network(self):
        if self.interface:
            conf.iface = self.interface
        arp_request = ARP(pdst=self.ip)
        broadcast_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        final_request = broadcast_frame / arp_request
        answered_list = srp(final_request, timeout=2, verbose=False)[0]
        self.clients = [{"ip": received.psrc, "mac": received.hwsrc} for sent, received in answered_list]

    def display_results(self):
        print("IP Address\t\tMAC Address")
        print("-----------------------------------------")
        for client in self.clients:
            print(f"{client['ip']}\t\t{client['mac']}")

    def save_results(self):
        # Ensure the Logs directory exists
        logs_dir = 'Logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Set the output file path to be inside the Logs directory
        output_file = os.path.join(self.output)
        
        file_exists = os.path.exists(output_file)
        mode = 'a' if file_exists else 'w'
        with open(output_file, mode, newline='') as csvfile:
            fieldnames = ['Date', 'IP Address', 'MAC Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for client in self.clients:
                writer.writerow({'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'IP Address': client['ip'], 'MAC Address': client['mac']})

    def run(self):
        if self.ip is None:
            self.ip = input(Fore.GREEN + "Enter IP range (e.g., 192.168.1.0/24): " + Style.RESET_ALL).strip()
        self.interface = input(Fore.GREEN + "Enter network interface (optional): " + Style.RESET_ALL).strip() or self.interface
        self.output = input(Fore.GREEN + "Enter output file (CSV format): " + Style.RESET_ALL).strip() or self.output
        
        # Ensure the output file path is inside the Logs directory
        if not self.output.startswith('Logs/'):
            self.output = os.path.join('Logs', self.output)
        
        if not self.ip:
            logging.error("Invalid Syntax. Use --help or -h for options.")
            print("Invalid Syntax")
            print("Use --help or -h for options.")
            sys.exit(1)
        
        self.scan_network()
        if self.clients:
            self.display_results()
            self.save_results()
            print(f"\nResults appended to {self.output}")
            logging.info(f"Results appended to {self.output}")
        else:
            print("No clients found.")
            logging.info("No clients found.")

def main():
    EndpointDetector()

if __name__ == "__main__":
    main()
