"""
settings.py
Kevin Xu and Raymond Wu

This file contains the functions that read and write to settings file.
IMPORTANT: Also contains the function saveDefaultSettings() which resets the settings file to default.
Use if settings file is corrupted (most likely only happens due to merge errors).
"""

# defaultSettings = ["Win Score", 5, "Bullet Load", 5, "Reload Period", 5, "Bullet Life", 6]


def getSettings():
    # reads from settings.txt
    settingsFile = open("settings.txt", "r")
    settings = [] # Initialize an empty list
    while True:
        # Add the diffent lines of values to the list
        line = settingsFile.readline()
        if line == "":
            break
        settings.append(int(line.split("\n")[0]))
    return settings # Returns the list of values


# Takes the current values of the four settings and writes them to the settings file
# One value on each line
def saveSettings(winScore, bulletLoad, reloadPeriod, bulletLife):
    settingsFile = open("settings.txt", "w")
    settings = [winScore, bulletLoad, reloadPeriod, bulletLife]
    for i in range(len(settings)):
        settingsFile.write(str(settings[i]) + "\n")
    settingsFile.close()


# Resets the settings file to default
def saveDefaultSettings():
    defaultSettings = ["Win Score", 5, "Bullet Load", 5, "Reload Period", 5000, "Bullet Life", 6000]
    settingsFile = open("settings.txt", "w")
    for i in range(len(defaultSettings)):
        if i % 2 == 1:
            settingsFile.write(str(defaultSettings[i]) + "\n")
    settingsFile.close()



# Debugging Code
# print(getSettings())
# saveSettings(5, 4, 1000, 5000)
# print(getSettings())
# saveDefaultSettings()
# print(getSettings())


