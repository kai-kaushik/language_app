import reflex as rx
import os

# Railway deployment configuration
# The api_url must include port 8000 for backend communication
config = rx.Config(
    app_name="language_app",
    env=rx.Env.PROD,
    api_url="https://lingo.up.railway.app:8000",
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)