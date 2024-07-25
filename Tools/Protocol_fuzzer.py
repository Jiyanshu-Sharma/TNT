import socket
import time
import ftplib
import sys

def fuzz_buff_http(title, part1, part2):
    buffer = "A"
    cont = 0
    anumber = 1
    print("\n", title)
    while cont <= 13:
        time.sleep(0.25)
        cont += 1
        buffer += buffer
        send = f"{part1}{buffer}{part2}"
        try:
            with socket.create_connection((host, port), timeout=15) as s:
                s.sendall(send.encode())
        except socket.timeout:
            print("\n\n   Connection timeout.\n   Host may be down. Possible Exploit?\n")
            print(f"   Packet: {title}{anumber}A\n")
            sys.exit()
        except socket.error:
            print("\n\n   Impossible to connect.\n   Host may be down. Possible Exploit?\n")
            print(f"   Packet: {title}{anumber}A\n")
            sys.exit()
        anumber += anumber
        print(f"{anumber}A ", end="")
    print("- OK\n")

def fuzz_buff_http_client(title, header):
    buffer = "A"
    cont = 0
    anumber = 1
    print("\n", title)
    while cont <= 13:
        buffer += buffer
        conn, addr = http_server.accept()
        conn.recv(5000)
        packet = f"HTTP/1.1 200 OK\r\n{header}: {buffer}\r\n\r\n<!doctype html>\n<script>\n{sleep_js}\nlocation.reload(true);\n</script>"
        conn.sendall(packet.encode())
        conn.close()
        cont += 1
        anumber += anumber
        print(f"{anumber}A ", end="")
    print("- OK\n")

def fuzz_buff_ftp(command):
    buffer = "A"
    cont = 0
    anumber = 1
    print(f"   {command} [MALFORMED] -> ", end="")
    while cont <= 13:
        time.sleep(0.25)
        cont += 1
        buffer += buffer
        try:
            if command == "cd":
                ftp.cwd(buffer)
            elif command == "delete":
                ftp.delete(buffer)
            elif command == "get":
                ftp.retrbinary(f"RETR {buffer}", open("/dev/null", "wb").write)
            elif command == "help":
                ftp.sendcmd(f"HELP {buffer}")
            elif command == "status":
                ftp.sendcmd(f"STAT {buffer}")
        except ftplib.all_errors:
            pass
        anumber += anumber
        print(f"{anumber}A ", end="")
    print("- OK\n")

print("\n// Fuzzer //\n")
print("Supported protocols -> [HTTP, client HTTP, FTP]\n")
print(" Insert host (unnecessary if fuzzing HTTP client).\n")
host = input("   -> ")
print("\n Insert port (will be opened if fuzzing HTTP client).\n")
port = int(input("   -> "))
print("\n Select mode.\n")
print("1- HTTP headers (fuzz server)")
print("2- HTTP headers browser (fuzz client)")
print("3- FTP\n")
protocol = input("   -> ")

if protocol == "3":
    print("\n Insert username.\n")
    user = input("   -> ")
    print("\n Insert password (it will be printed on the screen).\n")
    password = input("   -> ")

if protocol == "1" or protocol == "3":
    try:
        with socket.create_connection((host, port)):
            pass
    except socket.error:
        print("\nConnection problem.\n")
        sys.exit()

sleep_js = "\
var startTime = new Date().getTime();\n\
while (new Date().getTime() < startTime + 1500);\n"

if protocol == "1":
    print("\n  Testing Buffer Overflow")
    print("  -----------------------")
    fuzz_buff_http("   HEAD [MALFORMED] HTTP/1.1 -> ", "HEAD ", " HTTP/1.1\r\n\r\n")
    fuzz_buff_http("   HEAD / [MALFORMED] -> ", "HEAD / ", "\r\n\r\n")
    fuzz_buff_http("   GET [MALFORMED] HTTP/1.1 -> ", "GET ", " HTTP/1.1\r\n\r\n")
    fuzz_buff_http("   GET / [MALFORMED] -> ", "GET / ", "\r\n\r\n")
    fuzz_buff_http("   POST [MALFORMED] HTTP/1.1 -> ", "POST ", " HTTP/1.1\r\n\r\n")
    fuzz_buff_http("   POST / [MALFORMED] -> ", "POST / ", "\r\n\r\n")
    fuzz_buff_http("   GET / HTTP/[MALFORMED] -> ", "GET / HTTP/", "\r\n\r\n")
    fuzz_buff_http("   GET / [MALFORMED]/1.1 -> ", "GET / ", "/1.1\r\n\r\n")
    fuzz_buff_http("   User-Agent: [MALFORMED] -> ", "GET / HTTP/1.1\r\nUser-Agent: ", "\r\n\r\n")
    fuzz_buff_http("   Host: [MALFORMED] -> ", "GET / HTTP/1.1\r\nHost: ", "\r\n\r\n")
    fuzz_buff_http("   Connection: [MALFORMED] -> ", "GET / HTTP/1.1\r\nConnection: ", "\r\n\r\n")
    fuzz_buff_http("   Referer: [MALFORMED] -> ", "GET / HTTP/1.1\r\nReferer: ", "\r\n\r\n")
    fuzz_buff_http("   Authorization: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAuthorization: ", "\r\n\r\n")
    fuzz_buff_http("   Cookie: [MALFORMED] -> ", "GET / HTTP/1.1\r\nCookie: ", "\r\n\r\n")
    fuzz_buff_http("   Accept: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAccept: ", "\r\n\r\n")
    fuzz_buff_http("   Accept-Encoding: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAccept-Encoding: ", "\r\n\r\n")
    fuzz_buff_http("   Accept-Language: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAccept-Language: ", "\r\n\r\n")
    fuzz_buff_http("   Accept-Charset: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAccept-Charset: ", "\r\n\r\n")
    fuzz_buff_http("   Accept-Ranges: [MALFORMED] -> ", "GET / HTTP/1.1\r\nAccept-Ranges: ", "\r\n\r\n")
    fuzz_buff_http("   Content-Length: [MALFORMED] -> ", "GET / HTTP/1.1\r\nContent-Length: ", "\r\n\r\n")
    fuzz_buff_http("   Content-Type: [MALFORMED] -> ", "GET / HTTP/1.1\r\nContent-Type: ", "\r\n\r\n")
    fuzz_buff_http("   Cache-Control: [MALFORMED] -> ", "GET / HTTP/1.1\r\nCache-Control: ", "\r\n\r\n")
    fuzz_buff_http("   Date: [MALFORMED] -> ", "GET / HTTP/1.1\r\nDate: ", "\r\n\r\n")
    fuzz_buff_http("   From: [MALFORMED] -> ", "GET / HTTP/1.1\r\nFrom: ", "\r\n\r\n")
    fuzz_buff_http("   Charge-To: [MALFORMED] -> ", "GET / HTTP/1.1\r\nCharge-To: ", "\r\n\r\n")
    fuzz_buff_http("   ChargeTo: [MALFORMED] -> ", "GET / HTTP/1.1\r\nChargeTo: ", "\r\n\r\n")
    fuzz_buff_http("   If-Match: [MALFORMED] -> ", "GET / HTTP/1.1\r\nIf-Match: ", "\r\n\r\n")
    fuzz_buff_http("   If-Modified-Since: [MALFORMED] -> ", "GET / HTTP/1.1\r\nIf-Modified-Since: ", "\r\n\r\n")
    fuzz_buff_http("   If-Unmodified-Since: [MALFORMED] -> ", "GET / HTTP/1.1\r\nIf-Unmodified-Since: ", "\r\n\r\n")
    fuzz_buff_http("   If-None-Match: [MALFORMED] -> ", "GET / HTTP/1.1\r\nIf-None-Match: ", "\r\n\r\n")
    fuzz_buff_http("   If-Range: [MALFORMED] -> ", "GET / HTTP/1.1\r\nIf-Range: ", "\r\n\r\n")
    fuzz_buff_http("   Max-Forwards: [MALFORMED] -> ", "GET / HTTP/1.1\r\nMax-Forwards: ", "\r\n\r\n")
    fuzz_buff_http("   Pragma: [MALFORMED] -> ", "GET / HTTP/1.1\r\nPragma: ", "\r\n\r\n")
    fuzz_buff_http("   Range: [MALFORMED] -> ", "GET / HTTP/1.1\r\nRange: ", "\r\n\r\n")
    fuzz_buff_http("   Transfer-Encoding: [MALFORMED] -> ", "GET / HTTP/1.1\r\nTransfer-Encoding: ", "\r\n\r\n")
    fuzz_buff_http("   Upgrade: [MALFORMED] -> ", "GET / HTTP/1.1\r\nUpgrade: ", "\r\n\r\n")
    fuzz_buff_http("   Via: [MALFORMED] -> ", "GET / HTTP/1.1\r\nVia: ", "\r\n\r\n")
    fuzz_buff_http("   Warning: [MALFORMED] -> ", "GET / HTTP/1.1\r\nWarning: ", "\r\n\r\n")

elif protocol == "2":
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server.bind(('', port))
    http_server.listen(5)
    print(f"\nWaiting browser connection on port {port}.\n")

    print("\n  Testing Buffer Overflow")
    print("  -----------------------")
    fuzz_buff_http_client("   User-Agent: [MALFORMED] -> ", "User-Agent")
    fuzz_buff_http_client("   Referer: [MALFORMED] -> ", "Referer")
    fuzz_buff_http_client("   Authorization: [MALFORMED] -> ", "Authorization")
    fuzz_buff_http_client("   Cookie: [MALFORMED] -> ", "Cookie")
    fuzz_buff_http_client("   Accept: [MALFORMED] -> ", "Accept")
    fuzz_buff_http_client("   Accept-Encoding: [MALFORMED] -> ", "Accept-Encoding")
    fuzz_buff_http_client("   Accept-Language: [MALFORMED] -> ", "Accept-Language")
    fuzz_buff_http_client("   Accept-Charset: [MALFORMED] -> ", "Accept-Charset")
    fuzz_buff_http_client("   Accept-Ranges: [MALFORMED] -> ", "Accept-Ranges")
    fuzz_buff_http_client("   Content-Length: [MALFORMED] -> ", "Content-Length")
    fuzz_buff_http_client("   Content-Type: [MALFORMED] -> ", "Content-Type")
    fuzz_buff_http_client("   Cache-Control: [MALFORMED] -> ", "Cache-Control")
    fuzz_buff_http_client("   Date: [MALFORMED] -> ", "Date")
    fuzz_buff_http_client("   From: [MALFORMED] -> ", "From")
    fuzz_buff_http_client("   Charge-To: [MALFORMED] -> ", "Charge-To")
    fuzz_buff_http_client("   ChargeTo: [MALFORMED] -> ", "ChargeTo")
    fuzz_buff_http_client("   If-Match: [MALFORMED] -> ", "If-Match")
    fuzz_buff_http_client("   If-Modified-Since: [MALFORMED] -> ", "If-Modified-Since")
    fuzz_buff_http_client("   If-Unmodified-Since: [MALFORMED] -> ", "If-Unmodified-Since")
    fuzz_buff_http_client("   If-None-Match: [MALFORMED] -> ", "If-None-Match")
    fuzz_buff_http_client("   If-Range: [MALFORMED] -> ", "If-Range")
    fuzz_buff_http_client("   Max-Forwards: [MALFORMED] -> ", "Max-Forwards")
    fuzz_buff_http_client("   Pragma: [MALFORMED] -> ", "Pragma")
    fuzz_buff_http_client("   Range: [MALFORMED] -> ", "Range")
    fuzz_buff_http_client("   Transfer-Encoding: [MALFORMED] -> ", "Transfer-Encoding")
    fuzz_buff_http_client("   Upgrade: [MALFORMED] -> ", "Upgrade")
    fuzz_buff_http_client("   Via: [MALFORMED] -> ", "Via")
    fuzz_buff_http_client("   Warning: [MALFORMED] -> ", "Warning")

    print("   Your browser should be stuck.\n")

elif protocol == "3":
    ftp = ftplib.FTP()
    try:
        ftp.connect(host, port, timeout=10)
        ftp.login(user, password)
    except ftplib.all_errors as e:
        print(f"\nLogin problem: {e}\n")
        sys.exit()

    print("\n  Testing Buffer Overflow")
    print("  -----------------------")
    fuzz_buff_ftp("cd")
    fuzz_buff_ftp("delete")
    fuzz_buff_ftp("get")
    fuzz_buff_ftp("help")
    fuzz_buff_ftp("status")
    ftp.quit()

print("\n")
