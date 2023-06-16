defaultSettings = ["Win Score", 5, "Bullet Load", 5, "Reload Period", 5, "Bullet Life", 6]

settingsFile = open("settings.txt", "r")
settings = []

def getSettings():
    while True:
        line = settingsFile.readline()
        if line == "":
            break
        settings.append(int(line.split("\n")[0]))
    return settings

def saveSettings():
    settingsFile = open("settings.txt", "w")
    for i in range(len(settings)):
        settingsFile.write(settings[i] + "\n")
    settingsFile.close()

def saveDefaultSettings():
    settingsFile = open("settings.txt", "w")
    for i in range(len(defaultSettings)):
        if (i + 1) % 2 == 0:
            settingsFile.write(str(defaultSettings[i]) + "\n")
        # settingsFile.write(str(defaultSettings[i][1]) + "\n")
    settingsFile.close()



print(getSettings())


