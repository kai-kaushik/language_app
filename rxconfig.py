import reflex as rx

class LanguageappConfig(rx.Config):
    pass

config = LanguageappConfig(
    app_name="language_app",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
