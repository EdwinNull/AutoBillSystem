
; 汽车维修管理系统安装脚本
; 使用Inno Setup编译

[Setup]
AppName=汽车维修管理系统
AppVersion=1.0
DefaultDirName={pf}\汽车维修管理系统
DefaultGroupName=汽车维修管理系统
OutputDir=installer
OutputBaseFilename=汽车维修管理系统_安装包
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\汽车维修管理系统.exe"; DestDir: "{app}"
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\汽车维修管理系统"; Filename: "{app}\汽车维修管理系统.exe"
Name: "{commondesktop}\汽车维修管理系统"; Filename: "{app}\汽车维修管理系统.exe"

[Run]
Filename: "{app}\汽车维修管理系统.exe"; Description: "启动汽车维修管理系统"; Flags: nowait postinstall skipifsilent
