import os
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "OpenAI")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.1"))