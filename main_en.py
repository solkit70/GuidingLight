import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAIError, Image
from datetime import datetime
import os
from langchain_community.callbacks import get_openai_callback
from openai import OpenAI

# Function to interact with OpenAI API
def generate_text(api_key, birth_date, gender, language):
    try: 
        model_name = 'gpt-4o-mini'
        # Initialize your OpenAI instance using the provided API key
        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name)
        
        # Calculate age and age group
        current_year = datetime.now().year
        birth_year = int(birth_date.split("년")[0])
        age = current_year - birth_year
        age_group = (age // 10) * 10

        # Define age-specific advice
        if age_group == 10:
            age_advice = "🧒 This is the beginning of a journey to find yourself. Don't be afraid and love yourself even in mistakes. You may have many concerns about studying, friends, and dreams."
        elif age_group == 20:
            age_advice = "👩‍🎓 Failure is the nourishment for growth. Take courage and try new challenges. Uncertainty about love, career, and the future is all part of your journey."
        elif age_group in [30, 40]:
            age_advice = "👨‍👩‍👧‍👦 Balancing family and work can be exhausting, and you may forget yourself at times, but you are already doing well. Take a moment to comfort yourself."
        else:  # 50-60s and above
            age_advice = "🧑‍🦳 Now is the time to feel the depth of life. Be proud of the path you've walked. Wonderful times are still waiting to begin."

        # Update instruction to include structured sections
        instruction = f"""
        You are a warm life counselor who gives kind advice. 
        The user born on {birth_date} is currently {age} years old. 
        Please provide warm advice, comfort, and encouragement suitable for their current age.

        Write the answer in the following structure:
        
        1️⃣ **Age and Basic Information**  
        - User's age: {age} years old  
        - Korean Zodiac: Mention the zodiac corresponding to the birth date.  
        - Constellation: Mention the constellation corresponding to the birth date.  
        - Birth flower: Mention the birth flower corresponding to the birth date.  

        2️⃣ **Advice Suitable for Current Age**  
        - Mention concerns, comfort, and possibilities for positive change suitable for people in their {age_group}s.  
        - {age_advice}  

        3️⃣ **Specific Action Plan**  
        - Suggest specific action plans such as health management, self-development, strengthening relationships, and financial planning.  

        4️⃣ **Words of Comfort and Encouragement**  
        - Use emojis to enhance readability. 😊  
        - End with the following comforting words:  
          "Be proud and grateful for the path you've walked so far. Life will continue to be on your side. Today and tomorrow, you are doing well enough." 💖  

        Write the entire response in {language}.
        """
        query = instruction + ". " + birth_date + " born " + gender + " should think or act on what? Please answer in " + language + "."
        # Generate text response
        with get_openai_callback() as cb:
            generated_text = llm.invoke(query)
            st.write(cb)
        return generated_text
    except OpenAIError as e:
        st.warning("Incorrect API key provided or OpenAI API error. You can find your API key at https://platform.openai.com/account/api-keys.")

# Function to generate an image based on the response content
def generate_image(api_key, prompt, age_group, language):
    try:
        # Define popular characters or themes based on age group
        if age_group == 10:
            theme = "a cheerful cartoon character popular among teenagers"
        elif age_group == 20:
            theme = "a nostalgic character from the 2000s"
        elif age_group in [30, 40]:
            theme = "a classic character from the 1980s or 1990s"
        else:  # 50-60s and above
            theme = "a timeless character from the 1960s or 1970s"

        # Adjust theme based on language and associated countries
        if language == "Korean":
            theme += ", such as Pororo or Dooly, in a bright and hopeful setting inspired by South Korea"
        elif language == "Japanese":
            theme += ", such as Doraemon or Astro Boy, in a peaceful and inspiring scene inspired by Japan"
        elif language == "English":
            theme += ", such as Mickey Mouse or Snoopy, in a joyful and uplifting environment inspired by countries like the United States, United Kingdom, Canada, or Australia"
        elif language == "French":
            theme += ", such as Tintin or Asterix, in a charming and adventurous setting inspired by France"
        elif language == "Spanish":
            theme += ", such as Mafalda or Don Quixote, in a warm and optimistic atmosphere inspired by Spain, Mexico, or Argentina"
        elif language == "Chinese":
            theme += ", such as Monkey King (Sun Wukong) or Pleasant Goat, in a vibrant and hopeful landscape inspired by China, Taiwan, or Singapore"
        elif language == "German":
            theme += ", such as Maya the Bee or Pumuckl, in a cheerful and serene environment inspired by Germany or Austria"
        elif language == "Italian":
            theme += ", such as Pinocchio or Geronimo Stilton, in a creative and inspiring scene inspired by Italy"
        elif language == "Portuguese":
            theme += ", such as characters from Brazilian folklore, in a lively and colorful setting inspired by Portugal or Brazil"
        elif language == "Russian":
            theme += ", such as Cheburashka or Winnie-the-Pooh (Russian version), in a cozy and heartwarming setting inspired by Russia"
        elif language == "Arabic":
            theme += ", such as characters from Arabian Nights, in a magical and inspiring scene inspired by Saudi Arabia, Egypt, or the United Arab Emirates"
        elif language == "Hindi":
            theme += ", such as characters from Indian mythology, in a vibrant and culturally rich setting inspired by India"
        elif language == "Dutch":
            theme += ", such as Miffy, in a charming and minimalist scene inspired by the Netherlands"
        elif language == "Swedish":
            theme += ", such as Pippi Longstocking, in a whimsical and adventurous setting inspired by Sweden"
        elif language == "Turkish":
            theme += ", such as Nasreddin Hodja, in a humorous and inspiring scene inspired by Turkey"
        elif language == "Polish":
            theme += ", such as characters from Polish fairy tales, in a magical and heartwarming setting inspired by Poland"
        else:
            theme += ", inspired by popular characters and cultural elements from countries associated with the selected language"

        # Combine the theme with the advice for the image prompt
        full_prompt = f"Create an illustration that visually represents the following advice: {prompt}. Avoid using text in the image. Focus on {theme}."

        # Display the full prompt for debugging
        st.write(f"Debug: Full prompt for image generation: {full_prompt}")

        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except OpenAIError as e:
        st.warning("Error generating image. Please check your API key or try again later.", e)

def main():
    st.title('Guiding Light 🌟')

    # Get user input for OpenAI API key
    api_key = st.text_input("Please input your OpenAI API Key:", type="password")

    # Get the current year
    current_year = datetime.now().year   

    # Set year, month and date
    birth_date = st.date_input("Select your birth date", min_value=datetime(1900, 1, 1), max_value=datetime(current_year, 12, 31), format="MM/DD/YYYY")

    # Extract year, month, day from datetime.date
    year = str(birth_date.year)
    month = str(birth_date.month)
    day = str(birth_date.day)   

    birth_date_str = year + "년 " + month + "월 " + day + "일"    

    # Set gender
    gender = st.radio("Select your gender", ["Male", "Female"])

    # List of languages in which ChatGPT is available
    available_languages = [
        "English", "Korean", "Spanish", "French", "German", "Chinese", "Japanese",
        "Italian", "Portuguese", "Russian", "Arabic", "Hindi", "Dutch", "Swedish", "Turkish", "Polish"
    ]

    # Language selected by user
    selected_language = st.selectbox("Select a language:", available_languages)  

    # Button to trigger text generation
    if st.button("Shine My Day"):
        if api_key:
            with st.spinner('Wait for it...'):    
                # When an API key is provided
                generated_text = generate_text(api_key, birth_date_str, gender, selected_language)
                st.write("Generated counsel:")
                st.write(generated_text.content)

                # Generate an image based on the response
                image_prompt = f"A bright and hopeful illustration inspired by the following advice: {generated_text.content}"
                birth_year = int(birth_date.year)
                age_group = ((current_year - birth_year) // 10) * 10
                image_url = generate_image(api_key, image_prompt, age_group, selected_language)
                if image_url:
                    st.image(image_url, caption="Generated Image")
        else:
            st.warning("Please insert your OpenAI API key.")


if __name__ == "__main__":
    main()