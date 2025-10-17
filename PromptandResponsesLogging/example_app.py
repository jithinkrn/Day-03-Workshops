"""
Example LLM Application with ELK Stack Logging
This demonstrates how to integrate LLM logging with the ELK stack.
"""

import time
import random
import uuid
from datetime import datetime
from llm_logger import LLMLogger, LLMTimer, log_llm_interaction


class MockLLM:
    """Mock LLM for demonstration purposes."""
    
    def __init__(self, model_name: str = "mock-gpt-3.5"):
        self.model_name = model_name
    
    def generate(self, prompt: str) -> tuple:
        """
        Generate a mock response with simulated latency and token usage.
        
        Returns:
            tuple: (response, tokens_used)
        """
        # Simulate API latency
        time.sleep(random.uniform(0.1, 0.5))
        
        # Mock responses based on prompt keywords
        if "capital" in prompt.lower():
            response = f"The capital mentioned in your question relates to geographic or political centers."
        elif "weather" in prompt.lower():
            response = f"Weather patterns vary by location and season. Current conditions depend on your specific area."
        elif "code" in prompt.lower() or "programming" in prompt.lower():
            response = f"Here's a programming example:\n```python\nprint('Hello, World!')\n```"
        else:
            response = f"Thank you for your question: '{prompt[:50]}...'. Here's a thoughtful response based on the topic."
        
        # Simulate token usage
        tokens_used = len(prompt.split()) + len(response.split()) + random.randint(5, 15)
        
        return response, tokens_used


class LLMApplication:
    """Example application that uses LLM with comprehensive logging."""
    
    def __init__(self):
        self.llm = MockLLM()
        self.logger = LLMLogger()
        self.session_id = str(uuid.uuid4())
    
    def chat(self, prompt: str, user_id: str = "demo_user") -> str:
        """
        Process a chat message with full logging.
        
        Args:
            prompt: User's input prompt
            user_id: User identifier
            
        Returns:
            str: LLM response
        """
        start_time = datetime.utcnow()
        
        try:
            # Generate response using LLM
            response, tokens_used = self.llm.generate(prompt)
            
            # Calculate latency
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            # Log the successful interaction
            self.logger.log_interaction(
                prompt=prompt,
                response=response,
                model=self.llm.model_name,
                user_id=user_id,
                session_id=self.session_id,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
                success=True,
                prompt_category=self._categorize_prompt(prompt)
            )
            
            return response
            
        except Exception as e:
            # Log any errors that occur
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            self.logger.log_error(
                error_message=str(e),
                prompt=prompt,
                error_type=type(e).__name__,
                user_id=user_id,
                session_id=self.session_id,
                latency_ms=latency_ms
            )
            
            raise
    
    def _categorize_prompt(self, prompt: str) -> str:
        """Categorize the prompt for analytics."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["code", "programming", "python", "javascript"]):
            return "coding"
        elif any(word in prompt_lower for word in ["weather", "temperature", "forecast"]):
            return "weather"
        elif any(word in prompt_lower for word in ["capital", "country", "geography"]):
            return "geography"
        elif "?" in prompt:
            return "question"
        else:
            return "general"


def simulate_user_interactions():
    """Simulate various user interactions to generate sample data."""
    
    app = LLMApplication()
    
    # Sample prompts for different categories
    sample_prompts = [
        "What is the capital of Japan?",
        "How's the weather today?",
        "Write a Python function to sort a list",
        "Explain quantum computing",
        "What are the benefits of renewable energy?",
        "Show me a JavaScript example",
        "What is the capital of Brazil?",
        "Tell me about machine learning",
        "How do I debug Python code?",
        "What's the current temperature?",
    ]
    
    users = ["user1", "user2", "user3", "demo_user"]
    
    print("🚀 Starting LLM interaction simulation...")
    print("📝 Generating sample data for ELK Stack...")
    
    for i, prompt in enumerate(sample_prompts):
        user = random.choice(users)
        
        print(f"\n[{i+1}/{len(sample_prompts)}] User: {user}")
        print(f"Prompt: {prompt}")
        
        try:
            response = app.chat(prompt, user_id=user)
            print(f"Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Add some delay between requests
        time.sleep(random.uniform(0.5, 2.0))
    
    print("\n✅ Simulation completed!")
    print("📊 Check logs/llm_logs.json for generated data")
    print("🔍 Start ELK stack with: docker-compose up -d")


def demonstrate_context_manager():
    """Demonstrate using the LLMTimer context manager."""
    
    print("\n🔄 Demonstrating LLMTimer context manager...")
    
    # Using context manager for automatic timing
    with LLMTimer("Explain the concept of AI", model="gpt-4", user_id="demo_user") as timer:
        # Simulate LLM processing
        time.sleep(0.3)
        response = "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines..."
        timer.set_response(response)
    
    print("✅ Context manager demo completed")


def demonstrate_convenience_functions():
    """Demonstrate convenience logging functions."""
    
    print("\n📋 Demonstrating convenience functions...")
    
    # Using convenience function
    log_llm_interaction(
        prompt="What is the meaning of life?",
        response="The meaning of life is a philosophical question that has been pondered for centuries...",
        model="gpt-3.5-turbo",
        user_id="philosopher",
        tokens_used=42,
        latency_ms=200.5,
        category="philosophy"
    )
    
    print("✅ Convenience function demo completed")


if __name__ == "__main__":
    print("🎯 LLM Application with ELK Stack Logging Demo")
    print("=" * 50)
    
    # Run demonstrations
    simulate_user_interactions()
    demonstrate_context_manager()
    demonstrate_convenience_functions()
    
    print("\n🎉 All demonstrations completed!")
    print("\n📋 Next steps:")
    print("1. Start ELK stack: docker-compose up -d")
    print("2. Wait for services to start (2-3 minutes)")
    print("3. Open Kibana: http://localhost:5601")
    print("4. Create index pattern: llm-logs-*")
    print("5. Explore your data in Discover and create dashboards!")