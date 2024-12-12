(function() {
    const refreshIntervals = {
        "disabled": 0, // Represents the disabled state
        "15s": 15000,
        "1m": 60000,
        "5m": 300000,
        "15m": 900000,
    };

    let refreshIntervalId;

    function triggerAppendAndSend() {
        document.querySelector('button[type="submit"]').click();
    }

    function saveRefreshInterval(intervalKey) {
        localStorage.setItem('refreshInterval', intervalKey);
    }

    function getSavedRefreshInterval() {
        return localStorage.getItem('refreshInterval') || 'disabled'; // Default to disabled
    }

    function setRefreshInterval(intervalKey) {
        if (intervalKey === 'disabled') {
            clearInterval(refreshIntervalId); // Clear existing interval if any
        } else if (refreshIntervals[intervalKey]) {
            if (refreshIntervalId) {
                clearInterval(refreshIntervalId); // Clear existing interval
            }
            refreshIntervalId = setInterval(triggerAppendAndSend, refreshIntervals[intervalKey]);
        }

        document.getElementById('refresh-interval').value = intervalKey; // Set hidden input value
    }

    document.addEventListener('DOMContentLoaded', function() {
        const savedIntervalKey = getSavedRefreshInterval();
        setRefreshInterval(savedIntervalKey);

        const refreshDropdownButton = document.getElementById('refreshDropdownButton');
        const refreshMapping = {
            "disabled": "Disabled Auto Refresh",
            "15s": "15 seconds",
            "1m": "1 minute",
            "5m": "5 minutes",
            "15m": "15 minutes"
        };

        refreshDropdownButton.textContent = refreshMapping[savedIntervalKey];

        document.querySelectorAll('.dropdown-menu a').forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault();
                const intervalKey = Object.keys(refreshMapping).find(key => refreshMapping[key] === this.textContent.trim());
                saveRefreshInterval(intervalKey);
                setRefreshInterval(intervalKey);
                refreshDropdownButton.textContent = refreshMapping[intervalKey];
            });
        });
    });
})();
