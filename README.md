rtc_ds3234
==========

Userspace driver for RTC DS3234 written in Python. Provides a small command-line tool and matching
systemd files to set the system time from the RTC on boot and periodically save the current system
time to the RTC while the system is running.

Especially useful for Linux based systems like the Rasberry Pi / BeagleBone that don't have a
built-in RTC and therefore lose their system date and time on reboot / power cycle / power loss.
