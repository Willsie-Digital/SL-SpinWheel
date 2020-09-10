#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references
import time
import clr

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Spin Wheel"
Website = "https://willsie.net"
Description = "Viewers can spin a wheel to gain or lose nuggets"
Creator = "Willsie Digital"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()
global RestPath
RestPath = os.path.join(os.path.dirname(__file__), "REST")

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Settings Overwritten"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnCooldown(ScriptName,ScriptSettings.Command):
         Parent.SendStreamMessage("Easy there cowboy. Wait for the wheel to stop spinning.")

    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("You can't spin for another " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)) + " seconds")

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnCooldown(ScriptName,ScriptSettings.Command) and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':true}")
        Parent.SendStreamMessage("CoolCat It's time to spin the wheel!")    # Send your message to chat TODO: WE NEED TO REMOVE THIS SETTING
        Parent.AddCooldown(ScriptName,ScriptSettings.Command,40) # Put the command on global cooldown

        thread = threading.Thread(target=ReadWheelResults)
        thread.start()
        
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on user cooldown
        

    return

#---------------------------
#   Command Function
#---------------------------
def AddPointsAll(PayoutAmount):
    """Add points to all users"""
    Mydict = {}
    for viewer in Parent.GetViewerList():
        Mydict[viewer] = PayoutAmount

    Parent.AddPointsAll(Mydict)

def RemovePointsAll(PayoutAmount):
    """Remove points to all users"""
    Mydict = {}
    for viewer in Parent.GetViewerList():
        Mydict[viewer] = PayoutAmount

    Parent.RemovePointsAll(Mydict)

def ReadWheelResults():
    # Open the nuggets file (this file gets updated after our javascript overlay kicks back results)
    time.sleep(26)
    f = open(RestPath + "/nuggetsinbound.dat")
    nuggets = f.read()

    # Let's deal with the raffle
    if nuggets == "raf":
        Parent.SendStreamMessage("OMG It's a Raffle")
        
    elif nuggets == "0":
        Parent.SendStreamMessage("TearGlove Nobody get's any kix")
    elif nuggets == "-500":
        nuggets = nuggets[1:]
        RemovePointsAll(nuggets)
        Parent.SendStreamMessage("NotLikeThis Way to go... everybody lost " + nuggets + " kix" )
    else:
        AddPointsAll(nuggets)
        Parent.SendStreamMessage("OhMyDog Everybody gets " + nuggets + " kix!")

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse():
    return 

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return