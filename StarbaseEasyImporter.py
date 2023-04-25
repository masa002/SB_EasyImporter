import wx
import os
import shutil

class FileDropCopy(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.appdata = os.getenv("APPDATA")
        self.blueprints_path = "/Starbase/ssc/autosave/ship_blueprints/"

    def GetFileNum(self):
        return sorted([int(os.path.splitext(f)[0].split('_')[1]) 
        for f in os.listdir(self.appdata + self.blueprints_path) 
        if os.path.splitext(f)[1] == ".fbe"])[-1]

    def OnDropFiles(self, x, y, filenames):
        error = ""
        if len(filenames) > 1:
            error += 'You can only import one file at a time.\n'
        if os.path.splitext(filenames[0])[1] != ".fbe":
            error += 'You can only import .fbe file.\n'
        if error != "":
            wx.MessageBox(error, "Error", wx.OK | wx.ICON_ERROR)
            return 0

        else:
            try:
                shutil.copy(filenames[0], self.appdata + self.blueprints_path +
                "ship_" + str(self.GetFileNum() + Frame.GetRadio(self.window)) + ".fbe")
                wx.MessageBox("Imported.", "Success", wx.OK | wx.ICON_INFORMATION)
            except:
                wx.MessageBox("Failed to import.", "Error", wx.OK | wx.ICON_ERROR)
                return 0

            return 0

class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(235, 410), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER))
        
        panel = wx.Panel(self)
        
        radio = wx.RadioBox(panel, 1, "Overwrite or New File", pos=(10, 10), size=(200, 70), 
        choices=['Overwrite', 'New File(Game must be reboot.)'], majorDimension=1, style=wx.RA_SPECIFY_COLS)

        radio.SetItemLabel(0, "Overwrite")
        radio.SetItemLabel(1, "New File(Game must be reboot.)")

        wx.StaticText(panel, -1, "Drop .fbe file here.", (10, 90))

        drop_panel = wx.Panel(panel, -1, pos=(10, 110), size=(200, 210), style=wx.SIMPLE_BORDER)
        drop_panel.SetBackgroundColour("white")
        drop_panel.SetDropTarget(FileDropCopy(drop_panel))

        wx.StaticText(panel, -1, "Starbase Easy Importer v1.0\nCreate by Masakk(masa002)", (10, 330))

    def GetRadio(self):
        if self.FindWindowById(1).GetStringSelection() == "Overwrite":
            return 0
        else:
            return 1

if __name__ == "__main__":
    app = wx.App()
    frame = Frame(None, -1, "Starbase Easy Importer")
    frame.Show()
    app.MainLoop()