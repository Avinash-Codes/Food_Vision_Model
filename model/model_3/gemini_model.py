from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(image_path):
    with open(image_path, "rb") as file:
        bytes_data = file.read()

    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": bytes_data
        }
    ]
    return image_parts

if __name__ == "__main__":
    input_prompt = """
    You are an expert in nutritionist where you need to see the food items from the image
    and calculate the total calories, also provide the details of every food item with calorie intake
    in the format below:

    1. Item 1 - no of calories, protein
    2. Item 2 - no of calories, protein
    ----
    ----
    Also mention disease risk from these items.
    Finally, mention whether the food items are healthy or not and suggest some healthy alternatives 
    in the format below:
    1. Item 1 - no of calories, protein
    2. Item 2 - no of calories, protein
    ----
    ----
    """

    image_path = 'test/jalebis.jpg'
    
    try:
        image_data = input_image_setup(image_path)
    except FileNotFoundError:
        print("Error: No file found at the specified path.")
        exit(1)

    response = get_gemini_response(input_prompt, image_data)
    
    print("The Response is:")
    print(response)
