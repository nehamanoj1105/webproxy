from flask import Flask, request, Response, send_file
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return send_file('static/webproxy.html')

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    logger.info(f"Proxy request received for URL: {url}")
    
    if not url:
        return "No URL provided", 400
        
    try:
        logger.info(f"Fetching content from: {url}")
        response = requests.get(url, verify=False)
        logger.info(f"Response received with status code: {response.status_code}")
        
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'text/html'),
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=True, host='0.0.0.0', port=5000)