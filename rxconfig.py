import reflex as rx
import os

# Railway deployment - uses environment variable for dynamic URL
config = rx.Config(
    app_name="language_app",
    env=rx.Env.PROD,
)