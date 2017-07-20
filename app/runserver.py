import os
from mim.routes import flask_app as application


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host='127.0.0.1', port=port, debug=True)
