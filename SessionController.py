import telnetlib
import time
import threading
import subprocess
import logging
import socket
from concurrent import futures

log = logging.getLogger(__name__)


# class OpenOCDSession(threading.Thread):
#     def __init__(self, args=[]):
#         self.stdout = None
#         self.stderr = None
#
#         cmd = ["openocd"]
#         for arg in args:
#             cmd.append(arg)
#
#         self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#                                   shell=False)
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.stdout, self.stderr = self.p.communicate()
#         print("stdout", self.stdout, "\n")
#         print("stderr", self.stderr, "\n")

class FlashService(object):

    def __init__(self):
        super().__init__()
        self.executor = futures.ThreadPoolExecutor(max_workers=1)

    def start_async(self, args):
        return self.executor.submit(self.resend, args)

    def flash(self, args):

        cmd = ["openocd"]
        for arg in args:
            cmd.append(arg)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  shell=False)
        return p.communicate()


# class SessionController(object):
#     def __init__(self):
#         self.tn = None
#         self.is_open = False
#         self.session = None
#
#     def start_session(self, init_args):
#         if not self.session is None:
#             self.close()
#         self.session = OpenOCDSession(args=init_args)
#         self.session.start()
#
#         success = None
#         for _ in range(100):
#             time.sleep(0.1)
#             try:
#                 self.tn = telnetlib.Telnet("127.0.0.1", "4444")
#                 success = True
#                 break
#             except:
#                 success = False
#
#         if success == False:
#             return
#         self.is_open = True
#
#     def close(self):
#         if not self.is_open:
#             return None
#         self.tn.write("shutdown\n".encode('utf8'))
#         result = self.session.stderr
#         try:
#             result = self.tn.read_all()
#         except:
#             pass
#         self.is_open = False
#         self.tn = None
#         return result
#
#     def send(self, msg):
#         self.tn.write(msg.encode('utf8'))
