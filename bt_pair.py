import pexpect
import subprocess

def pair_trust():
    child = pexpect.spawn("bluetoothctl", encoding='utf-8')
    child.sendline('discoverable on')
    child.sendline('agent off')
    child.sendline('agent DisplayYesNo')
    child.sendline('default-agent')
    try:
        child.expect("(yes/no)", timeout=20)
        print(child.before)
        res = input("[y]es/[n]o: ")
        if(res[0]=='y'):
            child.send("yes\ntrust\n")
    except:
        print("Already connected or pairing declined on other device.")


if __name__=='__main__':
    pair_trust()