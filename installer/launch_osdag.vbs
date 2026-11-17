Set objShell = CreateObject("Wscript.Shell")
root = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

cmd = "cmd /c ""set PATH=" & root & "\Library\bin;" & root & "\Scripts;%PATH% && """ & root & "\Scripts\osdag.exe"""""

objShell.Run cmd, 0
