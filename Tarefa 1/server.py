import socket
import threading

host = 'localhost'
port = 8000

def multithreading_client(client):
    data_request = client.recv(1024).decode()
    first_line = data_request.split("\n")[0]
    request_method = first_line.split()[0]


    if request_method == 'GET':
        data = "HTTP/1.1 200 OK\n\n"
        with open('index.html', 'r') as fin:
            content = fin.read()
        response = data + content
        client.send(response.encode())
    elif request_method == 'POST':
        user_and_password = data_request.split("\n")[-1].split("=")
        user = user_and_password[1].split("&")[0]
        password = user_and_password[2].split()[0]

        if user == 'admin' and password == '1234':
            data = "HTTP/1.1 200 OK\n\n"
            with open('logoff.html', 'r') as fin:
                content = fin.read()
                content = content.replace('<h1>Bem Vindo!</h1>', f'<h1>Bem Vindo! IP DNS: {socket.gethostbyname(host)}</h1>')
            response = data + content
            client.send(response.encode())
        else:
            data = "HTTP/1.1 404 Not Found\n\n"
            with open('notfound.html', 'r') as fin:
                content = fin.read()
            response = data + content
            client.send(response.encode())

    client.close()

def createServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    while True:
        client, _ = server.accept()
        client_thread = threading.Thread(target=multithreading_client, args=(client,))
        client_thread.start()
createServer()