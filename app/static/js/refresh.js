(function () {
  const refreshIntervals = {
    "disabled": 0,
    "15s": 15000,
    "1m": 60000,
    "5m": 300000,
    "15m": 900000,
  };
  let refreshIntervalId = null;

  function triggerAppendAndSend() {
    document.querySelector('button[type="submit"]').click();
  }

  function setModel(selectedModel) {
    const modelDropdownButton = document.getElementById('dropdownMenuButton');
    modelDropdownButton.textContent = selectedModel;
    document.getElementById('model').value = selectedModel;
    localStorage.setItem('model', selectedModel);
  }

  function setRefreshInterval(selectedInterval) {
    const refreshDropdownButton = document.getElementById('refreshDropdownButton');
    refreshDropdownButton.textContent = selectedInterval;
    document.getElementById('refresh-interval').value = selectedInterval;

    clearInterval(refreshIntervalId);
    if (refreshIntervals[selectedInterval]) {
      refreshIntervalId = setInterval(triggerAppendAndSend, refreshIntervals[selectedInterval]);
    }

    localStorage.setItem('refreshInterval', selectedInterval);
  }

  function setSystemRole(selectedRole) {
    const roleDropdownButton = document.getElementById('systemRoleDropdownButton');
    roleDropdownButton.textContent = selectedRole;
    document.getElementById('system-role').value = selectedRole;
    localStorage.setItem('systemRole', selectedRole);
  }


  function restoreSettings() {
    const storedModel = localStorage.getItem('model');
    const storedInterval = localStorage.getItem('refreshInterval');
    const storedRole = localStorage.getItem('systemRole');

    if (storedModel) {
      setModel(storedModel);
    }
    if (storedInterval) {
      setRefreshInterval(storedInterval);
    }
    if (storedRole) {
      setSystemRole(storedRole);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    restoreSettings();

    document.getElementById('dropdownMenuButton').addEventListener('change', function (event) {
      setModel(event.target.value);
    });

    document.getElementById('refreshDropdownButton').addEventListener('change', function (event) {
      setRefreshInterval(event.target.value);
    });

    document.getElementById('systemRoleDropdownButton').addEventListener('change', function (event) {
      setSystemRole(event.target.value);
    });
  });

})();