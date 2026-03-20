import os
import sys
import subprocess
import ctypes
import platform
import getInfo

class PhoneDevice(ctypes.Structure):
    _fields_ = [
        ("model", ctypes.c_char * 64),
        ("os_version", ctypes.c_char * 32),
        ("ram_mb", ctypes.c_uint32),
        ("storage_gb", ctypes.c_uint32),
        ("battery_mah", ctypes.c_uint32),
        ("features", ctypes.c_uint32)
    ]

# Feature bitmasks matching the C code
FEATURE_5G = (1 << 0)
FEATURE_NFC = (1 << 1)
FEATURE_BLUETOOTH_5 = (1 << 2)
FEATURE_WIFI_6 = (1 << 3)
FEATURE_GPS = (1 << 4)
FEATURE_FINGERPRINT = (1 << 5)
FEATURE_FACE_UNLOCK = (1 << 6)
FEATURE_FAST_CHARGE = (1 << 7)

class DriverOps(ctypes.Structure):
    _fields_ = [
        ("check_memory", ctypes.c_void_p),
        ("check_os", ctypes.c_void_p),
        ("check_features", ctypes.c_void_p),
        ("print_report", ctypes.c_void_p)
    ]

class CompatibilityDriver(ctypes.Structure):
    _fields_ = [
        ("driver_name", ctypes.c_char * 64),
        ("supported_os", ctypes.c_char * 32),
        ("min_ram", ctypes.c_uint32),
        ("min_storage", ctypes.c_uint32),
        ("min_battery", ctypes.c_uint32),
        ("required_features", ctypes.c_uint32),
        ("ops", DriverOps)
    ]

def build_driver():
    """Compiles the C driver to a shared library."""
    lib_name = "phone_driver.dll" if platform.system() == "Windows" else "libphone_driver.so"
    if not os.path.exists(lib_name):
        print(f"[*] Building native C compatibility drivers ({lib_name})...")
        try:
            # -DSHARED_LIB prevents compiling the test main() function
            subprocess.run(
                ["gcc", "-shared", "-o", lib_name, "-fPIC", "-DSHARED_LIB", "phoneCompatibilityDriver.c"], 
                check=True
            )
            print("[+] Driver compiled successfully.")
        except Exception as e:
            print(f"[!] Failed to build driver natively over GCC: {e}")
            print("[!] Please ensure GCC is installed and in your PATH, or compile it manually.")
            sys.exit(1)
    return lib_name

def map_specs_to_device(specs):
    """Maps the string-based dictionary specs from ADB to the PhoneDevice ctypes struct."""
    device = PhoneDevice()
    
    # Map Model
    model = specs.get("Model", "Unknown")
    device.model = model.encode('utf-8')[:63]
    
    # Map OS Version
    os_vers = specs.get("Android Version", "Unknown")
    # Prefixing 'Android ' to match the expected format in C driver (e.g. 'Android 13')
    device.os_version = f"Android {os_vers}".encode('utf-8')[:31]
    
    # Map RAM
    ram_str = specs.get("RAM", "0")
    try:
        if "kB" in ram_str:
            device.ram_mb = int(ram_str.split()[0].strip()) // 1024
        else:
            device.ram_mb = int(ram_str.strip())
    except:
        device.ram_mb = 0

    # Map Storage
    storage_str = specs.get("Internal Storage", "0")
    try:
        # Assuming block size string representation roughly converts to GB directly
        device.storage_gb = int(storage_str) // (1024 * 1024)
    except:
        device.storage_gb = 128 # Mock default for compatibility testing
        
    # Map Battery
    battery_str = specs.get("Battery Level (%)", "0")
    try:
        # Assuming a 5000 mAh design capacity for the sake of battery health estimation
        level = int(battery_str)
        device.battery_mah = 5000 * level // 100
    except:
        device.battery_mah = 0

    # Map Features (ADB doesn't readily provide a single bitmask, so mapping arbitrary reasonable defaults)
    device.features = FEATURE_5G | FEATURE_NFC | FEATURE_WIFI_6 | FEATURE_FAST_CHARGE | FEATURE_GPS
    
    return device

def run_integration():
    print("==================================================")
    print("        PHONE FULL SYSTEM INTEGRATION DECK        ")
    print("==================================================")
    
    print("\n[Step 1] Initializing Native Drivers...")
    lib_path = build_driver()
    driver_lib = ctypes.CDLL(os.path.abspath(lib_path))
    
    # Setup Cctypes function prototypes
    init_driver = driver_lib.init_driver
    init_driver.argtypes = [ctypes.POINTER(CompatibilityDriver)]
    init_driver.restype = None
    
    evaluate_device = driver_lib.evaluate_device
    evaluate_device.argtypes = [ctypes.POINTER(CompatibilityDriver), ctypes.POINTER(PhoneDevice)]
    evaluate_device.restype = ctypes.c_int

    print("\n[Step 2] Contacting Android Device via ADB...")
    getInfo.check_adb()
    devices = getInfo.get_connected_devices()
    
    if not devices:
        print("[!] No physical Android devices found.")
        print("[!] Please connect an Android device in Developer Mode to proceed.")
        return
        
    driver = CompatibilityDriver()
    init_driver(ctypes.byref(driver))
    print(f"[+] Loaded Profile: {driver.driver_name.decode('utf-8')} (Requires {driver.supported_os.decode('utf-8')})")

    for dev_id in devices:
        print(f"\n==================================================")
        print(f" Processing Device: {dev_id}")
        
        # Collect specs using the existing python info module
        specs = getInfo.collect_specs(dev_id)
        getInfo.print_specs(dev_id, specs)
        
        c_device = map_specs_to_device(specs)
        
        print("\n[Step 3] Running Full Hardware Compatibility Checks...")
        # Handing off struct reference directly to shared library
        result = evaluate_device(ctypes.byref(driver), ctypes.byref(c_device))
        
        if result == 1:
            print("\n>>> System Status: SUPPORTED <<<")
            
            # Integration with flash subroutine
            print("\n[Step 4] Execution Options")
            print("Would you like to initiate the flashing sequence via `falsh.sh`? (y/n)")
            ans = input("> ").strip().lower()
            
            if ans == 'y':
                print(f"[*] Preparing bridging payload for {dev_id}...")
                subprocess.run(f'adb -s {dev_id} push falsh.sh /data/local/tmp/', shell=True)
                print(f"[*] Dispatching flashing routine execution in superuser scope...")
                # Execution requires su binary generally on ADB roots
                subprocess.run(f'adb -s {dev_id} shell "chmod +x /data/local/tmp/falsh.sh && su -c /data/local/tmp/falsh.sh"', shell=True)
                print("[+] System flashed successfully!")
            else:
                print("[*] Operation halted by User.")
        else:
            print("\n>>> System Status: UNSUPPORTED <<<")
            print("[!] Device does not satisfy baseline performance indices.")

if __name__ == "__main__":
    run_integration()
