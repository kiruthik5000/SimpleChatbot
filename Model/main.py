import os
import random
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from ChatBot import ChatBot  # Assuming your ChatBot class is in ChatBot.py

# A dictionary to hold our chatbot instance
# We will initialize this once when the application starts
chatbot_instance = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that runs on application startup and shutdown.
    This is the ideal place to load our ML model and other resources.
    """
    print("Application startup: Loading chatbot model...")
    try:
        # Load the data and build the model on startup
        bot = ChatBot()
        bot.laod_data('./intents.json') # Correcting the path to intents.json
        
        # Check if the model exists, if not, build it.
        # This prevents training on every startup if the model is already saved.
        if not os.path.exists('ChatBot.pkl'):
            bot.build(test_size=0.2)
        
        # Load the pre-trained model. We do this here instead of in the predict method.
        bot.load_model('ChatBot.pkl')
        
        chatbot_instance['bot'] = bot
        print("Chatbot model loaded successfully!")
    except Exception as e:
        print(f"Error during startup: {e}")
        # It's better to let the application crash if the model can't be loaded
        # as it's not functional without it.
        raise RuntimeError("Failed to load ChatBot model during startup.")
    
    yield # The application will serve requests here
    
    # Code after the `yield` runs on application shutdown
    chatbot_instance.clear()
    print("Application shutdown: Chatbot instance cleared.")

app = FastAPI(lifespan=lifespan)

class UserInput(BaseModel):
    user_message: str

@app.post("/get_response")
def get_response(user_input: UserInput):
    """
    Receives user input and returns a chatbot response.
    This function now only uses the pre-loaded model.
    """
    try:
        bot = chatbot_instance.get('bot')
        if not bot:
            return {"error": "Chatbot model not loaded. Please check server logs."}
            
        response = bot.predict(user_input.user_message)
        
        return {"response": response}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
