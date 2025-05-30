sync
echo 3 > /proc/sys/vm/drop_caches
nvram set restore_defaults=1
nvram set btn_restore=1
nvram commit
sync

gpio 1 1
gpio 2 0

mount -o remount,size=100% /tmp

echo -1000 > /proc/$$/oom_score_adj
sync

mtd=`cat /proc/mtd | grep OS1 | cut -d":" -f1` ; dd if=/dev/$mtd of=/tmp/os1.bin
sync

if [ -f "/etc/init.d/sysapihttpd" ] ;then
    /etc/init.d/sysapihttpd stop
fi

wifi down
rmmod mt7603e
rmmod mt76x2e

ifdown wan

for i in /etc/rc.d/K*; do
	echo "$i" | grep -q '[0-9]\{1,100\}reboot-wdt$'
	if [ $? -eq 0 ]; then continue;	fi
	echo "$i" | grep -q '[0-9]\{1,100\}umount$'
	if [ $? -eq 0 ]; then continue; fi
	$i stop
done

sleep 10

IFS=$'\n'
for i in `ps | grep -v "PID"`; do
	pid=${i:0:5}
	pid=${pid// /}
	cmd=${i:26}
	[[ "${cmd}" != "${cmd%bin*}" ]] && kill -9 $pid || {
		[[ "${cmd}" != "${cmd%acsc*}" ]] && kill -9 $pid
		[[ "${cmd}" != "${cmd%bsd*}" ]] && kill -9 $pid
		[[ "${cmd}" != "${cmd%tail*}" ]] && kill -9 $pid
	}
done

sleep 10

for i in `ps | grep -v "PID"`; do
	pid=${i:0:5}
	pid=${pid// /}
	cmd=${i:26}
	[[ "${cmd}" != "${cmd%bin*}" ]] && kill -9 $pid || {
		[[ "${cmd}" != "${cmd%ftpd*}" ]] && kill -9 $pid
		[[ "${cmd}" != "${cmd%btnd*}" ]] && kill -9 $pid
		[[ "${cmd}" != "${cmd%sleep*}" ]] && kill -9 $pid
	}
done

sleep 1
sync

for i in `mount |grep squashfs | cut -d" " -f3`; do umount $i; done
for i in `mount |grep jffs2 | cut -d" " -f3`; do umount $i; done
sleep 1
for i in `mount |grep squashfs | cut -d" " -f3`; do umount $i; done

gpio 1 1
gpio l 8 20 20 1 0 4000; sleep 1; gpio l 10 20 20 1 0 4000

echo "V" > /dev/watchdog
mtd -e OS1 -r write /tmp/sysupgrade.bin OS1

gpio 1 1
gpio 2 0

mtd -e OS1 -r write /tmp/os1.bin OS1

gpio 1 0
