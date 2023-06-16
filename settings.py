# defaultSettings = ["Win Score", 5, "Bullet Load", 5, "Reload Period", 5, "Bullet Life", 6]
# settingsFile = open("settings.txt", "r")

settings = []


def getSettings():
    settingsFile = open("settings.txt", "r")
    settings = []
    while True:
        line = settingsFile.readline()
        if line == "":
            break
        settings.append(int(line.split("\n")[0]))
    return settings



def saveSettings(winScore, bulletLoad, reloadPeriod, bulletLife):
    settingsFile = open("settings.txt", "w")
    settings = [winScore, bulletLoad, reloadPeriod, bulletLife]
    for i in range(len(settings)):
        settingsFile.write(str(settings[i]) + "\n")
    settingsFile.close()

def saveDefaultSettings():
    defaultSettings = ["Win Score", 5, "Bullet Load", 5, "Reload Period", 5000, "Bullet Life", 6000]
    settingsFile = open("settings.txt", "w")
    for i in range(len(defaultSettings)):
        if i % 2 == 1:
            settingsFile.write(str(defaultSettings[i]) + "\n")
        # settingsFile.write(str(defaultSettings[i][1]) + "\n")
    settingsFile.close()


# print(getSettings())
# saveSettings(5, 4, 1000, 5000)
# print(getSettings())
# saveDefaultSettings()
# print(getSettings())


