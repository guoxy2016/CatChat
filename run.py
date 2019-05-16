import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from catchat import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app=app, host='0.0.0.0', port=8000)
    # app.run()
