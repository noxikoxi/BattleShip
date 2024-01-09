import random
import socket


class Client:
    def __init__(self):
        self.name = socket.gethostname()
        self.serverIp = socket.gethostbyname(self.name)
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
            if data:
                print(f'Otrzymano dane z serwera: {data.decode()} ')
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
        print(f'\nFirst player name: {self.client1Name}')

        self.client2Socket, self.client2Address = self.socket.accept()
        print(f"Connected with: {self.client2Address}")
        print(f"Second player has connected.")

        self.client2Name = self.client2Socket.recv(1024).decode()
        print(f'\nSecond player name: {self.client2Name}')

        self.sendData(self.client1Socket, self.client2Name)
        self.sendData(self.client2Socket, self.client1Name)

    def sendData(self, s, data):
        s.send(data.encode(), )

    def handleGame(self):

        mess1 = self.client1Socket.recv(1024).decode()
        mess2 = self.client2Socket.recv(1024).decode()

        if mess1 != "READY" or mess2 != "READY":
            print("\nCommunication error.\nTry launching the game again.")
            self.sendData(self.client1Socket, "ERROR")
            self.sendData(self.client2Socket, "ERROR")
            return
        print("Both players are ready.\nStarting the game.")

        turn = random.random()
        if turn <= 0.5:
            self.sendData(self.client1Socket, "TURN")
            handling_client = 1
            print(f'Sent "TURN" to: {self.client1Name}')
        else:
            self.sendData(self.client2Socket, "TURN")
            handling_client = 2
            print(f'Sent "TURN" to: {self.client2Name}')

        while True:
            if handling_client == 1:
                message = self.client1Socket.recv(1024).decode()
                print(f'Received {message} from {self.client1Name}')

                self.sendData(self.client2Socket, message)

                if message.split(' ')[0] == "SHOOT":
                    handling_client = 2
                elif message.split(' ')[0] == "SHIP":
                    self.sendData(self.client2Socket, "TURN")
                    handling_client = 2
                elif message.split(' ')[0] == 'SHIP_SUNK':
                    self.sendData(self.client2Socket, "TURN")
                    handling_client = 2
                elif message.split(' ')[0] == "WATER":
                    self.sendData(self.client1Socket, "TURN")
                    handling_client = 1
                elif message.split(' ')[0] == "GAME_OVER":
                    break

            elif handling_client == 2:
                message = self.client2Socket.recv(1024).decode()
                print(f'Received {message} from {self.client2Name}')

                self.sendData(self.client1Socket, message)

                if message.split(' ')[0] == "SHOOT":
                    handling_client = 1
                elif message.split(' ')[0] == "SHIP":
                    self.sendData(self.client1Socket, "TURN")
                    handling_client = 1
                elif message.split(' ')[0] == 'SHIP_SUNK':
                    self.sendData(self.client1Socket, "TURN")
                    handling_client = 1
                elif message.split(' ')[0] == "WATER":
                    self.sendData(self.client2Socket, "TURN")
                    handling_client = 2
                elif message.split(' ')[0] == "GAME_OVER":
                    break

    def __del__(self):
        self.socket.close()
        self.client1Socket.close()
        self.client2Socket.close()


if __name__ == '__main__':
    server = Server()
    server.start_server()
    server.wait_for_clients()
    server.handleGame()
