class GPTService:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    def get_response(self, prompt: str) -> str:
        import openai

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']