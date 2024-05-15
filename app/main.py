# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client

    # request ok response
    request_ok = b"HTTP/1.1 200 OK\r\n\r\n"

    # request not found response
    request_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # send response
    conn.sendall(request_ok)

    # receive data
    received_data = conn.recv(1024).decode("utf-8")
    request_target = received_data.split()[1]

    # check if request target is /test
    if request_target == "/":
        conn.sendall(request_ok)
    else:
        conn.sendall(request_not_found)


if __name__ == "__main__":
    main()
