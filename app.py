import os
from app import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Start the Flask application on the correct port
    app.run(host='0.0.0.0', port=port)
