[Setup]
AppName=KonectTrafficStudio
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\KonectTrafficStudio
DefaultGroupName=KonectTrafficStudio
OutputBaseFilename=KonectTrafficStudio_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
UsePreviousAppDir=no
DisableDirPage=no

[Files]
; Main executable files
Source: "dist\KonectTrafficStudio\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Copy assets to root
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Ensure correct folder structure
Source: "assets\icons\*"; DestDir: "{app}\assets\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\icons\black\*"; DestDir: "{app}\assets\icons\black"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\icons\cyan\*"; DestDir: "{app}\assets\icons\cyan"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\KonectTrafficStudio"; Filename: "{app}\KonectTrafficStudio.exe"
Name: "{autodesktop}\KonectTrafficStudio"; Filename: "{app}\KonectTrafficStudio.exe"

[Run]
Filename: "{app}\KonectTrafficStudio.exe"; Description: "Launch KonectTrafficStudio"; Flags: postinstall nowait shellexec runascurrentuser

[UninstallDelete]
Type: filesandordirs; Name: "{app}"