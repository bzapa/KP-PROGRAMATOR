from menu import *
import threading
import pexpect

INACTIVE = 0
AGENT_SETUP = 1
AWAITING_CONNECTION = 2
AWAITING_INPUT = 3


class PairDialog(MenuItem):
    def __init__(self):
        super().__init__("Enable pairing")
        self.height = 16
        self.width = 96
        self.pairThread = PairThread()

    @property
    def visible_text(self):
        return self.pairThread.display_text + "\n" + "YES [OK]    NO [<-]"

    def on_click(self, select=True):
        print("clicked", select)
        if self.pairThread.state == INACTIVE:
            self.pairThread = PairThread()
            self.pairThread.start()
        elif self.pairThread.state == AGENT_SETUP:
            pass
        elif self.pairThread.state == AWAITING_CONNECTION:
            pass
        else:
            self.pairThread.notify(select)
            # self.pairThread.decision = select
            # self.pairThread.event.set()

    def draw(self, draw, x, y):
        if self.is_selected:
            draw.rectangle((x, y, x + self.width, y + self.height),
                           outline=1, fill=0)
        # Endline looked bad.
        draw.text((x + 1, y), self.pairThread.display_text, font=FONT, fill=1)
        draw.text((x + 1, y+8), "YES [OK]    NO [<-]", font=FONT, fill=1)


class PairThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.state = INACTIVE
        self.display_text = "Enable pairing"
        self.event = threading.Event()
        self.decision = None

    def run(self):
        self.state = AGENT_SETUP
        # print("agent setup")
        self.display_text = "setup ..."
        child = pexpect.spawn("bluetoothctl", encoding='utf-8')
        child.sendline('discoverable on')
        child.sendline('agent off')
        child.sendline('agent DisplayYesNo')
        child.sendline('default-agent')

        # print("waiting for connection")
        self.display_text = "connect now"
        fail = None
        try:
            self.state = AWAITING_CONNECTION
            child.expect("(yes/no)", timeout=20)
            print(child.before)
            self.display_text = child.before[-17:-2]
            self.state = AWAITING_INPUT
            self.event.wait()
            if self.decision == True:
                child.send("yes\ntrust\n")
            else:
                child.send("no\n")
        except:
            fail = True
        if fail:
            self.display_text("not paired. pair again?")
        else:
            self.display_text("paired. pair again?")
        self.state = INACTIVE

    def notify(self, decision):
        print("decisoin", decision)
        self.decision = decision
        self.event.set()
