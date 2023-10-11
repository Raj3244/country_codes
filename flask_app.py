from flask import Flask, jsonify, request
import requests

app = Flask(__name)

@app.route('/health', methods=['GET'])
def health():
    return 'Service is healthy'

@app.route('/diag', methods=['GET'])
def diag():
    api_url = 'https://www.travel-advisory.info/api'
    response = requests.get(api_url)

    if response.status_code == 200:
        return jsonify({"api_status": {"code": 200, "status": "ok"}})
    else:
        return jsonify({"api_status": {"code": response.status_code, "status": "error"}})

@app.route('/convert', methods=['GET'])
def convert():
    country_name = request.args.get('country_name')
    if country_name:
        api_url = 'https://www.travel-advisory.info/api'
        response = requests.get(api_url)
        data = response.json()

        country_data = data.get('data', {})
        for code, info in country_data.items():
            if info.get('name', '').lower() == country_name.lower():
                return jsonify({country_name: code})

    return jsonify({"error": "Country code not found"})

if __name__ == '__main__':
    app.run()
