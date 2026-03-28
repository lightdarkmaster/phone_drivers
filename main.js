document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("compat-form");
    const input = document.getElementById("model");
    const statusMsg = document.getElementById("status-message");
    const checkBtn = document.getElementById("check-btn");

    if (!form) return;

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        
        const deviceModel = input.value.trim();
        if (!deviceModel) return;

        // Reset state
        statusMsg.className = "status-loading";
        statusMsg.innerHTML = '<div class="spinner"></div> Checking database...';
        statusMsg.classList.remove("hidden");
        checkBtn.disabled = true;
        checkBtn.style.opacity = "0.7";

        // Simulate network request (1.5s delay)
        setTimeout(() => {
            checkBtn.disabled = false;
            checkBtn.style.opacity = "1";
            
            // Validation Logic
            const isAppleOrSamsungOrPixel = /iphone|ipad|galaxy|pixel/i.test(deviceModel);
            const isModern = /[0-9]{2}|1[0-9]|2[0-9]/i.test(deviceModel) || deviceModel.toLowerCase().includes('pro');

            if (isAppleOrSamsungOrPixel || isModern || deviceModel.length > 3) {
                statusMsg.className = "status-success";
                statusMsg.innerHTML = `✅ Great news! Standard integration is fully supported for <strong>${deviceModel}</strong>.`;
            } else {
                statusMsg.className = "status-error";
                statusMsg.innerHTML = `❌ <strong>${deviceModel}</strong> is currently not supported. Please check back after the next driver update.`;
            }
            
            // Clear input after a success
            if(statusMsg.classList.contains('status-success')) {
                setTimeout(() => {
                    input.value = '';
                }, 2000);
            }
            
        }, 1500);
    });
});