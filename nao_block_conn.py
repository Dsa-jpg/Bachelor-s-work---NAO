import urllib
import urllib2

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.tts = ALProxy('ALTextToSpeech')

    def onInput_onStart(self):
        try:
            # Data, která chcete odeslat
            data = {"key": "value"}
            # Kódování dat
            encoded_data = urllib.urlencode(data)
            # Vytvoření HTTP požadavku
            request = urllib2.Request("http://localhost:9999", encoded_data)
            # Odeslání požadavku
            response = urllib2.urlopen(request)
            if response.getcode() == 200:
                print("Data successfully sent to the server.")
                # Přečtení odpovědi ze serveru
                server_response = response.read()
                self.tts.say("Response from the server: " + server_response)

            else:
                self.tts.say("Failed to send data to the server. Status code:" + response.getcode())
        except Exception as e:
            self.tts.say("Failed to send data to the server:", str(e))
    
    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()

