# Uncomment this to pass the first stage
import argparse
import socket
import threading

def handle_client(conn, args):
    # request ok response
    request_ok = b"HTTP/1.1 200 OK\r\n\r\n"

    # request not found response
    request_not_found = b"HTTP/1.1 404 Not Found\r\n\r\n"

    # receive data
    received_data = conn.recv(1024).decode("utf-8")
    request_method = received_data.split()[0]
    request_target = received_data.split()[1]

    # check if request target is /
    if request_target == "/":
        conn.sendall(request_ok)

    # check if request target is /echo
    elif request_target.startswith("/echo/"):
        # retrieve request string
        request_string = request_target[6:]

        # status code
        status_code = "HTTP/1.1 200 OK\r\n"

        # response headers
        content_type = "Content-Type: text/plain\r\n"
        content_length = f"Content-Length: {len(request_string)}\r\n"

        #response
        response = f"{status_code}{content_type}{content_length}\r\n{request_string}"
        conn.sendall(response.encode("utf-8"))

    # check if request target is /user-agent
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

    elif request_target.startswith("/files/"):
        # retrieve file name and directory
        request_file = request_target[7:]
        directory = args.directory

        if request_method == "GET":
            # open file
            try:
                with open(f"{directory}/{request_file}", "rb") as file:
                    request_file = file.read().decode("utf-8")
            except FileNotFoundError:
                conn.sendall(request_not_found)
                return

            # status code
            status_code = "HTTP/1.1 200 OK\r\n"

            # response headers
            content_type = "Content-Type: application/octet-stream\r\n"
            content_length = f"Content-Length: {len(request_file)}\r\n"

            #response
            response = f"{status_code}{content_type}{content_length}\r\n{request_file}"
            conn.sendall(response.encode("utf-8"))

        elif request_method == "POST":
            # open file
            with open(f"{directory}/{request_file}", "wb") as file:
                file.write(received_data.split("\r\n\r\n")[1].encode("utf-8"))

            # status code
            status_code = "HTTP/1.1 201 OK\r\n\r\n"

            conn.sendall(status_code.encode("utf-8"))


    # return 404 if request target is not found
    else:
        conn.sendall(request_not_found)
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Directory to serve files from")
    args = parser.parse_args()

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # assign a new thread to handle each concurrent client
    while True:
        conn, addr = server_socket.accept() # wait for client.
        client_thread = threading.Thread(target=handle_client, args=(conn, args))
        client_thread.start()


if __name__ == "__main__":
    main()
