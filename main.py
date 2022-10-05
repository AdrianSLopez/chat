def initialize():
    print(r"""
==========================================================
|                                                        |
|       CCCCCCCCC   H     H      AA    TTTTTTTTTTTT      |
|      C            H     H     A  A        TT           |
|      C            HH H HH    A AA A       TT           |
|      C            H     H   A      A      TT           |
|       CCCCCCCCC   H     H  A        A     TT           |
|                                                 ONLINE |
==========================================================""")
    print("Use 'help' command to view a list of commands w/ description.\n")

def body():
    userInput = getUserInput()

    while userInput[0] != "exit":
        print("User command is ", userInput[0])
        print("\n...Command finished")
        userInput = getUserInput()

    exit()

def getUserInput():
    userInput = input("chat: ").split(" ")
    count = 0

    while(not validateCommand(userInput)):
        count+=1
        print("Command invalid!...Use 'help' command to view a list of commands w/ description.") if (count % 3) == 0 else print("Command invalid!")
        userInput = input("chat: ").split(" ")
    
    return userInput

def validateCommand(userInput):
    validCommands = ["help", "myip", "myport", "connect", "list", "terminate", "send", "exit"]
    
    if len(userInput) == 0:
        return False
    
    for command in validCommands:
        if userInput[0] == command:
            return True

    return False


def help():
    # 1. help Display information about the available user interface options or command manual.
    print("help()") # <- delete once command is finished

def myip():
    # 2. myip Display the IP address of this process.
    # Note: The IP should not be your “Local” address (127.0.0.1). It should be the actual IP of the computer. 
    print("myip()")

def myport():
    # 3. myport Display the port on which this process is listening for incoming connections.
    print("myport()") # <- delete once command is finished

def connect(destinationIP, portNum):
    # This command establishes a new TCP connection to the specified
    # <destination> at the specified < port no>. The <destination> is the IP address of the computer. Any attempt
    # to connect to an invalid IP should be rejected and suitable error message should be displayed. Success or
    # failure in connections between two peers should be indicated by both the peers using suitable messages.
    # Self-connections and duplicate connections should be flagged with suitable error messages.
    print("connect(destinationIP, portNum)") # <- delete once command is finished

def list():
    # Display a numbered list of all the connections this process is part of. This numbered list will include
    # connections initiated by this process and connections initiated by other processes. The output should
    # display the IP address and the listening port of all the peers the process is connected to.
    # E.g., id: IP address    Port No.
    #        1: 192.168.21.20    4545
    #        2: 192.168.21.21    5454
    #        3: 192.168.21.23    5000
    #        4: 192.168.21.24    5000
    print("list()") # <- delete once help is finished

def terminate(connectionID):
    # This command will terminate the connection listed under the specified
    # number when LIST is used to display all connections. E.g., terminate 2. In this example, the connection
    # with 192.168.21.21 should end. An error message is displayed if a valid connection does not exist as
    # number 2. If a remote machine terminates one of your connections, you should also display a message.
    print("terminate(connectionID)") # <- delete once help is finished

def send(connectionID, message):
    # (For example, send 3 Oh! This project is a piece of cake). This will
    # send the message to the host on the connection that is designated by the number 3 when command “list” is
    # used. The message to be sent can be up-to 100 characters long, including blank spaces. On successfully
    # executing the command, the sender should display “Message sent to <connection id>” on the screen. On
    # receiving any message from the peer, the receiver should display the received message along with the
    # sender information.
    # (Eg. If a process on 192.168.21.20 sends a message to a process on 192.168.21.21 then the output on
    # 192.168.21.21 when receiving a message should display as shown:
    # Message received from 192.168.21.20
    # Sender’s Port: <The port no. of the sender>
    # Message: “<received message>”   
    print("terminate(connectionID, message)") # <- delete once help is finished

def exit():
    # Close all connections and terminate this process. The other peers should also update their connection
    # list by removing the peer that exits.
        print(r"""
==========================================================
|                                                        |
|       CCCCCCCCC   H     H      AA    TTTTTTTTTTTT      |
|      C            H     H     A  A        TT           |
|      C            HH H HH    A AA A       TT           |
|      C            H     H   A      A      TT           |
|       CCCCCCCCC   H     H  A        A     TT           |
|                                                 OFFLINE|
==========================================================""")
        print("\n")

def main():
    initialize()
    body()

if __name__ == "__main__":
    main()
