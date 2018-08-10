import sys
from subprocess import check_output

print('start')
cmd = "adb shell pm list packages -f | sed -e 's/.*=//' | sort"
packages = check_output(cmd.split(" ")).split('\n')

for package in packages:
    if len(package) == 0:
        continue
    sys.stdout.write("Uninstalling: ")
    sys.stdout.write(package)
    result = check_output(["adb", "uninstall", package]).replace("\n", "")
    sys.stdout.write(" Result: ")
    sys.stdout.write(result)
    sys.stdout.write('\n')

print('end')
