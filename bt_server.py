import bluetooth as bt
import subprocess
import threading
from demo_store import get_files
from message_utils import *
from StreamParser import StreamParser

class BTServer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.uuid = "0446eb5c-d775-11ec-9d64-0242ac120002"
        self.client = None
        self.stream_parser = StreamParser()

        self.handlers = {
            CLEAR: lambda msg: None,
            GET_FILES_REQUEST: lambda msg: self.send(str(get_files()).encode(), JSON_DATA),
            FLASH_REQUEST: lambda msg: print(msg[5:].decode("utf-8"))
        }

    def run(self):

        # must be discoverable to advertise
        subprocess.call(["bluetoothctl", "discoverable", "on"])

        server = bt.BluetoothSocket(bt.RFCOMM)
        print("socket created")
        server.bind(("", bt.PORT_ANY))

        # Start listening. One connection
        server.listen(1)
        port = server.getsockname()[1]

        bt.advertise_service(server, "BTSrv",
                             service_id=self.uuid,
                             service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                             profiles=[bt.SERIAL_PORT_PROFILE])

        while True:
            print(f"Waiting for connection on RFCOMM channel {port}")

            try:
                self.client, addr = server.accept()
                print("Connected with: " +  str(addr))

                while True:
                    data = self.client.recv(1024)
                    msg = self.stream_parser.parse(data)
                    if msg:
                        self.receiveMessage(msg)

            except IOError as e:
                print(e)
            except KeyboardInterrupt:
                if self.client is not None:
                    self.client.close()

                server.close()

                print("Server closing")
                break


    def send(self, message, msg_type):
        message = prep_message(message, msg_type)       # adding header
        # print(message[5:].decode('utf-8'))
        self.client.send(message)


    def receiveMessage(self, message):
        self.handlers[int(message[0])](message)


def main():
    server = BTServer()
    server.run()
    #    print(str(get_files()))
    #    print(len(str(get_files())))
    #    print(len(str(get_files()).encode('utf-8')))

if __name__ == '__main__':
    main()
