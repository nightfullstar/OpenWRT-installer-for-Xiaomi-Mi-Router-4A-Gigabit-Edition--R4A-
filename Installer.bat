@echo off
color 1F
echo                                           -Добро пожаловать!
echo                                           \     R3GV2      \
echo                                           /  R4A Gigabyte  /
echo                                           \    Routers     \
echo                                           / By IgorechekXD /
echo ----------------------------------------Меню выбора операций.----------------------------------------
echo        1 -- Запустить Telnet и FTP сервера
echo        2 -- Создать Backup стоковой прошивки
echo        3 -- Установить загрузчик от 3 прошивки
echo        4 -- Установить ОС (OpenWRT, Сток и Т.Д.)
echo        5 -- Установить Backup
echo        6 -- Зайти в Shell роутера (По FTP)
echo -------------------------------------------------------------
set /p f=Введите число которое написано до операции: 
set /a n=%f%
if %n% == 1 (
	echo Скрипт на запуск Telnet и FTP серверов запустился...
	"python/python.exe" scripts/main.py
	pause
) else (
	if %n% == 2 (
	    echo Запуск скрипта для бэкапа прошивки...
		"python/python.exe" scripts/createbackup.py
		pause 
	) else (
		if %n% == 3 (
		echo Запуск скрипта на установку загрузчиков...
			"python/python.exe" scripts/writeuboot3.py
			pause
		) else (
			if %n% == 4 (
			echo Запуск скрипта на установку прошивок...
				"python/python.exe" scripts/writeOS.py
				pause
			) else (
				if %n% == 5 (
				echo Запуск скрипта на восстановление роутера из бэкапа..
				"python/python.exe" scripts/restorebackup.py
				pause
				) else (
				    if %n% == 6 (
					echo Запуск скрипта на вход в Shell роутера по FTP... Пользователь и пароль - root. После всех операций, просто закройте окно.
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