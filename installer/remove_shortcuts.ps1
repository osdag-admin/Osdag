$AppName = "osdag"

# If user is admin?
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    $StartMenuDir = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\$AppName"
    $DesktopPath = Join-Path $env:Public "Desktop"
    $UninstallKey = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
}else {
    $StartMenuDir = Join-Path $env:AppData "Microsoft\Windows\Start Menu\Programs\$AppName"
    $DesktopPath = [Environment]::GetFolderPath("Desktop")
    $UninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
}

Remove-Item "$StartMenuDir" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$DesktopPath\$AppName.lnk" -Force -ErrorAction SilentlyContinue
Remove-Item $UninstallKey -Recurse -Force -ErrorAction SilentlyContinue
