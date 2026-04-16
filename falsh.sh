#!/system/bin/sh

## setup for testing:
unzip -p $Z tools*/busybox > $F/busybox;
unzip -p $Z META-INF/com/google/android/update-binary > $F/update-binary;
##

chmod 755 $F/busybox;
$F/busybox chmod 755 $F/update-binary;
$F/busybox chown root:root $F/busybox $F/update-binary;

TMP=$F/tmp;

$F/busybox umount $TMP 2>/dev/null;
$F/busybox rm -rf $TMP 2>/dev/null;
$F/busybox mkdir -p $TMP;

$F/busybox mount -t tmpfs -o noatime tmpfs $TMP;
$F/busybox mount | $F/busybox grep -q " $TMP " || exit 1;

# update-binary <RECOVERY_API_VERSION> <OUTFD> <ZIPFILE>
AKHOME=$TMP/anykernel $F/busybox ash $F/update-binary 3 1 "$Z";
RC=$?;

$F/busybox umount $TMP;
$F/busybox rm -rf $TMP;
$F/busybox mount -o ro,remount -t auto /;
$F/busybox rm -f $F/update-binary $F/busybox;

# Function to handle script exit with proper return code
exit_with_rc() {
    local exit_code=$RC
    if [ -n "$1" ]; then
        exit_code=$1
    fi
    exit $exit_code
}

# Extend to add needed functions/modules
add_needed() {
    local NEEDED=$1
    local max_attempts=10
    local attempt=0
    
    # If no module specified, return success
    if [ -z "$NEEDED" ]; then
        return 0
    fi
    
    # Loop to process needed modules
    while [ -n "$NEEDED" ] && [ $attempt -lt $max_attempts ]; do
        local needed_file="$F/update-binary-$NEEDED-needed.txt"
        
        # Check if the needed file exists
        if [ -f "$needed_file" ]; then
            # Check if the required function/symbol is already present
            if $F/busybox grep -q "$NEEDED" < "$needed_file" 2>/dev/null; then
                break
            fi
        fi
        
        # Execute the needed module
        $F/busybox $F/update-binary $NEEDED "$1"
        RC=$?
        
        if [ $RC -ne 0 ]; then
            $F/busybox echo "Error executing needed module: $NEEDED"
            return 1
        fi
        
        NEEDED=$((NEEDED + 1))
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -ge $max_attempts ]; then
        $F/busybox echo "Max attempts reached for needed modules"
        return 1
    fi
    
    return 0
}

# Logging function
log_msg() {
    $F/busybox echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1"
}

# Error handling function
handle_error() {
    local error_msg=$1
    local error_code=${2:-1}
    log_msg "ERROR: $error_msg"
    return $error_code
}

# Main execution
main() {
    log_msg "Starting AnyKernel flash process"
    
    # Call add_needed if needed
    if [ $# -gt 0 ]; then
        add_needed "$1" || handle_error "add_needed failed"
    fi
    
    log_msg "Flash process completed with RC=$RC"
    exit_with_rc $RC
}

# Run main if script is executed directly
main "$@"
