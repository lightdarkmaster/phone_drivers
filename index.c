#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_BUFFER 4096

/* =========================
   Execute Shell Command
   ========================= */
void execute_command(const char *command, char *result) {
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        printf("Failed to run command.\n");
        exit(1);
    }

    while (fgets(result + strlen(result), MAX_BUFFER - strlen(result), fp) != NULL);

    pclose(fp);
}

/* =========================
   Check if Phone Connected
   ========================= */
bool is_device_connected() {
    char buffer[MAX_BUFFER] = {0};

    execute_command("adb devices", buffer);

    return strstr(buffer, "device") && !strstr(buffer, "offline");
}

/* =========================
   Get Device Property
   ========================= */
void get_property(const char *prop_name, const char *label) {
    char command[256];
    char result[MAX_BUFFER] = {0};

    snprintf(command, sizeof(command),
             "adb shell getprop %s", prop_name);

    execute_command(command, result);

    printf("%-20s : %s\n", label, result);
}

/* =========================
   Get Device RAM Info
   ========================= */
void get_ram_info() {
    char command[256];
    char result[MAX_BUFFER] = {0};

    snprintf(command, sizeof(command),
             "adb shell cat /proc/meminfo | grep MemTotal");

    execute_command(command, result);

    printf("%-20s : %s\n", "Total RAM", result);
}

/* =========================
   Get Device Screen Info
   ========================= */
void get_screen_info() {
    char command[256];
    char result[MAX_BUFFER] = {0};

    snprintf(command, sizeof(command),
             "adb shell dumpsys window | grep mScreenDisplayRect");

    execute_command(command, result);

    printf("%-20s : %s\n", "Screen Resolution", result);
}

/* =========================
   Main Program
   ========================= */
int main() {

    printf("Checking for connected Android device...\n");

    if (!is_device_connected()) {
        printf("No Android device detected.\n");
        return 1;
    }

    printf("Device detected successfully!\n\n");
    printf("Fetching phone specifications...\n\n");

    get_property("ro.product.model", "Model");
    get_property("ro.product.brand", "Brand");
    get_property("ro.product.manufacturer", "Manufacturer");
    get_property("ro.build.version.release", "Android Version");
    get_property("ro.build.version.sdk", "SDK Version");
    get_property("ro.hardware", "Hardware");
    get_property("ro.board.platform", "Chipset");
    get_property("ro.bootloader", "Bootloader");
    get_property("ro.product.cpu.abi", "CPU ABI");

    printf("\nGetting RAM info...\n");
    get_ram_info();

    printf("\nGetting screen info...\n");
    get_screen_info();

    printf("\nDone.\n");

    return 0;
}

