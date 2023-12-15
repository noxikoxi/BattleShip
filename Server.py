import socket
import threading


class Client:
    def __init__(self):
        self.name = socket.gethostname()
        self.serverIp = "192.168.100.10"
        self.serverPort = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

    def updateIp(self, ip):
        self.serverIp = ip

    def connect_with_server(self):
        print("Connecting with server...")
        self.socket.connect((self.serverIp, self.serverPort))
        print(f'Connected with server: {self.serverIp}:{self.serverPort}')
        self.isConnected = True

    def waitForData(self):
        while True:
            data = self.socket.recv(1024)
            if not data:
                raise(ValueError("Nie otrzymano danych z serwera..."))
            else:
                print('Otrzymano dane z serwera')
                return data.decode()

    def sendData(self, data):
        self.socket.send(data.encode())

    def __del__(self):
        self.socket.close()


class Server:
    def __init__(self):
        self.name = socket.gethostname()
        self.ip = socket.gethostbyname(self.name)
        self.port = 5555
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client1Socket = None
        self.client1Address = None
        self.client2Socket = None
        self.client2Address = None

        self.client1Name = None
        self.client2Name = None

    def start_server(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))

        # Max 2 connections
        self.socket.listen(2)
        print(f'Server started on : {self.ip}:{self.port}')

    def wait_for_clients(self):
        # Akceptowanie połączenia od klienta
        print(f'Waiting for players to connect...')
        self.client1Socket, self.client1Address = self.socket.accept()
        print(f"Connected with: {self.client1Address}")
        print(f"First player has connected, waiting for second player to connect...")

        self.client1Name = self.client1Socket.recv(1024).decode()
        print(f'First player name: {self.client1Name}')

        self.client2Socket, self.client2Address = self.socket.accept()
        print(f"Connected with: {self.client2Address}")
        print(f"Second player has connected.\nStarting the Game.")

        self.client2Name = self.client2Socket.recv(1024).decode()
        print(f'Second player name: {self.client2Name}')

        self.sendData(self.client1Socket, self.client2Name)
        self.sendData(self.client2Socket, self.client1Name)

    def sendData(self, s, data):
        # Obsługa komunikacji z klientem
        s.send(data.encode())

    def handleClient(self):
        pass

    # def waitForData(self):
    #     while True:
    #         data = self.client_socket.recv(1024)
    #         if not data:
    #             break
    #         else:
    #             print(f'Otrzymałem dane od klienta')
    #             return data

    def __del__(self):
        self.socket.close()
        # self.client_socket.close()


if __name__ == '__main__':
    server = Server()
    server.start_server()
    server.wait_for_clients()


