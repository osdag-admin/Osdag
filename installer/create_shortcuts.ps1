param(
    [string]$InstallDir
)

$AppName = "osdag"
$Version = "1.0.0"
$AppExe = Join-Path $InstallDir "Scripts\osdag.exe"
$Launcher = Join-Path $InstallDir "launch_osdag.vbs"
$UninstallExe = Join-Path $InstallDir "Uninstall-$AppName.exe"
$IconFile = Join-Path $InstallDir "Osdag.ico"

# If user is admin?
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    $StartMenuDir = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\$AppName"
    $DesktopPath = Join-Path $env:Public "Desktop"
}else {
    $StartMenuDir = Join-Path $env:AppData "Microsoft\Windows\Start Menu\Programs\$AppName"
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
}


if (!(Test-Path $StartMenuDir)) {
    New-Item -ItemType Directory -Path $StartMenuDir | Out-Null
}
if (!(Test-Path $DesktopPath)) {
    New-Item -ItemType Directory -Path $DesktopPath | Out-Null
}

$Shell = New-Object -ComObject WScript.Shell

# ---- Desktop Shortcut ----
$Shortcut = $Shell.CreateShortcut("$DesktopPath\$AppName.lnk")
$Shortcut.TargetPath = $Launcher
$Shortcut.WorkingDirectory = "$InstallDir"
$Shortcut.IconLocation = "$IconFile,0"
$Shortcut.Save()

# ---- App Shortcut (Start Menu) ----
$Shortcut = $Shell.CreateShortcut("$StartMenuDir\$AppName.lnk")
$Shortcut.TargetPath = $Launcher
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.IconLocation = "$IconFile,0"
$Shortcut.Save()


# ---- Write Registry Entry for Uninstall ----
$SizeBytes = (Get-ChildItem $InstallDir -Recurse -Force | Measure-Object -Property Length -Sum).Sum
$SizeKB = [math]::Round($SizeBytes / 1KB)

if ($isAdmin) {

    $baseKey = [Microsoft.Win32.RegistryKey]::OpenBaseKey(
        [Microsoft.Win32.RegistryHive]::LocalMachine,
        [Microsoft.Win32.RegistryView]::Registry64
    )

    $subKey = $baseKey.CreateSubKey(
        "Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
    )

    $subKey.SetValue("DisplayName", $AppName)
    $subKey.SetValue("UninstallString", "`"$UninstallExe`"")
    $subKey.SetValue("DisplayIcon", $IconFile)
    $subKey.SetValue("Publisher", "Osdag, FOSSEE")
    $subKey.SetValue("DisplayVersion", $Version)
    $subKey.SetValue("InstallLocation", $InstallDir)
    $subKey.SetValue("HelpLink", "https://osdag.fossee.in/")
    $subKey.SetValue("EstimatedSize", $SizeKB, [Microsoft.Win32.RegistryValueKind]::DWord)
    $subKey.Close()
    $baseKey.Close()

}
else {

    $UninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"

    New-Item -Path $UninstallKey -Force | Out-Null
    Set-ItemProperty -Path $UninstallKey -Name "DisplayName" -Value $AppName
    Set-ItemProperty -Path $UninstallKey -Name "UninstallString" -Value "`"$UninstallExe`""
    Set-ItemProperty -Path $UninstallKey -Name "DisplayIcon" -Value $IconFile
    Set-ItemProperty -Path $UninstallKey -Name "Publisher" -Value "Osdag, FOSSEE"
    Set-ItemProperty -Path $UninstallKey -Name "DisplayVersion" -Value $Version
    Set-ItemProperty -Path $UninstallKey -Name "InstallLocation" -Value $InstallDir
    Set-ItemProperty -Path $UninstallKey -Name "HelpLink" -Value "https://osdag.fossee.in/"
    New-ItemProperty -Path $UninstallKey -Name "EstimatedSize" -Value $SizeKB -PropertyType DWord -Force | Out-Null
}
