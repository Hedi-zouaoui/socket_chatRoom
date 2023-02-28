import socket
import threading 
#run multiple threads (lightweight processes)
HOST='127.0.0.1'
PORT = 9090
server=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#socket.AF_INET : IPv4
#socket.SOCK_STREAM : type of socket ; stream socket
server.bind((HOST , PORT)) 
#bind the socket to a specific network address HOST -> 127.0.0.1 and PORT 9090
server.listen()
clients = []
nicknames =[]
 
def broadcast(message) : # iterate over all the connected clients stored in the list "clients"
    for client in clients : 
        client.send(message)
def handle (client) : 
    while True : 
        try : 
          message = client.recv(1024) # receiving maximum : 1024 byes
          print(f"{nicknames[clients.index(client)]} says {message}") # in the server side 
          broadcast(message)
        except : #if theres an error 
            index = clients.index(client) #get the index from the list 
            clients.remove(client) # remove it from the clients list
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname) # remove from the nicknames list 
            break
def receive():
   while True : 
        client , address = server.accept()
        print(f"Connected with {str(address)} ! ") # in consol : server side 
        client.send("X".encode('utf-8')) #send the initial message 
        nickname=client.recv(1024)
        nicknames.append(nickname) # add to the nicknames list 
        clients.append(client)# add to the clients list 
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server! \n".encode('utf-8')) # broadcasting the message to all connected clients
        client.send("connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle , args=(client , )) 
        # thread : run multiple threads (lightweight processes) 
        # target -> the next function to be ex , args -> tuble of the args to be passed to the function
        thread.start()
print("server running ...")
receive()
