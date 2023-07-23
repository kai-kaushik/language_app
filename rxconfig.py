import reflex as rx
import os


# Get the value of the PORT environment variable, or use 8000 if it's not set
# port = os.environ.get('PORT', '3000')

# Local
config = rx.Config(
    app_name="language_app",
    db_url="sqlite:///pynecone.db",
    env=rx.Env.DEV,
)

# Fly / Docker
# config = rx.Config(
#     app_name="language_app",
#     api_url="http://0.0.0.0:8000",
#     bun_path="/language_app/.bun/bin/bun",
#     db_url="sqlite:///reflex.db",
# )