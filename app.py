

from flask import Flask, request
from assistant import set_data, set_data_params

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/assistant', methods=['GET'])
        def assistant():
            msg = request.args.get('msg')
            thread_id = request.args.get('thread_id')  
            if (thread_id == 'null'):
                result = set_data(msg)         
                return result, { 'Content-Type': 'application/json; charset=utf-8'} 
            else:
                result = set_data_params(msg, thread_id)                           
                return result, { 'Content-Type': 'application/json; charset=utf-8'}         
                   
    def run(self, host='0.0.0.0', port=10001): 
        self.app.run(debug=True, threaded=True, host=host, port=port)  
        
if __name__ == '__main__':
    app = App()
    app.run(host='0.0.0.0', port=10001)