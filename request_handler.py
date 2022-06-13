import time
import threading
from concurrent import futures

from SessionController import SessionController


class RequestHandler(object):

    def __init__(self, executor: futures.Executor, session_controller: SessionController):
        super().__init__()
        self.executor = executor
        self.session_controller = session_controller

        self.request_handlers = {
            "flash": lambda args: self.executor.submit(self.flash, args)
        }

    def flash(self,  args):
        self.session_controller.start_session(args)
        # return self.executor.submit(self.session_controller.close())
        return self.session_controller.close()


    def start_async(self, request, args):
        return self.request_handlers[request](args)

    @staticmethod
    def serve(session_controller) -> "RequestHandler":
        executor = futures.ThreadPoolExecutor(max_workers=1)
        service = RequestHandler(executor, session_controller)
        return service

class Proxy(object):

    def __init__(self, executor: futures.Executor, service: RequestHandler):
        super().__init__()
        self.executor = executor
        self.service = service

    def start_async(self, request, args):
        return self.executor.submit(self.resend, request, args)

    def resend(self, request, args):

        print("[Proxy]", request, args)

        res = self.service.start_async(request, args).result()

        print(res)
        # tu chyba docelowo return none i zapis wynikow do store, a na store menu i BTServer beda observerami
        return res

    @staticmethod
    def serve(service: RequestHandler) -> "Proxy":
        executor = futures.ThreadPoolExecutor(max_workers=1)
        proxy = Proxy(executor, service)
        return proxy


if __name__ == '__main__':
    sc = SessionController()
    requestHandler = RequestHandler.serve(sc)
    proxy = Proxy.serve(requestHandler)

    request = "flash"
    args = ["-f", "/home/pi/bootloader/my_rpi.cfg",
                      "-c", "transport select swd",
                      #"-c", "bcm2835gpio srst_num 24",
                      "-f", "/home/pi/openocd/tcl/target/stm32f0x.cfg",
                      #"-c", "halt reset",
                      "-c", "targets",
                      "-c", "program /home/pi/bootloader/file.elf verify"]

    futs = [proxy.start_async(request, args) for _ in range(5)]

    print(futs)
    time.sleep(1)
    print(futs)

    for a in [fut.result() for fut in futs]:
        print(a)
