import reflex as rx
import os

class LanguageappConfig(rx.Config):
    pass

# Get the value of the PORT environment variable, or use 8000 if it's not set
# port = os.environ.get('PORT', '3000')

config = LanguageappConfig(
    app_name="language_app",
    api_url="0.0.0.0:8000",
    bun_path="/app/.bun/bin/bun",
    db_url="sqlite:///reflex.db",
)
