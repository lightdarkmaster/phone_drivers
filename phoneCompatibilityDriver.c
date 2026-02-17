#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* ===============================
   Hardware Feature Bitmasks - pag defines bitmask values for various hardware features
   =============================== */

#define FEATURE_5G            (1 << 0)
#define FEATURE_NFC           (1 << 1)
#define FEATURE_BLUETOOTH_5   (1 << 2)
#define FEATURE_WIFI_6        (1 << 3)
#define FEATURE_GPS           (1 << 4)
#define FEATURE_FINGERPRINT   (1 << 5)
#define FEATURE_FACE_UNLOCK   (1 << 6)
#define FEATURE_FAST_CHARGE   (1 << 7)

/* ===============================
   Device Profile Structure - pag defines the structure to hold device specifications and features
   =============================== */

typedef struct {
    char model[64];
    char os_version[32];
    uint32_t ram_mb;
    uint32_t storage_gb;
    uint32_t battery_mah;
    uint32_t features;  // Bitmask
} PhoneDevice;

/* ===============================
   Driver Operation Table - pag defines function pointers for driver operations
   =============================== */

typedef struct DriverOps {
    int (*check_memory)(PhoneDevice*);
    int (*check_os)(PhoneDevice*);
    int (*check_features)(PhoneDevice*, uint32_t required_features);
    void (*print_report)(PhoneDevice*);
} DriverOps;

/* ===============================
   Compatibility Driver - pag defines the driver structure that holds metadata and function pointers for operations
   =============================== */

typedef struct {
    char driver_name[64];
    char supported_os[32];
    uint32_t min_ram;
    uint32_t min_storage;
    uint32_t min_battery;
    uint32_t required_features;
    DriverOps ops;
} CompatibilityDriver;

/* ===============================
   Function Implementations
   =============================== */

int check_memory_impl(PhoneDevice *device) {
    if (device->ram_mb < 4096) {
        printf("[ERROR] Insufficient RAM.\n");
        return 0;
    }
    if (device->storage_gb < 64) {
        printf("[ERROR] Insufficient Storage.\n");
        return 0;
    }
    return 1;
}

int check_os_impl(PhoneDevice *device) {
    if (strncmp(device->os_version, "Android 13", 10) != 0) {
        printf("[ERROR] Unsupported OS version.\n");
        return 0;
    }
    return 1;
}

int check_features_impl(PhoneDevice *device, uint32_t required_features) {
    if ((device->features & required_features) != required_features) {
        printf("[ERROR] Missing required hardware features.\n");
        return 0;
    }
    return 1;
}

void print_report_impl(PhoneDevice *device) {
    printf("\n=== Device Report ===\n");
    printf("Model: %s\n", device->model);
    printf("OS: %s\n", device->os_version);
    printf("RAM: %u MB\n", device->ram_mb);
    printf("Storage: %u GB\n", device->storage_gb);
    printf("Battery: %u mAh\n", device->battery_mah);
    printf("Features Bitmask: 0x%X\n", device->features);
}

/* ===============================
   Driver Initialization
   =============================== */

void init_driver(CompatibilityDriver *driver) {
    strcpy(driver->driver_name, "Advanced Phone Compatibility Driver");
    strcpy(driver->supported_os, "Android 13");
    driver->min_ram = 4096;
    driver->min_storage = 64;
    driver->min_battery = 4000;
    driver->required_features =
        FEATURE_5G |
        FEATURE_NFC |
        FEATURE_WIFI_6 |
        FEATURE_FAST_CHARGE;

    driver->ops.check_memory = check_memory_impl;
    driver->ops.check_os = check_os_impl;
    driver->ops.check_features = check_features_impl;
    driver->ops.print_report = print_report_impl;
}

/* ===============================
   Compatibility Evaluation Engine - pag check hit compatibility of a device against the driver requirements
   =============================== */

int evaluate_device(CompatibilityDriver *driver, PhoneDevice *device) {

    printf("\nRunning compatibility check using %s...\n",
           driver->driver_name);

    driver->ops.print_report(device);

    if (!driver->ops.check_os(device))
        return 0;

    if (!driver->ops.check_memory(device))
        return 0;

    if (!driver->ops.check_features(device, driver->required_features))
        return 0;

    if (device->battery_mah < driver->min_battery) {
        printf("[ERROR] Battery capacity too low.\n");
        return 0;
    }

    printf("\n[SUCCESS] Device is fully compatible.\n");
    return 1;
}

/* ===============================
   Simulated Main Entry - pag entry point for testing
   =============================== */

int main() {

    CompatibilityDriver driver;
    init_driver(&driver);

    PhoneDevice device1 = {
        .model = "XPhone Ultra",
        .os_version = "Android 13",
        .ram_mb = 8192,
        .storage_gb = 128,
        .battery_mah = 5000,
        .features = FEATURE_5G |
                    FEATURE_NFC |
                    FEATURE_WIFI_6 |
                    FEATURE_FAST_CHARGE |
                    FEATURE_BLUETOOTH_5 |
                    FEATURE_GPS
    };

    PhoneDevice device2 = {
        .model = "BudgetPhone Lite",
        .os_version = "Android 12",
        .ram_mb = 2048,
        .storage_gb = 32,
        .battery_mah = 3000,
        .features = FEATURE_GPS
    };

    evaluate_device(&driver, &device1);
    evaluate_device(&driver, &device2);

    return 0;
}
