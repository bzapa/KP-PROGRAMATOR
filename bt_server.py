import subprocess

import bluetooth as bt

class BTServer(object):

    def __init__(self):

        self.uuid = "0446eb5c-d775-11ec-9d64-0242ac120002"
        self.client = None

    def start(self):

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
                print("Connected with: " + str(addr))

                while True:
                    data = self.client.recv(1024)
                    print(data)
                    msg = data.decode('utf-8')
                    print(msg)
                    self.handleMessage(msg)

            except IOError:
                pass
            except KeyboardInterrupt:
                if self.client is not None:
                    self.client.close()

                server.close()

                print("Server closing")
                break

    def send(self, message):
        self.client.send(message.encode('utf-8'))

    def handleMessage(self, message):
        print(f"Received msg: {message}")
        self.send(str("Received msg: " + message))



def main():
    server = BTServer()
    server.start()


if __name__ == '__main__':
    main()

