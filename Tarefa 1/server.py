import socket
host = 'localhost'
port = 8941

def createServer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(1)
    
    while True:
        client, _ = server.accept()
        data_request = client.recv(1024).decode()
       
        
        first_line = data_request.split("\n")[0]
        request_method = first_line.split()[0]
        
        print(request_method)
        
        if(request_method == 'GET'):
             data = "HTTP/1.1 200 OK\n\n"
             fin = open('index.html')
             content = fin.read()
             fin.close()
             response = data + content
             client.send(response.encode())
                
        elif(request_method == 'POST'):
            user_and_password = data_request.split("\n")[-1].split("=")
            user = user_and_password[1].split("&")[0]
            password = user_and_password[2].split()[0]

            if( user == 'admin' and  password == '1234' ):
                data = "HTTP/1.1 200 OK\n\n"
                fin = open('logoff.html')
                content = fin.read()
                fin.close()
                response = data + content
                client.send(response.encode())
            else:
                data = "HTTP/1.1 404 Not Found\n\n"
                fin = open('notfound.html')
                content = fin.read()
                fin.close()
                response = data + content
                client.send(response.encode())
createServer()