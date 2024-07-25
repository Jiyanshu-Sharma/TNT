import os
import scapy.all as scapy
import logging
from colorama import Fore, Style
import subprocess

class NetworkMonitor:
    def __init__(self, interface=None):
        self.interface = interface
        self.log_directory = 'Logs'
        self.log_file = os.path.join(self.log_directory, 'network_monitoring.log')
        
        # Ensure the log directory exists
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Set up logging
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

        if self.interface:
            # Ensure the interface is in monitor mode
            self.set_monitor_mode()
    
    def set_monitor_mode(self):
        """
        Ensure the network interface is set to monitor mode.
        """
        try:
            # Check current mode
            mode_check = subprocess.check_output(['iwconfig', self.interface]).decode()
            if 'Mode:Monitor' in mode_check:
                print(Fore.GREEN + f"{self.interface} is already in monitor mode." + Style.RESET_ALL)
                return
            
            # Set monitor mode
            print(Fore.YELLOW + f"Setting {self.interface} to monitor mode..." + Style.RESET_ALL)
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'down'], check=True)
            subprocess.run(['sudo', 'iw', 'dev', self.interface, 'set', 'type', 'monitor'], check=True)
            subprocess.run(['sudo', 'ip', 'link', 'set', self.interface, 'up'], check=True)
            print(Fore.GREEN + f"{self.interface} successfully set to monitor mode." + Style.RESET_ALL)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error setting monitor mode: {e}" + Style.RESET_ALL)
            raise

    def packet_callback(self, packet):
        """
        This method will be called for each packet that is captured.
        """
        try:
            if packet.haslayer(scapy.IP):
                ip_src = packet[scapy.IP].src
                ip_dst = packet[scapy.IP].dst
                protocol = packet[scapy.IP].proto
                payload_len = len(packet)
                
                # Log packet information
                logging.info(f"Source IP: {ip_src} - Destination IP: {ip_dst} - Protocol: {protocol} - Length: {payload_len}")
                
                # Print packet information to the console
                print(Fore.CYAN + f"Source IP: {ip_src} - Destination IP: {ip_dst} - Protocol: {protocol} - Length: {payload_len}" + Style.RESET_ALL)
        except Exception as e:
            logging.error(f"Error processing packet: {e}")

    def start_monitoring(self):
        """
        Start sniffing packets on the specified network interface.
        """
        if not self.interface:
            print(Fore.RED + "No interface specified for monitoring." + Style.RESET_ALL)
            return
        
        print(Fore.GREEN + f"Starting network monitoring on interface: {self.interface}" + Style.RESET_ALL)
        scapy.sniff(iface=self.interface, prn=self.packet_callback, store=0)

    def get_user_input(self):
        """
        Function to get user input for network monitoring.
        """
        self.interface = input("Enter the network interface to monitor (e.g., wlan0): ").strip()
        self.set_monitor_mode()
    
    def run(self):
        """
        Run the NetworkMonitor.
        """
        if not self.interface:
            self.get_user_input()
        self.start_monitoring()
