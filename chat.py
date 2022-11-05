from audioop import add
import socket
import threading
import sys

global i
global inbox

i = 0
ip = socket.gethostbyname(socket.gethostname())
inbox = []
clients = []
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


class Client:
    def __init__(self, ip, port, id, socket):
        self.ip = ip
        self.port = port
        self.id = id
        self.socket = socket

class InboxItem:
    def __init__(self, message, socket):
        self.message = message
        self.socket = socket

def help():
    return """
    help                                Displays command info.
    myip                                Display IP address.
    myport                              Display port which is listening for incoming connections
    list                                Display list of all connections this process is part of.
    terminate <connection id>           Terminate connection with <connection id>.
    send <connection id> <message>      Sends <message> to <connection id>.
    exit                                Terminates process.
    """

def list():
    message = "    ID:   IP              PORT\n"

    for client_obj in clients:
        message = message + f"    {client_obj.id}:   {client_obj.ip}    {client_obj.port}\n"

    return message

def terminate(connection_id):
    temp_ip = 1
    temp_port = 1

    for x in clients:
        if connection_id == x.id:
            temp_ip = x.ip
            temp_port = x.port
            x.socket.close()
            clients.remove(x)

    return temp_ip + str(temp_port)

def send(connection_id):
    for obj_client in clients:
        if obj_client.id == connection_id:
            return obj_client

def exit(conn):
    for c in clients:
        if c.socket == conn:
            clients.remove(c)

    return "exit"

def client_thread(c, addr): 
    while True:
        try:
            message = c.recv(2048).decode("utf-8")
            print(f"> ({addr[0]} : {addr[1]}>): {message} ")

            if message == "exit":
                message = exit(c)
                message += retrieveInboxMessages(c)
                c.send(message.encode("utf-8"))
                c.close()
            elif message == "help":
                message = help()
                message += retrieveInboxMessages(c)
                c.send(f"    {message}".encode("utf-8"))
            elif message == "myip":
                message = str(ip)
                message += retrieveInboxMessages(c)

                c.send(f"    {message}".encode("utf-8"))
            elif message == "myport":
                message = str(port)
                message += retrieveInboxMessages(c)
                c.send(f"    {message}".encode("utf-8"))
            elif message == "list":
                message = list()
                message += retrieveInboxMessages(c)
                c.send(message.encode("utf-8"))
            elif message.split()[0] == "terminate":
                if not validNumOfParams(2, message):
                    c.send("Missing parameter(s).".encode("utf-8"))
                    continue

                if not validConnectionID(message.split()[1]):
                    c.send("Invalid connection id.".encode("utf-8"))
                    continue                
                
                message = terminate(int(message.split()[1])) + " has been banished!"
                message += retrieveInboxMessages(c)
                c.send(message.encode("utf-8"))
            elif message.split()[0] == "send":
                if not validNumOfParams(3, message):
                    c.send("Missing parameter(s).".encode("utf-8"))
                    continue

                if not validConnectionID(message.split()[1]):
                    c.send("Invalid connection id.".encode("utf-8"))
                    continue  

                if not validMessage(message.split()[2]):
                    c.send("Message can be up-to 100 characters long.".encode("utf-8"))
                    continue

                rec_obj = send(int(message.split()[1]))
                s = rec_obj.socket
                rec_ip = rec_obj.ip
                rec_port = rec_obj.port
                message = f"    Message Received from {addr[0]}:{addr[1]}\n" \
                            f"    Sender's Port: {addr[1]}\n    Message: \"{message.split()[2]}\"\n"
                inbox.append(InboxItem(message, s))
                c.send(f"Message sent to {rec_ip}:{rec_port}.".encode("utf-8"))
            else:
                message += retrieveInboxMessages(c)
                c.send(message.encode("utf-8"))
        except WindowsError as e:
            if e.winerror == 10038 or e.winerror == 10053:
                print(f"> {addr[0]}:{addr[1]} closed")
                break
            elif e.winerror == 10054:
                exit(c)
                print(f"> {addr[0]}:{addr[1]} closed")
                break
            else:
                print("> ", e)
        
    c.close()

def retrieveInboxMessages(c):
    delete = []
    messages = "\n"
    for item in inbox:
        if c == item.socket:
                messages += item.message + "\n"
                delete.append(item)

    for item in delete:
        inbox.remove(item)
    
    return messages
def validMessage(msg):
    if msg is None or len(msg) > 100 or len(msg) <= 0:
        return False

    return True

def validNumOfParams(num, input):
    return len(input.split()) == num

def validConnectionID(connection_id):
    try:
        conn_id = int(connection_id)

        for client in clients:
            if client.id == conn_id:
                return True
        
        return False
    except:
        return False

def server():
    print("> Server is starting...")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
    except ConnectionRefusedError:
        print("Invalid port number")
        sys.exit()

    server.listen(5)
    print(f"> Server is listening on {ip}:{port}")

    while True:
        global i
        i += 1
        c, addr = server.accept()
        print(f"> {addr} connected")
        clients.append(Client(addr[0], addr[1], i, c))
        thread = threading.Thread(target=client_thread, args=(c, addr))
        thread.start()

def main():
    server()


if __name__ == "__main__":
    main()
