# logging → built-in module for system logging
import logging


def setup_logger() -> None:
    # Configure global logging settings
    logging.basicConfig(
        level=logging.INFO,  # Log level (INFO and above)
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",  # Structured format
    )