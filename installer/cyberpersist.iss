[Setup]
AppName=CyberPersist
AppVersion=0.1.0
AppPublisher=Windows Autorun Inspector
AppPublisherURL=https://github.com/mokhtarfertit/Windows-Autorun-Inspector
DefaultDirName={autopf}\CyberPersist
DefaultGroupName=CyberPersist
OutputDir=..\dist-installer
OutputBaseFilename=CyberPersist-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes

[Files]
Source: "..\dist\cyberpersist\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\CyberPersist Help"; Filename: "{cmd}"; Parameters: "/K ""{app}\cyberpersist.exe"" --help"; WorkingDir: "{app}"
Name: "{group}\CyberPersist Scan"; Filename: "{cmd}"; Parameters: "/K ""{app}\cyberpersist.exe"" scan"; WorkingDir: "{app}"
Name: "{commondesktop}\CyberPersist Help"; Filename: "{cmd}"; Parameters: "/K ""{app}\cyberpersist.exe"" --help"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Run]
Filename: "{cmd}"; Parameters: "/K ""{app}\cyberpersist.exe"" --help"; Description: "Open CyberPersist help"; Flags: postinstall skipifsilent