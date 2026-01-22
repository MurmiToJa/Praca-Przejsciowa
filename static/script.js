// Update status every 2 seconds
setInterval(updateStatus, 2000);

// Initial status update
updateStatus();

function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            const activeAttacks = data.active_attacks;
            document.getElementById('active-attacks').textContent = activeAttacks.length;

            // Update attack status indicators
            const attackTypes = ['http_flood', 'scapy_http', 'combined_attack', 'syn_flood'];
            attackTypes.forEach(type => {
                const statusElement = document.getElementById(`status-${type}`);
                if (activeAttacks.includes(type)) {
                    statusElement.classList.add('active');
                } else {
                    statusElement.classList.remove('active');
                }
            });
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

function startAttack(attackType) {
    const targetIp = document.getElementById('target-ip').value;
    const port = document.getElementById('port').value;
    const threads = document.getElementById('threads').value;

    if (!targetIp) {
        addLog('Błąd: Wprowadź docelowy adres IP', 'error');
        return;
    }

    const data = {
        attack_type: attackType,
        target_ip: targetIp,
        port: parseInt(port),
        threads: parseInt(threads)
    };

    fetch('/start_attack', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addLog(`✓ ${data.message}`, 'success');
                updateStatus();
            } else {
                addLog(`✗ Błąd: ${data.message}`, 'error');
            }
        })
        .catch(error => {
            addLog(`✗ Błąd połączenia: ${error}`, 'error');
        });
}

function stopAttack(attackType) {
    const data = {
        attack_type: attackType
    };

    fetch('/stop_attack', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addLog(`✓ ${data.message}`, 'success');
                updateStatus();
            } else {
                addLog(`✗ Błąd: ${data.message}`, 'error');
            }
        })
        .catch(error => {
            addLog(`✗ Błąd połączenia: ${error}`, 'error');
        });
}

function addLog(message, type = 'info') {
    const logContainer = document.getElementById('log-container');
    const timestamp = new Date().toLocaleTimeString('pl-PL');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;

    logContainer.insertBefore(logEntry, logContainer.firstChild);

    // Keep only last 50 log entries
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// Add initial log entry
addLog('System gotowy do pracy', 'success');
