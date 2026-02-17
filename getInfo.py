import subprocess
import sys
import json


def run_command(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running command: {e}")
        sys.exit(1)


def check_adb():
    result = run_command("adb version")
    if "Android Debug Bridge" not in result:
        print("ADB not installed or not in PATH.")
        sys.exit(1)


def get_connected_devices():
    output = run_command("adb devices")
    lines = output.split("\n")[1:]
    devices = []

    for line in lines:
        if "device" in line and not "offline" in line:
            devices.append(line.split()[0])

    return devices


def get_property(device_id, prop):
    return run_command(f"adb -s {device_id} shell getprop {prop}")


def get_ram(device_id):
    meminfo = run_command(f"adb -s {device_id} shell cat /proc/meminfo")
    for line in meminfo.split("\n"):
        if "MemTotal" in line:
            return line.split(":")[1].strip()
    return "Unknown"


def collect_specs(device_id):
    specs = {
        "Model": get_property(device_id, "ro.product.model"),
        "Brand": get_property(device_id, "ro.product.brand"),
        "Manufacturer": get_property(device_id, "ro.product.manufacturer"),
        "Android Version": get_property(device_id, "ro.build.version.release"),
        "SDK Version": get_property(device_id, "ro.build.version.sdk"),
        "Hardware": get_property(device_id, "ro.hardware"),
        "Chipset": get_property(device_id, "ro.board.platform"),
        "CPU ABI": get_property(device_id, "ro.product.cpu.abi"),
        "Bootloader": get_property(device_id, "ro.bootloader"),
        "RAM": get_ram(device_id)
    }
    return specs


def print_specs(device_id, specs):
    print("\n==============================")
    print(f"Device ID: {device_id}")
    print("==============================")

    for key, value in specs.items():
        print(f"{key:<18}: {value}")

    print("==============================\n")


def main():
    print("Checking ADB...")
    check_adb()

    print("Scanning for connected devices...\n")
    devices = get_connected_devices()

    if not devices:
        print("No Android device detected.")
        return

    for device in devices:
        specs = collect_specs(device)
        print_specs(device, specs)


if __name__ == "__main__":
    main()