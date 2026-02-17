import subprocess
import sys


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
        if "\tdevice" in line:
            devices.append(line.split()[0])

    return devices


def get_property(device_id, prop):
    return run_command(f'adb -s {device_id} shell getprop {prop}')


def get_ram(device_id):
    meminfo = run_command(f'adb -s {device_id} shell cat /proc/meminfo')
    for line in meminfo.split("\n"):
        if "MemTotal" in line:
            return line.split(":")[1].strip()
    return "Unknown"


def get_storage(device_id):
    storage = run_command(
        f'adb -s {device_id} shell df /data | tail -1'
    )
    parts = storage.split()
    if len(parts) >= 2:
        return parts[1]
    return "Unknown"


def get_battery(device_id):
    battery = run_command(
        f'adb -s {device_id} shell dumpsys battery | grep level'
    )
    return battery.replace("level:", "").strip()


def get_screen_info(device_id):
    size = run_command(
        f'adb -s {device_id} shell wm size'
    )
    density = run_command(
        f'adb -s {device_id} shell wm density'
    )
    return size + " | " + density


def get_cpu_info(device_id):
    cpu = run_command(
        f'adb -s {device_id} shell cat /proc/cpuinfo | grep Hardware'
    )
    return cpu if cpu else "Unknown"


def collect_specs(device_id):
    specs = {
        "Model": get_property(device_id, "ro.product.model"),
        "Brand": get_property(device_id, "ro.product.brand"),
        "Manufacturer": get_property(device_id, "ro.product.manufacturer"),
        "Android Version": get_property(device_id, "ro.build.version.release"),
        "SDK Version": get_property(device_id, "ro.build.version.sdk"),
        "Security Patch": get_property(device_id, "ro.build.version.security_patch"),
        "Build ID": get_property(device_id, "ro.build.display.id"),
        "CPU Info": get_cpu_info(device_id),
        "CPU ABI": get_property(device_id, "ro.product.cpu.abi"),
        "RAM": get_ram(device_id),
        "Internal Storage": get_storage(device_id),
        "Battery Level (%)": get_battery(device_id),
        "Screen Info": get_screen_info(device_id),
        "Bootloader": get_property(device_id, "ro.bootloader"),
        "Hardware": get_property(device_id, "ro.hardware")
    }
    return specs


def print_specs(device_id, specs):
    print("\n========================================")
    print(f"Device ID: {device_id}")
    print("========================================")

    for key, value in specs.items():
        print(f"{key:<20}: {value}")

    print("========================================\n")


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
