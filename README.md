# K380-auto-conf
This python program watches Logicool K380 keyboard connection, and every time its reonnection is detected, automatically normalize the function key configuration.

This program **requires another core program**: https://github.com/jergusg/k380-function-keys-conf, and extends its function so that you no longer need to manually execute a shell script every time you reconnect K380.
## Depends on
You need to install following commands.
* bluez
* bluez-tools
## Usage
Download and build https://github.com/jergusg/k380-function-keys-conf.
Then put this python code (`K380-fn-keys-auto-conf.py`) in the same directory as `fn_on.sh`.
This program **requires root privileges**.
I recommend registering this program to auto start-up with root privileges.
