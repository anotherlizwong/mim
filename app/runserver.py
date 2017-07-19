import os
from mim.routes import flask_app as application


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    application.run(host='0.0.0.0', port=port, debug=True)
