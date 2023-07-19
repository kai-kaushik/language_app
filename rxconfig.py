import reflex as rx

class LanguageappConfig(rx.Config):
    pass

config = LanguageappConfig(
    app_name="language_app",
    api_url="0.0.0.0:8000",
    bun_path="/app/.bun/bin/bun",
    db_url="sqlite:///reflex.db",
)
