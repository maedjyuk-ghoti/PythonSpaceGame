""" audio.py """
from src.lib.OSC import OSCClient, OSCMessage, OSCBundle
import src.borg as Borg


class Audio(Borg.Borg):
    """ controls osc messages """
    def __init__(self, address="localhost", port=7110):
        """ init """
        self.serv_addr = address
        self.serv_port = port
        self.client = OSCClient()
        self.client.connect((self.serv_addr, self.serv_port))
        self.root_address = "/spacegame"
        self.bundle = OSCBundle()

    def quit(self):
        """ Quits the audio server """
        self.client.send(OSCMessage("/quit"))

    def get_server_address(self):
        """ gets server address """
        return self.serv_addr

    def get_server_port(self):
        """ gets server port """
        return self.serv_port

    def create_bundle(self):
        """ Create an osc bundle, wiping out the old one if it existed """
        self.bundle = OSCBundle()

    def delete_bundle(self):
        """ Deletes the message """
        self.bundle = None

    def add_to_bundle(self, address, data):
        """ adds data to the bundle """
        temp_message = OSCMessage(self.root_address + address)
        temp_message.append(data)
        self.bundle.append(temp_message)

    def send(self):
        """ sends a message to the server """
        self.client.send(self.bundle)

    def quit_server(self):
        """ sends the quit message to the synth server """
        self.client.send(OSCMessage("/quit"))
