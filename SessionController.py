import telnetlib
import time
import threading
import subprocess
import logging
import socket

log = logging.getLogger(__name__)


class OpenOCDSession(threading.Thread):
    def __init__(self, args=[]):
        self.stdout = None
        self.stderr = None

        cmd = ["openocd"]
        for arg in args:
            cmd.append(arg)

        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=False)
        threading.Thread.__init__(self)

    def run(self):
        self.stdout, self.stderr = self.p.communicate()
        # print(self.stderr)
        # print(self.stdout)


class SessionController:
    def __init__(self):
        self.tn = None
        self.is_open = False
        self.session = None

    def start_session(self, init_args):
        self.session = OpenOCDSession(args=init_args)
        self.session.start()

        for _ in range(100):
            time.sleep(0.1)
            try:
                self.tn = telnetlib.Telnet("127.0.0.1", "4444")
                response = 'Success'
                break
            except:
                response = 'Failed'
            finally:
                print(response)

        self.is_open = True

    def close(self):
        self.tn.write("shutdown\n".encode('utf8'))
        result = self.tn.read_all()
        self.is_open = False
        self.tn = None
        return result

    def send(self, msg):
        self.tn.write(msg.encode('utf8'))


