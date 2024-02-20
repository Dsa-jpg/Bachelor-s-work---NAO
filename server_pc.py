import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive data and handle client connection
        self.data = self.request.recv(1024).strip()
        print("{} says: {}".format(self.client_address[0], self.data.decode("utf-8")))

        # Process received data
        processed_data = self.process_data(self.data)

        # Send response back to the client
        response = "Message has been successfully received and processed."
        self.request.sendall(response.encode("utf-8"))

    def process_data(self, data):
        # Here you can perform processing of received data
        # For example, you can implement code to process the data and return a response

        # In this example, we simply return the same data back
        return data

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create TCP server
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Start the server to listen on the specified port
        print("Server is running on address {} and port {}".format(HOST, PORT))
        server.serve_forever()
