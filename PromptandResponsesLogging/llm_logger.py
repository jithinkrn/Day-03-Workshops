import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class LLMLogger:
    """
    Enhanced logger for LLM prompts and responses with thread safety and flexible output options.
    """
    
    def __init__(self, log_file: str = "llm_logs.json", log_dir: str = "logs"):
        """
        Initialize the LLM logger.
        
        Args:
            log_file: Name of the log file
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / log_file
        self._lock = threading.Lock()
    
    def log_interaction(
        self,
        prompt: str,
        response: str,
        model: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        tokens_used: Optional[int] = None,
        latency_ms: Optional[float] = None,
        **additional_metadata
    ) -> None:
        """
        Log an LLM interaction with comprehensive metadata.
        
        Args:
            prompt: The input prompt sent to the LLM
            response: The response received from the LLM
            model: Model name/identifier
            user_id: User identifier
            session_id: Session identifier
            tokens_used: Number of tokens consumed
            latency_ms: Response latency in milliseconds
            **additional_metadata: Any additional metadata to log
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "response": response,
            "model": model,
            "user_id": user_id,
            "session_id": session_id,
            "tokens_used": tokens_used,
            "latency_ms": latency_ms,
            **additional_metadata
        }
        
        # Remove None values to keep logs clean
        log_entry = {k: v for k, v in log_entry.items() if v is not None}
        
        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    def log_error(
        self,
        error_message: str,
        prompt: Optional[str] = None,
        error_type: Optional[str] = None,
        **additional_metadata
    ) -> None:
        """
        Log an error that occurred during LLM interaction.
        
        Args:
            error_message: Description of the error
            prompt: The prompt that caused the error (if available)
            error_type: Type/category of the error
            **additional_metadata: Any additional metadata to log
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "error",
            "error_message": error_message,
            "prompt": prompt,
            "error_type": error_type,
            **additional_metadata
        }
        
        # Remove None values
        log_entry = {k: v for k, v in log_entry.items() if v is not None}
        
        with self._lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


# Legacy function for backward compatibility
def log_to_file(prompt: str, response: str, metadata: Dict[str, Any] = None) -> None:
    """
    Simple logging function for backward compatibility.
    
    Args:
        prompt: The input prompt
        response: The LLM response
        metadata: Additional metadata dictionary
    """
    if metadata is None:
        metadata = {}
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": response,
        **metadata
    }
    
    with open("logs/llm_logs.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


# Global logger instance for convenience
default_logger = LLMLogger()


def log_llm_interaction(
    prompt: str,
    response: str,
    **kwargs
) -> None:
    """
    Convenience function to log using the default logger instance.
    """
    default_logger.log_interaction(prompt, response, **kwargs)


def log_llm_error(
    error_message: str,
    **kwargs
) -> None:
    """
    Convenience function to log errors using the default logger instance.
    """
    default_logger.log_error(error_message, **kwargs)


# Context manager for timing LLM calls
class LLMTimer:
    """Context manager to automatically time and log LLM interactions."""
    
    def __init__(self, prompt: str, logger: LLMLogger = None, **metadata):
        self.prompt = prompt
        self.logger = logger or default_logger
        self.metadata = metadata
        self.start_time = None
        self.response = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.utcnow()
        latency_ms = (end_time - self.start_time).total_seconds() * 1000
        
        if exc_type is not None:
            # An exception occurred
            self.logger.log_error(
                error_message=str(exc_val),
                prompt=self.prompt,
                error_type=exc_type.__name__,
                latency_ms=latency_ms,
                **self.metadata
            )
        elif self.response is not None:
            # Successful interaction
            self.logger.log_interaction(
                prompt=self.prompt,
                response=self.response,
                latency_ms=latency_ms,
                **self.metadata
            )
    
    def set_response(self, response: str):
        """Set the response received from the LLM."""
        self.response = response


if __name__ == "__main__":
    # Example usage
    logger = LLMLogger()
    
    # Basic logging
    logger.log_interaction(
        prompt="What is the capital of France?",
        response="The capital of France is Paris.",
        model="gpt-3.5-turbo",
        user_id="user123",
        session_id="session456",
        tokens_used=25,
        latency_ms=150.5
    )
    
    # Using context manager for timing
    with LLMTimer("Explain quantum computing", model="gpt-4") as timer:
        # Simulate LLM call
        import time
        time.sleep(0.1)  # Simulate API call
        response = "Quantum computing is a type of computation that uses quantum bits..."
        timer.set_response(response)
    
    print("Logging examples completed. Check logs/llm_logs.json")