import reflex as rx
import os

# Railway deployment with Caddy proxy
config = rx.Config(
    app_name="language_app",
    env=rx.Env.PROD,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)