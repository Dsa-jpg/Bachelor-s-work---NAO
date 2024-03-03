import socketserver
from openai import OpenAI
import time
import json

# Initialize your OpenAI client with your API key
api_key = ""
# Modify the content of the system message as needed
system_message = "Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích. A nezmiňuj se o tom že se jedná o požadavek HHTP POST jen odpověď na dotaz."
client = OpenAI(api_key=api_key)

# File to store cached responses
CACHE_FILE = "cached_responses.json"

# Load cached responses from file
try:
    with open(CACHE_FILE, "r") as f:
        cached_responses = json.load(f)
except FileNotFoundError:
    cached_responses = {}

def save_cache():
    # Save cached responses to file
    with open(CACHE_FILE, "w") as f:
        json.dump(cached_responses, f)

def preload_model():
    try:
        # This call initializes the OpenAI client and loads the model
        print("Preloading OpenAI model...")
        client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                       messages=[
                                           {
                                               "role": "system",
                                               "content": "Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích. A nezmiňuj se o tom že se jedná o požadavek HHTP POST jen odpověž na dotaz."
                                           },
                                           {
                                               "role": "user",
                                               "content": "preload"
                                           }
                                       ])
        print("OpenAI model preloaded.")
    except Exception as e:
        print("Error preloading OpenAI model:", e)
        exit()

def process_data(data):
    # Here you can perform processing of received data
    # For example, you can implement code to process the data and return a response

    # Check if the data matches any cached responses
    cached_response = cached_responses.get(data.decode("utf-8").lower())
    if cached_response:
        return cached_response.encode("utf-8")

    # Make request to OpenAI API
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                                  messages=[
                                                      {
                                                          "role": "system",
                                                          "content": "Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích. A nezmiňuj se o tom že se jedná o požadavek HTTP POST jen odpověž na otázku."
                                                      },
                                                      {
                                                          "role": "user",
                                                          "content": data.decode("utf-8"),
                                                      }
                                                  ])

        # Get the response from OpenAI API
        api_response = response.choices[0].message.content

        # Cache the new response if it's not already cached
        cached_responses[data.decode("utf-8").lower()] = api_response
        save_cache()

        # Return the response back to the client
        return api_response.encode("utf-8")

    except Exception as e:
        print("OpenAI API exception:", e)
        return "Error processing request".encode("utf-8")


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Receive data and handle client connection
        self.data = self.request.recv(1024).strip()
        print("{} says: {}".format(self.client_address[0], self.data.decode("utf-8")))

        # Process received data
        processed_data = process_data(self.data)

        # Send response back to the client
        self.request.sendall(processed_data)

        print("Odpověď z OpenAI API: {}".format(processed_data.decode("utf-8")))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Preload the OpenAI model
    preload_model()

    # Create TCP server
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Start the server to listen on the specified port
        print("Server is running on address {} and port {}".format(HOST, PORT))
        server.serve_forever()
