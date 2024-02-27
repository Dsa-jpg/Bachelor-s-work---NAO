import socketserver
from openai import OpenAI
import time

# Initialize your OpenAI client with your API key
api_key = ""
client = OpenAI(api_key=api_key)

def process_data(data):
    # Here you can perform processing of received data
    # For example, you can implement code to process the data and return a response

    # Measure the time before making the request
    start_time = time.time()

    # Make request to OpenAI API
    response = client.chat.completions.create(model="gpt-3.5-turbo-0125",
                                              messages=[
                                                  {
                                                      "role": "system",
                                                      "content": "Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích. A nezmiňuj se o tom že se jedná o požadavek HHTP POST jen odpověž na dotaz."
                                                  },
                                                  {
                                                      "role": "user",
                                                      "content": data.decode("utf-8"),
                                                  }
                                              ])

    # Calculate the time taken for the response
    end_time = time.time()
    response_time = end_time - start_time

    # Get the response from OpenAI API
    api_response = response.choices[0].message.content

    # Print the response and the time taken
    print("OpenAI Response: {}".format(api_response))
    print("Response Time: {:.2f} seconds".format(response_time))

    # Return the response back to the client
    return api_response.encode("utf-8")


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive data and handle client connection
        self.data = self.request.recv(1024).strip()
        print("{} says: {}".format(self.client_address[0], self.data.decode("utf-8")))

        # Process received data
        processed_data = process_data(self.data)

        # Send response back to the client
        self.request.sendall(processed_data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create TCP server
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Start the server to listen on the specified port
        print("Server is running on address {} and port {}".format(HOST, PORT))
        server.serve_forever()
