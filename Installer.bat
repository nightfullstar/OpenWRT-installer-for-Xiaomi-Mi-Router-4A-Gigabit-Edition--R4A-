@echo off
color 1F
echo                                           -���� ����������!
echo                                           \     R3GV2      \
echo                                           /  R4A Gigabyte  /
echo                                           \    Routers     \
echo                                           / By IgorechekXD /
echo ----------------------------------------���� �롮� ����権.----------------------------------------
echo        1 -- �������� Telnet � FTP �ࢥ�
echo        2 -- ������� Backup �⮪���� ��訢��
echo        3 -- ��⠭����� �����稪 �� 3 ��訢��
echo        4 -- ��⠭����� �� (OpenWRT, �⮪ � �.�.)
echo        5 -- ��⠭����� Backup
echo        6 -- ���� � Shell ���� (�� FTP)
echo -------------------------------------------------------------
set /p f=������ �᫮ ���஥ ����ᠭ� �� ����樨: 
set /a n=%f%
if %n% == 1 (
	echo ��ਯ� �� ����� Telnet � FTP �ࢥ஢ �����⨫��...
	"python/python.exe" scripts/main.py
	pause
) else (
	if %n% == 2 (
	    echo ����� �ਯ� ��� ���� ��訢��...
		"python/python.exe" scripts/createbackup.py
		pause 
	) else (
		if %n% == 3 (
		echo ����� �ਯ� �� ��⠭���� �����稪��...
			"python/python.exe" scripts/writeuboot3.py
			pause
		) else (
			if %n% == 4 (
			echo ����� �ਯ� �� ��⠭���� ��訢��...
				"python/python.exe" scripts/writeOS.py
				pause
			) else (
				if %n% == 5 (
				echo ����� �ਯ� �� ����⠭������� ���� �� ����..
				"python/python.exe" scripts/restorebackup.py
				pause
				) else (
				    if %n% == 6 (
					echo ����� �ਯ� �� �室 � Shell ���� �� FTP... ���짮��⥫� � ��஫� - root. ��᫥ ��� ����権, ���� ���ன� ����.
				    ftp 192.168.31.1
				    pause
					)
				)
			)
		)	
	)
)
cls
Installer.bat