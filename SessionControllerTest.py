from SessionController import *

if __name__ == "__main__":
    sc = SessionController()
    sc.start_session(["-f", "/home/pi/openocd/tcl/interface/raspberrypi-native.cfg",
                      "-c", "transport select swd",
                      "-c", "bcm2835gpio srst_num 24",
                      "-f", "/home/pi/openocd/tcl/target/stm32f0x.cfg"])
    time.sleep(5)
    sc.send("halt reset\n")
    sc.send("targets\n")
    sc.send("program file.elf verify\n")
    time.sleep(3)
    print(sc.close())