import socket
import sys

def validPortNum(port):
    try:
        portNum = int(port)

        if 1 <= portNum <= 65535:
            return True
        
        return False
    except:
        return False

if len(sys.argv) != 2 or not validPortNum(sys.argv[1]):
    print("Invalid port number")
    sys.exit()

port = int(sys.argv[1])
ip = socket.gethostbyname(socket.gethostname())


def initialize():
    message = """
         Welcome to the chatroom! You have been connected.
    ==========================================================
    |                                                        |
    |       CCCCCCCCC   H     H      AA    TTTTTTTTTTTT      |
    |      C            H     H     A  A        TT           |
    |      C            HH H HH    A AA A       TT           |
    |      C            H     H   A      A      TT           |
    |       CCCCCCCCC   H     H  A        A     TT           |
    |                                                 ONLINE |
    ==========================================================
    Use 'help' command to view a list of commands w/ description.\n"""
    print(message)

def end():
    return """
              Farewell!! You have been disconnected.
    ==========================================================
    |                                                        |
    |       CCCCCCCCC   H     H      AA    TTTTTTTTTTTT      |
    |      C            H     H     A  A        TT           |
    |      C            HH H HH    A AA A       TT           |
    |      C            H     H   A      A      TT           |
    |       CCCCCCCCC   H     H  A        A     TT           |
    |                                                OFFLINE |
    ==========================================================\n"""


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
    except ConnectionRefusedError:
        print("Invalid port number")
        sys.exit()

    initialize()
    print("<YOU> ", end="")
    while True:
        message = input()
        try:
            client.send(message.encode("utf-8"))
            message = client.recv(2048).decode("utf-8")
            
            if  message.startswith("exit"):
                print(end())
                sys.exit()   
            else:
                print(f"{message}")
                print("<YOU> ", end="")
        except ConnectionResetError:
            print(message)
            print(end())
            sys.exit()
        except WindowsError as e:
            if e.winerror == 10053:
                print(message)
                print(end())
                sys.exit()

if __name__ == "__main__":
    main()

