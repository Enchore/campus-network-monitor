Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "F:\stepclaw\tools\campus-network-monitor"
WshShell.Run "C:\Python313\python.exe monitor.py", 0, False
Set WshShell = Nothing
