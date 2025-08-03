import reflex as rx
import os

# Railway deployment configuration
config = rx.Config(
    app_name="language_app",
    env=rx.Env.PROD,
    api_url="https://lingo.up.railway.app",
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)