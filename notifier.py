from mcstatus import MinecraftServer
import time
from datetime import datetime
from win10toast import ToastNotifier
import config as cfg

toaster = ToastNotifier()

oldList = []
newList = []

online = False


def checkserver():
    try:
        global oldList
        global newList
        global online

        if not online:
            toaster.show_toast("Info", "Server has Startet!")
            online = True

        server = MinecraftServer(cfg.ip, cfg.port)

        # 'query' has to be enabled in a servers' server.properties file.
        query = server.query()

        newList = query.players.names
        newList.sort()
        print(newList)

        if newList != oldList:
            print("changed")
            checklists(oldList, newList)
            oldList = newList
        else:
            print("same")


    except:
        print("Server not reachable!")
        if online:
            toaster.show_toast("Error", "Server crashed!")
            online = False

    return;


def checklists(a, b):
    disconnected = set(a) - set(b)
    connected = set(b) - set(a)

    if (len(disconnected) > 0):
        print("Disconnected: {0}".format(disconnected))
        toaster.show_toast("Disconnected", ", ".join(disconnected))
    if (len(connected) > 0):
        print("Connected: {0}".format(connected))
        toaster.show_toast("Connected", "\n".join(connected))

    return;


while True:
    print("")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    str(datetime.now())
    checkserver()
    time.sleep(cfg.interval)
