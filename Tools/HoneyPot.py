import socket
import threading
import time
import os
import random

class Honeypot_pb:
    def __init__(self):
        print("")
        print("// Honeypot //")
        print("Select option.")
        print("")
        print("1- Fast Auto Configuration")
        print("2- Manual Configuration [Advanced Users, more options]")
        print("")
        configuration = input("   -> ")

        def honeyconfig(port, message, sound, log, logname): # Function to launch the Honeypot.
            try:
                tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcpserver.bind(("", int(port)))
                tcpserver.listen(5)
                print("")
                print(f"  HONEYPOT ACTIVATED ON PORT {port} ({time.ctime()})")
                print("")
                if log.lower() == "y":
                    try:
                        with open(logname, "a") as logf:
                            logf.write("#################### Honeypot log\n")
                            logf.write("\n")
                            logf.write(f"  HONEYPOT ACTIVATED ON PORT {port} ({time.ctime()})\n")
                            logf.write("\n")
                    except FileNotFoundError:
                        print("")
                        print(" Saving log error: No such file or directory.")
                        print("")
                while True:
                    socket_client, addr = tcpserver.accept()
                    time.sleep(1) # It is to solve possible DoS Attacks.
                    if socket_client:
                        def handle_client(socket_client):
                            remote_ip, remote_port = addr
                            print("")
                            print(f"  INTRUSION ATTEMPT DETECTED! from {remote_ip}:{remote_port} ({time.ctime()})")
                            print(" -----------------------------")
                            reciv = socket_client.recv(1000).decode("utf-8")
                            print(reciv)
                            if sound.lower() == "y":
                                # If sound is enabled, then beep 3 times.
                                print("\a\a\a")
                            if log.lower() == "y":
                                try:
                                    with open(logname, "a") as logf:
                                        logf.write("\n")
                                        logf.write(f"  INTRUSION ATTEMPT DETECTED! from {remote_ip}:{remote_port} ({time.ctime()})\n")
                                        logf.write(" -----------------------------\n")
                                        logf.write(reciv + "\n")
                                except FileNotFoundError:
                                    print("")
                                    print(" Saving log error: No such file or directory.")
                                    print("")
                            time.sleep(2) # This is a sticky honeypot.
                            socket_client.sendall(message.encode("utf-8"))
                            socket_client.close()

                        threading.Thread(target=handle_client, args=(socket_client,)).start()
            except PermissionError:
                print("")
                print(" Error: Honeypot requires root privileges.")
                print("")
            except OSError:
                print("")
                print(" Error: Port in use.")
                print("")
            except:
                print("")
                print(" Unknown error.")
                print("")

        if configuration == "1":
            access = random.randint(0, 2)
            if access == 0:
                honeyconfig(80, "<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n<H2>Access denied</H2>\n" + "<H3>HTTP Referrer login failed</H3>\n" + "<H3>IP Address login failed</H3>\n" + "<P>\n" + time.ctime() + "\n</P>", "N", "N", "")
            elif access == 1:
                honeyconfig(80, "<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n<H2>Access denied</H2>\n" + "<H3>IP Address login failed</H3>\n" + "<P>\n" + time.ctime() + "\n</P>", "N", "N", "")
            elif access == 2:
                honeyconfig(80, "<HEAD>\n<TITLE>Access denied</TITLE>\n</HEAD>\n<H2>Access denied</H2>\n" + "<P>\n" + time.ctime() + "\n</P>", "N", "N", "")
        elif configuration == "2":
            print("")
            print(" Insert port to Open.")
            print("")
            port = input("   -> ")
            print("")
            print(" Insert false message to show.")
            print("")
            message = input("   -> ")
            print("")
            print(" Save a log with intrusions?")
            print("")
            log = input(" (y/n)   -> ")
            if log.lower() == "y":
                print("")
                print(" Log file name? (incremental)")
                print("")
                print("Default: ./log_honeypot.txt")
                print("")
                logname = input("   -> ").replace("\"", "").replace("'", "")
                if logname == "":
                    logname = os.path.join(os.path.dirname(__file__), "log_honeypot.txt")
            print("")
            print(" Activate beep() sound when intrusion?")
            print("")
            sound = input(" (y/n)   -> ")
            honeyconfig(port, message, sound, log, logname)
        else:
            print("")
            print("Invalid option.")
            print("")

if __name__ == "__main__":
    Honeypot_pb()
