"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config

import reflex as rx
from openai import OpenAI
import os

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

try:
    client = OpenAI(api_key=os.environ["OPENAI_KEY"])
except KeyError:
    print("Warning: OPENAI_KEY environment variable not set")
    client = None

# ----------------------------------------------------------------------------
# OpenAI API Logic
# ----------------------------------------------------------------------------


class State(rx.State):
    """The app state."""

    text: str = ""
    text_opt: str = ""
    response: str = ""
    politeness: list = [
        "Super Casual",
        "Moderate Casual",
        "Workplace Casual",
        "Workplace Polite",
        "Super Polite",
    ]
    polite_level: str = "Workplace Casual"
    prompt: str = ""
    lang_list: list = ["English", "Japanese", "French", "Hindi", "Mandarin Chinese"]
    input_lang: str = "English"
    output_lang: str = "Japanese"
    out_processing: bool = False
    out_done: bool = False

    def translate(self) -> str:
        self.out_done = False
        self.out_processing = True
        yield

        if len(self.text) == 0:
            self.out_processing = False
            yield rx.window_alert("Please input some text to translate.")
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
        if client is None:
            raise Exception("OpenAI client not initialized. Please set OPENAI_KEY environment variable.")
        self._construct_prompt()
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": self.prompt}]
        )
        return response.choices[0].message.content.replace("\n", "<br/>")

    def _construct_prompt(self):
        if self.output_lang == "Japanese":
            self.prompt = f"""You are a helpful Japanese Translator. Please Translate the sentence '{self.text}' \
                            from the {self.input_lang} to {self.polite_level} Japanese and provide \
                            me with the word definitions of all the Japanese words used which are N4 proficiency \
                            level and above. The output should very stricly be in the following format:\
                            'Translated Sentence in {self.polite_level} Japanese: <Translated Sentence in Kanji>\
                            Translated Sentence In Romanji: <Translated sentnece in Romanji'\
                            Give the {self.input_lang} definitions for hard Japanese words used and the output should \
                            very stricly be in the following format:\
                            'The {self.input_lang} definitions for hard Japanese words used:\
                            Japanese Word in Kanji (Written in Romanji): {self.input_lang} Definition.'\
                            {self.text_opt}."""
        
        if self.output_lang in ["Mandarin Chinese", "Hindi"]:
            self.prompt = f"""You are a helpful {self.output_lang} Translator. Please Translate the sentence '{self.text}' \
                            from the {self.input_lang} to {self.polite_level} {self.output_lang} and provide \
                            me with the word definitions of all the hard {self.output_lang} words used. The output should very stricly be in the following format:\
                            'Translated Sentence in {self.polite_level} {self.output_lang}: <Translated Sentence in {self.output_lang}>\
                            Translated Sentence In {self.input_lang} charecters: <Translated sentence written with {self.input_lang} charecters'\
                            Give the {self.input_lang} definitions for hard {self.output_lang} words used and the output should \
                            very stricly be in the following format:\
                            '{self.input_lang} definitions for all the hard {self.output_lang} words used:\
                            {self.output_lang} Word: {self.input_lang} Definition.'\
                            {self.text_opt}."""

        elif self.output_lang == "French" or self.output_lang == "English":
            self.prompt = f"""You are a helpful {self.output_lang} Translator. Please Translate the sentence '{self.text}' \
                            from the {self.input_lang} to {self.polite_level} {self.output_lang} and provide \
                            me with the word definitions of all the hard {self.output_lang} words used. The output should \
                            very strictly be in the following format:\
                            'Translated Sentence in {self.polite_level} {self.output_lang}: <Translated Sentence in \
                            {self.output_lang}>'
                            Give the {self.input_lang} definitions for hard {self.output_lang} words used and the output should \
                            very stricly be in the following format:\
                            '{self.input_lang} definitions for all the hard {self.output_lang} words used:\
                            {self.output_lang} Word: {self.input_lang} Definition.'\
                            {self.text_opt}."""


# ----------------------------------------------------------------------------
# Website Styling, Inputs and Outputs
# ----------------------------------------------------------------------------


def header():
    """Basic instructions to get started."""
    return rx.vstack(
        rx.tablet_and_desktop(
            rx.heading(
                "Language Translator Assistant",
                background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
                background_clip="text",
                font_weight="bold",
                size="2xl",
                padding="0.2em",
                padding_top="20vh",
                text_align="center",
            )
        ),
        rx.mobile_only(
            rx.heading(
                "Language Translator Assistant",
                background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
                background_clip="text",
                font_weight="bold",
                size="xl",
                padding="0.2em",
                padding_top="10vh",
                text_align="center",
            )
        ),
        rx.text(
            "This is more than your average Language Translator!",
            color="#A9A9A9",
            text_align="center",
            width=["90%", "90%", "50em"],
            as_="i",
        ),
    )


def input_text(text="Text to translate", param=State.set_text):
    return rx.input(
        placeholder=text,
        on_blur=param,
        border_color="#eaeaef",
        position="relative",
        width=["90%", "90%", "50em"],
        box_shadow="rgba(169, 169, 169, 0.8) 0 10px 10px -10px",
    )


def select_politeness():
    return rx.select(
        items=[
            "Super Casual",
            "Moderate Casual", 
            "Workplace Casual",
            "Workplace Polite",
            "Super Polite",
        ],
        placeholder="Select level of politeness",
        on_change=State.set_polite_level,
    )


def select_input_lang():
    return rx.select(
        items=["English", "Japanese", "French", "Hindi", "Mandarin Chinese"],
        placeholder="Input",
        on_change=State.set_input_lang,
    )


def select_output_lang():
    return rx.select(
        items=["English", "Japanese", "French", "Hindi", "Mandarin Chinese"],
        placeholder="Output",
        on_change=State.set_output_lang,
    )


def submit_button():
    return rx.button(
        "Translate",
        on_click=State.translate,
        color="white",
        border_radius="1em",
        box_shadow="#A9A9A9 0 15px 30px -10px",
        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
        width="12em",
        _hover={
            "opacity": 0.85,
        },
    )


def kofi_popover():
    return rx.html(
        """<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
            <script>
            kofiWidgetOverlay.draw('kai_3575', {
                'type': 'floating-chat',
                'floating-chat.donateButton.text': 'Support me',
                'floating-chat.donateButton.background-color': '#d9534f',
                'floating-chat.donateButton.text-color': '#fff'
            });
            </script>
        """
    )


def output():
    return rx.box(
        rx.html(State.response),
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        padding="1em",
        width=["90%", "90%", "50em"],
        position="relative",
        box_shadow="rgba(169, 169, 169, 0.8) 0 10px 10px -10px",
    )


def index() -> rx.Component:
    """The main view."""
    return rx.box(
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
                select_politeness(),
            ),
            input_text(),
            input_text(text="Optional instructions.", param=State.set_text_opt),
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
            rx.text(
                "Made with ❤️ by Kai Kaushik",
                color="#A9A9A9",
                font_size="0.8em",
                text_align="center",
                width=["90%", "90%", "50em"],
                as_="i",
            ),
            rx.text("", height="10vh"),
            kofi_popover(),
            rx.button(
                rx.icon(tag="moon"),
                on_click=rx.toggle_color_mode,
                position="fixed",
                right="1em",
                bottom="1em",
            ),
            border_radius="lg",
            spacing="1em",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
        overflow_y="auto",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index, title="Language Translator")
