from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os
import signal

app = Flask(__name__)

# Dictionary to store running processes
running_processes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_attack', methods=['POST'])
def start_attack():
    data = request.json
    attack_type = data.get('attack_type')
    target_ip = data.get('target_ip')
    port = data.get('port', 80)
    threads = data.get('threads', 10)
    
    if not target_ip:
        return jsonify({'status': 'error', 'message': 'Target IP is required'}), 400
    
    # Map attack types to script files
    attack_scripts = {
        'http_flood': 'attacks/http_flood.py',
        'scapy_http': 'attacks/scapy_http.py',
        'combined_attack': 'attacks/combined_attack.py',
        'syn_flood': 'attacks/syn_flood.py'
    }
    
    if attack_type not in attack_scripts:
        return jsonify({'status': 'error', 'message': 'Invalid attack type'}), 400
    
    script_path = attack_scripts[attack_type]
    
    # Stop any running attack of this type
    if attack_type in running_processes and running_processes[attack_type]:
        try:
            running_processes[attack_type].terminate()
        except:
            pass
    
    # Start the attack in a subprocess
    try:
        env = os.environ.copy()
        env['TARGET_IP'] = target_ip
        env['PORT'] = str(port)
        env['THREADS'] = str(threads)
        
        process = subprocess.Popen(
            ['python', script_path],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        running_processes[attack_type] = process
        
        return jsonify({
            'status': 'success',
            'message': f'Attack {attack_type} started on {target_ip}:{port}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stop_attack', methods=['POST'])
def stop_attack():
    data = request.json
    attack_type = data.get('attack_type')
    
    if attack_type not in running_processes:
        return jsonify({'status': 'error', 'message': 'No such attack running'}), 400
    
    try:
        process = running_processes[attack_type]
        if process:
            process.terminate()
            process.wait(timeout=5)
            running_processes[attack_type] = None
            return jsonify({'status': 'success', 'message': f'Attack {attack_type} stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    active_attacks = []
    for attack_type, process in running_processes.items():
        if process and process.poll() is None:
            active_attacks.append(attack_type)
    
    return jsonify({
        'active_attacks': active_attacks
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
