import logging

from pathlib import Path
from appdirs import user_data_dir

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the path of the local app data folder
USER_DATA_PATH = Path(user_data_dir("divadsn", "EvelstarInvoices"))
