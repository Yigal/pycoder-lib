"""Runtime environment utilities for managing directories and logging."""

from pathlib import Path
from datetime import datetime
import logging
import shutil
from typing import Dict, Any, Tuple

def setup_runtime_environment(base_dir: str) -> Tuple[Dict[str, Path], logging.Logger]:
    """Setup runtime environment with directories and logging.
    
    Args:
        base_dir: Base directory for runtime files
        
    Returns:
        Tuple containing:
            - Dict of runtime paths
            - Configured logger instance
    """
    # Create runtime paths
    runtime_base = Path(base_dir)
    runtime_timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    runtime_dir = runtime_base / f"runtime_{runtime_timestamp}"
    
    # Define paths structure
    paths = {
        "base": runtime_base,
        "runtime": runtime_dir,
        "logs": runtime_dir / "logs",
        "output": runtime_dir / "outputs"
    }
    
    # Setup directories
    runtime_base.mkdir(exist_ok=True, parents=True)
    
    if paths["runtime"].exists():
        shutil.rmtree(paths["runtime"])
        
    # Create all required directories
    for path in [paths["runtime"], paths["logs"], paths["output"]]:
        path.mkdir(exist_ok=True, parents=True)
    
    # Configure logging
    log_file = paths["logs"] / "server.log"
    
    # Setup logger with both file and console handlers
    logger = configure_logger("agent_server", log_file)
    
    # Add a test log message to verify logging works
    logger.info(f"Server starting, logging to {log_file.absolute()}")
    
    return paths, logger

def configure_logger(logger_name: str, log_file: Path) -> logging.Logger:
    """Configure a logger with file and console handlers.
    
    Args:
        logger_name: Name of the logger
        log_file: Path to the log file
        
    Returns:
        Configured logger instance
    """
    # Reset root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Setup handlers
    file_handler = logging.FileHandler(str(log_file), mode='w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure logger
    logger = logging.getLogger(logger_name)
    logger.propagate = False  # Prevent duplicate logging
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_runtime_paths(runtime_dir: Path) -> Dict[str, Path]:
    """Get dictionary of runtime paths.
    
    Args:
        runtime_dir: Base runtime directory
        
    Returns:
        Dict mapping path names to Path objects
    """
    return {
        "base": runtime_dir,
        "logs": runtime_dir / "logs",
        "output": runtime_dir / "outputs"
    }

def cleanup_runtime_dir(runtime_dir: Path) -> None:
    """Clean up a runtime directory.
    
    Args:
        runtime_dir: Runtime directory to clean up
    """
    if runtime_dir.exists():
        shutil.rmtree(runtime_dir)
