# Uncomment this to pass the first stage
import socket
import threading

def handle_client(conn):
    # request ok response
    request_ok = b"HTTP/1.1 200 OK\r\n\r\n"

    # request not found response
    request_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # receive data
    received_data = conn.recv(1024).decode("utf-8")
    request_target = received_data.split()[1]

    # check if request target is /test
    if request_target == "/":
        conn.sendall(request_ok)

    elif request_target.startswith("/echo"):
        request_string = request_target[6:]

        # status code
        status_code = "HTTP/1.1 200 OK\r\n"

        # response headers
        content_type = "Content-Type: text/plain\r\n"
        content_length = f"Content-Length: {len(request_string)}\r\n"

        #response
        response = f"{status_code}{content_type}{content_length}\r\n{request_string}"
        conn.sendall(response.encode("utf-8"))

    elif request_target == "/user-agent":
        # retrieve user agent
        request_components = received_data.split("\r\n")
        user_agent = [component for component in request_components if "User-Agent: " in component][0]
        user_agent = user_agent.split(": ")[1]

        # status code
        status_code = "HTTP/1.1 200 OK\r\n"

        # response headers
        content_type = "Content-Type: text/plain\r\n"
        content_length = f"Content-Length: {len(user_agent)}\r\n"

        #response
        response = f"{status_code}{content_type}{content_length}\r\n{user_agent}"
        conn.sendall(response.encode("utf-8"))

    else:
        conn.sendall(request_not_found)


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client.
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()


if __name__ == "__main__":
    main()
