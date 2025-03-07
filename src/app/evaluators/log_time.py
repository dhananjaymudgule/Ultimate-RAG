# src/app/evaluators/log_time.py

import time
import pandas as pd
import os
from datetime import datetime
from functools import wraps
from src.app.utils.logger import logger
from src.app.core.config import settings

# Define DataFrame columns
COLUMNS = ["timestamp", "function", "retriever", "generator", "execution_time"]

def log_latency(retriever_name="Unknown", generator_name="Unknown"):
    """
    A decorator to log execution time of functions.

    Args:
        retriever_name (str): Name of the retriever (default: "Unknown").
        generator_name (str): Name of the generator (default: "Unknown").
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()  # More precise timing
            result = func(*args, **kwargs)  # Execute the actual function
            execution_time = time.perf_counter() - start_time

            # Create log entry
            new_entry = pd.DataFrame([{
                "timestamp": datetime.now().isoformat(sep=' ', timespec='seconds'),
                "function": func.__name__,
                "retriever": retriever_name,
                "generator": generator_name,
                "execution_time": round(execution_time, 6)  # Round for readability
            }])

            try:
                # Ensure the directory exists
                settings.LATENCY_CSV.parent.mkdir(parents=True, exist_ok=True)
                # Append to CSV
                new_entry.to_csv(
                    settings.LATENCY_CSV, 
                    mode="a", 
                    header=not settings.LATENCY_CSV.exists(), 
                    index=False
                )
            except Exception as e:
                logger.error(f"Failed to log execution time: {e}")

            return result
        return wrapper
    return decorator
