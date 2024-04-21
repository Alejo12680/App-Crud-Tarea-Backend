from flask import Flask
from routes.appRoutes import routes_auth
from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(routes_auth)



if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
    load_dotenv()
