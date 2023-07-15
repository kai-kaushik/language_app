"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
import openai
import yaml

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

with open("config.yaml", "r") as file:
    params = yaml.load(file, Loader=yaml.FullLoader)


# Set API key
openai.api_key = params["OPENAI_API_KEY"]

# ----------------------------------------------------------------------------
# OpenAI API Logic
# ----------------------------------------------------------------------------


class State(rx.State):
    """The app state."""

    text: str = ""
    response: str = ""
    politeness: list = [
        "Super Casual",
        "Moderate Casual",
        "Workplace Casual",
        "Workplace Polite",
        "Super Polite",
    ]
    polite_level: str = "Workplace Casual"
    profeciency: list = ["Newbie", "Beginner", "Conversational", "Business", "Native"]
    profeciency_level: str = "Beginner"
    prompt: str = ""
    lang_list: list = ["English", "Japanese"]
    input_lang: str = "English"
    output_lang: str = "Japanese"
    out_processing: bool = False
    out_done: bool = False

    def translate(self) -> str:
        self.out_done = False
        self.out_processing = True
        yield

        if len(self.text) == 0:
            self.response = "Please provide a sentence to translate!"
        else:
            try:
                self.response = self.get_openai_response()
                self.out_done = True
                self.out_processing = False
                yield
            except:
                self.out_processing = False
                yield rx.window_alert("Error with OpenAI Execution.")

    def get_openai_response(self, model="gpt-3.5-turbo") -> str:
        self._construct_prompt()
        response = openai.ChatCompletion.create(
            model=model, messages=[{"role": "user", "content": self.prompt}]
        )
        return response["choices"][0]["message"]["content"]

    def _construct_prompt(self):
        if self.output_lang == "Japanese":
            self.prompt = f"You are a helpful Japanese Translator. Please Translate the sentence '{self.text}' from the {self.input_lang} to {self.polite_level} Japanese and provide \
                            me with the word definitions of all the Japanese words used which are {self.profeciency_level} level and above. The output should \
                            be in the following format:\
                            Translated Sentence in {self.polite_level} Japanese: <Translated Sentence in Kanji>\
                            Translated Sentence In Romanji: <Translated sentnece in Romanji\
                            {self.input_lang} definitions for Japanse words used which are {self.profeciency_level} level and above:\
                            <provide prodefinitions seperated by '|' in the format: Japanese Word in Kanji (Written in Romanji): {self.input_lang} Definition.>"

        elif self.output_lang == "English":
            self.prompt = f"You are a helpful English Translator. Please Translate the sentence '{self.text}' from the {self.input_lang} to {self.polite_level} English and provide \
                            me with the word definitions of all the English words used which are {self.profeciency_level} level and above. The output should \
                            be in the following format:\
                            Translated Sentence in {self.polite_level} English: <Translated Sentence in English>\
                            {self.input_lang} definitions for English words used which are {self.profeciency_level} level and above:\
                            <provide prodefinitions seperated by '|' in the format: English Word: {self.input_lang} Definition.>"


# ----------------------------------------------------------------------------
# Website Styling, Inputs and Outputs
# ----------------------------------------------------------------------------


def header():
    """Basic instructions to get started."""
    return rx.vstack(
        rx.heading(
            "Language Translator Assistant",
            background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
            background_clip="text",
            font_weight="bold",
            size="2xl",
            padding="0.2em",
        ),
        rx.text(
            "This is more than a Japanese-English Language Translator, Select you level of \
                     profeciency and language level and watch the magic happen!",
            color="White",
        ),
    )


def input_text():
    return rx.input(
        placeholder="Text to translate",
        on_blur=State.set_text,
        border_color="#eaeaef",
        position="relative",
    )


def select_profeciency():
    return rx.select(
        State.profeciency,
        placeholder="Select " + State.output_lang + " Profeciency",
        on_change=State.set_profeciency_level,
    )


def select_politeness():
    return rx.select(
        State.politeness,
        placeholder="Select level of politeness",
        on_change=State.set_polite_level,
    )


def select_input_lang():
    return rx.select(
        State.lang_list,
        placeholder="English",
        on_change=State.set_input_lang,
    )


def select_output_lang():
    return rx.select(
        State.lang_list,
        placeholder="Japanese",
        on_change=State.set_output_lang,
    )


def submit_button():
    return rx.button(
        "Translate",
        on_click=State.translate,
        border_radius="1em",
        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
        width="20%",
        _hover={
            "opacity": 0.85,
        },
    )


def kofi_popover():
    return rx.popover(
        rx.popover_trigger(
            rx.button(
                "Support Me",
                border_radius="8em",
                box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                width="20%",
                _hover={
                    "opacity": 0.85,
                },
            )
        ),
        rx.popover_content(
            rx.html(
                "<iframe id='kofiframe' src='https://ko-fi.com/kai_3575/?hidefeed=true&widget=true&embed=true&preview=true' \
                            style='border:none;width:100%;padding:4px;background:#f9f9f9;' height='712' title='kai_3575'></iframe>"
            ),
            rx.popover_close_button(),
        ),
    )


def output():
    return rx.box(
        rx.text(State.response),
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


def index() -> rx.component():
    """The main view."""
    return rx.center(
        rx.vstack(
            header(),
            rx.vstack(
                rx.hstack(
                    select_input_lang(),
                    rx.image(
                        src="arrow.svg",
                        height="3em",
                        width="3em",
                    ),
                    select_output_lang(),
                ),
                rx.hstack(
                    select_profeciency(),
                    select_politeness(),
                ),
            ),
            input_text(),
            submit_button(),
            rx.cond(
                State.out_processing,
                rx.vstack(
                    rx.progress(is_indeterminate=True, width="100%"),
                    rx.progress(is_indeterminate=True, width="100%"),
                    rx.progress(is_indeterminate=True, width="100%"),
                    spacing="1em",
                    min_width=["10em", "20em"],
                ),
                rx.cond(
                    State.out_done,
                    output(),
                ),
            ),
            kofi_popover(),
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,
            ),
            border_radius="lg",
            spacing="1em",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index, title="Translator")
app.compile()
