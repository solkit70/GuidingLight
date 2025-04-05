# AI Web Application using LangChain and Streamlit

This project is an AI web application that utilizes OpenAI's GPT-4o mini model to answer user questions. The application is built using Streamlit and LangChain, providing an interactive interface for users to engage with the AI.

## Project Structure

```
ai-web-app
├── src
│   ├── main.py              # Main application for Korean prompts
│   ├── main_en.py           # Main application for English prompts
│   ├── services
│   │   └── gpt_service.py    # Service for interacting with the OpenAI API
│   ├── utils
│   │   └── __init__.py       # Utility functions (currently empty)
│   └── config
│       └── settings.py       # Configuration settings for the application
├── requirements.txt           # Project dependencies
├── .streamlit
│   └── config.toml           # Streamlit configuration settings
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/solkit70/GuidingLight.git
   cd ai-web-app
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   Update the `src/config/settings.py` file with your OpenAI API key and any other necessary configuration settings.

4. **Run the application:**
   - For Korean prompts, execute:
     ```
     streamlit run src/main.py
     ```
   - For English prompts, execute:
     ```
     streamlit run src/main_en.py
     ```

## Usage

Once the application is running, you can enter your questions in the provided input field. The AI will process your query and return a response generated by the GPT-4o mini model.

## Presentation

For more details, refer to the project presentation: [Google Slides](https://docs.google.com/presentation/d/1gKLK7q__58EymakIuHzl_n9qNIBT9rl8yw4qTvv6O7o/edit?usp=sharing)

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.