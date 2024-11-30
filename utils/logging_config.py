import logging

def setup_logging():
    logging.basicConfig(
        level=logging.WARNING,  # Set the log level to WARNING
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Log to console
            # You can add FileHandler or other handlers if needed
        ]
    ) 