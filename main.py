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
            age_advice = "🧒 이 시기는 자신을 찾는 여행의 시작입니다. 두려워하지 말고 실수 속에서도 당신을 사랑하세요. 공부, 친구, 꿈에 대한 고민이 많을 거예요."
        elif age_group == 20:
            age_advice = "👩‍🎓 실패는 성장의 자양분입니다. 용기를 내어 새로운 도전을 하세요. 사랑, 진로, 미래에 대한 불확실함도 결국 당신을 위한 여정입니다."
        elif age_group in [30, 40]:
            age_advice = "👨‍👩‍👧‍👦 가정과 일 사이에서 때로는 지치고, 스스로를 잊을 수 있지만, 당신은 이미 잘 해내고 있습니다. 잠시 멈춰 스스로를 다독여 주세요."
        else:  # 50-60대 이상
            age_advice = "🧑‍🦳 이제 인생의 깊이를 느낄 때입니다. 지난 길을 자랑스러워 하세요. 아직 시작되지 않은 멋진 시간이 기다리고 있습니다."

        # Update instruction to include structured sections
        instruction = f"""
        당신은 따뜻한 조언을 주는 인생 상담자입니다. 
        {birth_date}에 태어난 {gender}의 사용자는 현재 {age}세입니다. 
        그의 현재 나이에 어울리는 따뜻한 조언, 위로, 격려의 말을 해 주세요.

        답변은 아래와 같은 체계로 작성해 주세요:
        
        1️⃣ **나이와 기본 정보**  
        - 사용자의 나이: {age}세  
        - 한국식 띠: 생년월일에 해당하는 띠를 언급해 주세요.  
        - 별자리: 생년월일에 해당하는 별자리를 언급해 주세요.  
        - 탄생화: 생년월일에 해당하는 탄생화를 언급해 주세요.  

        2️⃣ **현재 나이에 어울리는 조언**  
        - {age_group}대에게 어울리는 고민, 위로, 그리고 긍정적인 변화의 가능성을 언급해 주세요.  
        - {age_advice}  

        3️⃣ **구체적인 행동 계획**  
        - 건강 관리, 자기 계발, 인간관계 강화, 재정 계획 등 구체적인 행동 계획을 제안해 주세요.  

        4️⃣ **위로와 격려의 말**  
        - 답변에 이모티콘(Emoji)을 사용하여 가독성을 높여 주세요. 😊  
        - 마지막엔 아래와 같은 위로의 말로 마무리해 주세요:  
          "지금까지 걸어온 길이 고맙고 자랑스럽습니다. 앞으로도 삶은 계속 당신 편일 거예요. 오늘도, 그리고 내일도, 당신은 충분히 잘하고 있어요." 💖  

        전체 문장은 {language}로 작성해 주세요.
        """
        query = instruction + ". " + birth_date + " 태어난 " + gender + "가 지금 생각하거나 행동해야 할 일은 무엇이 있을까요? 대답은 " + language + "로 해 주세요."
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
        else:  # 50-60대 이상
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
