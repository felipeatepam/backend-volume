import os
import logging
from typing import Union
from fastapi import FastAPI

# 1. Setup Logging to the Persistent Volume path
LOG_DIR = "/tmp/logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure the directory exists (best practice)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),  # Writes to the PVC
        logging.StreamHandler()         # Writes to stdout (kubectl logs)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    """Returns Hello World and logs the access."""
    logger.info("Root endpoint accessed - persistent log entry created.")
    return {"Hello": "World", "log_path": LOG_FILE}

@app.get("/items/{item_id}")
def read_item(item_id: int, item_count: Union[str, None] = None):
    """Returns numbers of items."""
    logger.info(f"Item endpoint accessed for item_id: {item_id}")
    return {"item_id": item_id, "q": item_count}

@app.get("/api/hello")
def check_volume():
    """Debug endpoint to verify if the volume is writable."""
    try:
        test_file = os.path.join(LOG_DIR, "write_test.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return {"status": "writable", "path": LOG_DIR}
    except Exception as e:
        return {"status": "error", "message": str(e)}
