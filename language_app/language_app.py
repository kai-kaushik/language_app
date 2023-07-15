"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
import openai
import yaml

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

with open('config.yaml', 'r') as file:
    params = yaml.load(file, Loader=yaml.FullLoader)


# Set API key
openai.api_key = params["OPENAI_API_KEY"]

#----------------------------------------------------------------------------
# OpenAI API Logic
#----------------------------------------------------------------------------

class State(rx.State):
    """The app state."""
    text: str = ""
    response: str = ""
    politeness: list = ["Super Casual", "Moderate Casual", "Workplace Casual", "Workplace Polite", "Super Polite"]
    polite_level: str = "Workplace Casual"
    profeciency: list = ["Newbie", "Beginner", "Conversational", "Business", "Native"]
    profeciency_level: str = "Beginner"
    prompt: str = ""

    def translate(self) -> str:
        if not self.text.strip():
            return "Translations will appear here."
        self.response = self.get_openai_response()

    def get_openai_response(self, model="gpt-3.5-turbo") -> str:
        self._construct_prompt()
        response = openai.ChatCompletion.create(
        model=model,
        messages=[
                {"role": "user", "content": self.prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    def _construct_prompt(self):
        self.prompt = f"You are a helpful Japanese Translator. Please Translate the sentence '{self.text}' from the English to {self.polite_level} Japanese and provide \
                        me with the word definitions of all the Japanese words used which are {self.profeciency_level} level and above. The output should \
                        be in the following format:\
                        Translated Sentence in {self.polite_level} Japanese: <Translated Sentence in Kanji>\
                        Translated Sentence In Romanji: <Translated sentnece in Romanji\
                        English definitions for Japanse words used which are {self.profeciency_level} level and above:\
                        <provide prodefinitions seperated by '|' in the format: Japanese Word in Kanji (Written in Romanji): English Definition.>"
        
#----------------------------------------------------------------------------
# Website Styling, Inputs and Outputs
#----------------------------------------------------------------------------

def header():
    """Basic instructions to get started."""
    return rx.vstack(
                rx.heading("Language Translator Assistant",
                    background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
                    background_clip="text",
                    font_weight="bold",
                    size="2xl"),
                rx.text(
                    "This is more than a Japanese-English Language Translator, Select you level of \
                     profeciency and language level and watch the magic happen!",
                    margin_top="0.2 rem",
                    color="#666",
                ),
            )

def output():
    return rx.box(
        rx.text(State.response),
        padding="8 rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )

def input_text():
    return rx.input(
                placeholder="Text to translate",
                on_blur=State.set_text,
                margin_top="1rem",
                border_color="#eaeaef",
                position="relative",
            )

def select_profeciency():
    return rx.select(
                State.profeciency,
                placeholder="Select level of Profeciency",
                on_change=State.set_profeciency_level,
                margin_top="1rem",
            )

def select_politeness():
    return rx.select(
                State.politeness,
                placeholder="Select level of politeness",
                on_change=State.set_polite_level,
                margin_top="1rem",
            )

def index() -> rx.component():
    """The main view."""
    return rx.center(
            rx.vstack(
                    header(),
                    input_text(),
                    rx.hstack(
                        select_profeciency(),
                        select_politeness(),
                        rx.button("Send", on_click=State.translate), 
                    ),
                    output(),
                    width="100%",
                    height="100vh",
                    bg="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%)",
                )
            )
    


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index, title="Translator")
app.compile()
