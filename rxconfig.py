import reflex as rx
import os

# Railway deployment configuration  
config = rx.Config(
    app_name="language_app",
    env=rx.Env.PROD,
    backend_host="0.0.0.0",
    backend_port=8000,
    frontend_host="0.0.0.0", 
    frontend_port=3000,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)