import threading
from queue import Queue
from scapy.all import IP, TCP, sr1

# Common ports with their names
port_services = {                               # Dictionary is created
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    993: 'IMAPS',
    995: 'POP3S',
}

class PortScanner:
    def __init__(self):
        self.target = None
        self.start_port = None
        self.end_port = None
        self.num_threads = 10
        self.verbose = False
        self.open_ports = []
        self.seen_ports = set()

    def get_user_input(self):
        self.target = input("Enter target IP or domain: ")
        self.start_port = int(input("Enter start port: "))
        self.end_port = int(input("Enter end port: "))
        self.verbose = input("Verbose output (yes/no): ").strip().lower() == 'yes'

    def scan_port(self, port):
        try:
            pkt = IP(dst=self.target) / TCP(dport=port, flags="S")    # IP packet is created
            response = sr1(pkt, timeout=3, verbose=0)
            
            if response and response.haslayer(TCP):
                if response[TCP].flags == 18:  # TCP SYN-ACK
                    service_name = port_services.get(port, 'Unknown Service')
                    self.open_ports.append((port, service_name))
                    self.seen_ports.add(port)
                    if self.verbose:
                        print(f"Port {port} is open: {service_name}")
                elif response[TCP].flags == 20:  # TCP RST-ACK (port closed)
                    self.seen_ports.add(port)
        except Exception as e:
            if self.verbose:
                print(f"Error scanning port {port}: {e}")

    def worker(self, port_queue):
        while not port_queue.empty():
            port = port_queue.get()
            self.scan_port(port)
            port_queue.task_done()

    def port_scan(self):
        print(f"Starting SYN scan on host: {self.target}")
        port_queue = Queue()

        for port in range(self.start_port, self.end_port + 1):
            port_queue.put(port)

        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker, args=(port_queue,))
            thread.start()
            threads.append(thread)

        port_queue.join()
        for thread in threads:
            thread.join()

        return self.open_ports

    def run(self):
        self.get_user_input()
        open_ports = self.port_scan()
        
        if open_ports:
            print("\nOpen ports:")
            for port, service in open_ports:
                print(f"Port {port} is open: {service}")
        else:
            print("No open ports found.")

if __name__ == "__main__":
    scanner = PortScanner()
    scanner.run()
