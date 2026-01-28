from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import sys
import json
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/calculator', methods=['POST'])
def calculate():
    try:
        data = request.json
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not (-90 <= latitude <= 90):
            return jsonify({'error': 'Latitude must be between -90 and 90'}), 400
        if not (-180 <= longitude <= 180):
            return jsonify({'error': 'Longitude must be between -180 and 180'}), 400
        
        # Use the wrapper script
        wrapper_path = r"C:\Users\Abel Philip\Downloads\Lunar Project\Lunar_Horizon_Project\lunar_calc_wrapper.py"
        python_exe = r"C:\Users\Abel Philip\.conda\envs\lunar\python.exe"
        
        result = subprocess.run(
            [python_exe, wrapper_path, str(latitude), str(longitude), start_date, end_date],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse the output
        output_text = result.stdout.strip()
        error_text = result.stderr.strip()
        
        if output_text:
            try:
                data = json.loads(output_text)
                if 'error' in data:
                    return jsonify({'success': False, 'error': data.get('error', 'Unknown error')}), 500
                else:
                    return jsonify(data)
            except json.JSONDecodeError:
                pass
        
        # If script failed
        if result.returncode != 0:
            error_msg = f"Script failed with return code {result.returncode}"
            if error_text:
                error_msg += f"\n{error_text[:300]}"
            return jsonify({'success': False, 'error': error_msg}), 500
        
        return jsonify({'success': False, 'error': 'No output from calculator'}), 500
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Calculation timeout (>2 minutes)'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=False, port=5000, use_reloader=False)
