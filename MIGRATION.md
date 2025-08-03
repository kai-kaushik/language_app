# Reflex Migration Guide: Old Version → Modern Reflex + Railway Deployment

This guide documents the breaking changes encountered when migrating from old Reflex versions (0.2.0-0.5.x) to modern Reflex (0.8.4+) and deploying to Railway.

## Table of Contents
- [Breaking Changes by Component](#breaking-changes-by-component)
- [Railway Deployment Guide](#railway-deployment-guide)
- [Common Issues & Solutions](#common-issues--solutions)

---

## Breaking Changes by Component

### 1. **Function Signatures & Return Types**

#### ❌ **Old (Reflex 0.2.0-0.5.x)**
```python
def index() -> rx.component():
    return rx.text("Hello")
```

#### ✅ **New (Reflex 0.8.4+)**
```python
def index() -> rx.Component:
    return rx.text("Hello")
```

**Fix**: Change `rx.component()` to `rx.Component` (capital C, no parentheses)

---

### 2. **Heading Component Size Props**

#### ❌ **Old**
```python
rx.heading("Title", size="2xl")
rx.heading("Subtitle", size="xl") 
rx.heading("Small", size="lg")
```

#### ✅ **New**
```python
rx.heading("Title", size="9")      # Largest
rx.heading("Subtitle", size="8")   # Second largest  
rx.heading("Small", size="6")      # Medium
```

**Size Mapping**:
- `"2xl"` → `"9"` (largest)
- `"xl"` → `"8"` 
- `"lg"` → `"6"`
- `"md"` → `"4"`
- `"sm"` → `"2"`

---

### 3. **Layout Components**

#### ❌ **Old: `rx.responsive_grid`**
```python
return rx.responsive_grid(
    content,
    columns=[1, 1, 1],
    spacing="1em"
)
```

#### ✅ **New: `rx.container` + `rx.center`**
```python
return rx.container(
    rx.center(
        content,
        max_width="800px"
    )
)
```

---

### 4. **Flex Wrap Component**

#### ❌ **Old: `rx.wrap`**
```python
rx.wrap(
    select_politeness(),
)
```

#### ✅ **New: `rx.flex` with `flex_wrap`**
```python
rx.flex(
    select_politeness(),
    flex_wrap="wrap",
    justify="center",
)
```

---

### 5. **Spacing Props**

#### ❌ **Old: CSS Values**
```python
rx.vstack(
    content,
    spacing="1em"
)
```

#### ✅ **New: Numeric Strings**
```python
rx.vstack(
    content,
    spacing="4"  # Scale of 0-9
)
```

**Mapping**:
- `"1em"` → `"4"`
- `"0.5em"` → `"2"`  
- `"2em"` → `"6"`

---

### 6. **Select Component API**

#### ❌ **Old: Items as first parameter**
```python
rx.select(
    State.lang_list,
    placeholder="Select language",
    on_change=State.set_language
)
```

#### ✅ **New: Static lists required**
```python
rx.select(
    items=["English", "Japanese", "French"],
    placeholder="Select language", 
    on_change=State.set_language
)
```

**Note**: Modern Reflex requires static lists instead of state variables for select items.

---

### 7. **App Initialization**

#### ❌ **Old: State parameter**
```python
app = rx.App(state=State)
app.add_page(index, title="My App")
app.compile()
```

#### ✅ **New: No state parameter**
```python
app = rx.App()
app.add_page(index, title="My App")
# No compile() needed
```

---

### 8. **OpenAI API Integration**

#### ❌ **Old: Direct API key assignment**
```python
import openai
openai.api_key = os.environ["OPENAI_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
return response["choices"][0]["message"]["content"]
```

#### ✅ **New: Client initialization**
```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_KEY"])

response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}],
    timeout=30
)
return response.choices[0].message.content
```

---

### 9. **Gradient Text Styling**

#### ❌ **Old: Direct props**
```python
rx.heading(
    "Gradient Text",
    background_image="linear-gradient(...)",
    background_clip="text",
    font_weight="bold"
)
```

#### ✅ **New: Style dictionary**
```python
rx.heading(
    "Gradient Text",
    style={
        "background_image": "linear-gradient(...)",
        "background_clip": "text",
        "-webkit-background-clip": "text", 
        "-webkit-text-fill-color": "transparent",
        "font_weight": "bold"
    }
)
```

---

### 10. **Config Changes**

#### ❌ **Old: Basic config**
```python
config = rx.Config(
    app_name="my_app",
    env=rx.Env.PROD,
)
```

#### ✅ **New: Disable plugins**
```python
config = rx.Config(
    app_name="my_app", 
    env=rx.Env.PROD,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)
```

---

## Railway Deployment Guide

### Method 1: Using Railway's Official Reflex Template (Recommended)

#### Step 1: Get the Template
1. **Visit**: https://railway.com/template/A5TaaV
2. **Click "Deploy Now"**
3. **Choose "Create new repo from template"**
4. **Name your new repository** (e.g., `my-reflex-app-railway`)
5. **Deploy**

#### Step 2: Clone Template Locally
```bash
git clone https://github.com/YOUR_USERNAME/my-reflex-app-railway.git
cd my-reflex-app-railway
```

#### Step 3: Migrate Your Code
```bash
# Copy your main app file
cp /path/to/old-project/my_app/my_app.py ./my_reflex_app/my_reflex_app.py

# Copy requirements if you have additional dependencies
# Note: Merge with existing requirements.txt, don't replace
```

#### Step 4: Update File Structure
The Railway template expects this structure:
```
my-reflex-app-railway/
├── my_reflex_app/
│   ├── __init__.py
│   └── my_reflex_app.py    # Your main app code goes here
├── requirements.txt         # Already configured for Reflex
├── rxconfig.py             # Already configured for Railway
├── Caddyfile              # Handles routing (don't modify)
├── nixpacks.toml          # Build configuration (don't modify)
└── README.md
```

#### Step 5: Apply Breaking Changes
Update your copied `my_reflex_app.py` using the [Breaking Changes](#breaking-changes-by-component) section above.

#### Step 6: Update Requirements
If you have additional dependencies, add them to `requirements.txt`:
```txt
# Existing template requirements
reflex>=0.8.4
gunicorn

# Your additional dependencies
openai>=1.51.0
# Add other packages you need
```

#### Step 7: Configure Environment Variables
In Railway dashboard:
1. **Go to your deployment**
2. **Variables tab**
3. **Add your environment variables**:
   - `OPENAI_KEY=your-actual-api-key`
   - Any other API keys or secrets

#### Step 8: Deploy
```bash
git add .
git commit -m "Migrate app to Railway template"
git push
```

Railway will automatically redeploy with your code.

---

### Method 2: Convert Existing Repository

If you want to convert your existing repo instead of using the template:

#### Step 1: Add Required Files

**Create `Caddyfile`:**
```caddyfile
:{$PORT}

handle /_event/* {
	reverse_proxy localhost:8000
}

handle /backend/* {
	reverse_proxy localhost:8000
}

handle {
	try_files {path} /index.html
	file_server {
		root .web/_static
	}
}
```

**Create/Update `nixpacks.toml`:**
```toml
[variables]
NIXPACKS_PYTHON_VERSION = "3.11"

[phases.setup]
nixPkgs = ["python311", "nodejs-18_x", "unzip", "curl", "caddy"]

[phases.install] 
cmds = [
    "python -m venv /opt/venv",
    ". /opt/venv/bin/activate && pip install -r requirements.txt"
]

[phases.build]
cmds = [
    ". /opt/venv/bin/activate && reflex init",
    ". /opt/venv/bin/activate && reflex export --frontend-only"
]

[start]
cmd = ". /opt/venv/bin/activate && reflex run --env prod --backend-only --backend-host 0.0.0.0 --backend-port 8000 & caddy run --config ./Caddyfile"
```

**Update `rxconfig.py`:**
```python
import reflex as rx

config = rx.Config(
    app_name="your_app_name",
    env=rx.Env.PROD,
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    show_built_with_reflex=False,
)
```

#### Step 2: Update Dependencies
```txt
reflex>=0.8.4
openai>=1.51.0
```

#### Step 3: Apply Breaking Changes & Deploy
Follow steps 5-8 from Method 1.

---

## Common Issues & Solutions

### Issue 1: "No reflex attribute [component_name]"
**Cause**: Component was removed or renamed in newer Reflex versions.

**Solutions**:
- `rx.responsive_grid` → Use `rx.container` + `rx.center`
- `rx.wrap` → Use `rx.flex` with `flex_wrap="wrap"`

### Issue 2: "Invalid var passed for prop [prop_name]"
**Cause**: Prop accepts different values in newer versions.

**Solutions**:
- Heading sizes: `"xl"` → `"8"`
- Spacing: `"1em"` → `"4"`

### Issue 3: "Cannot connect to server: timeout"
**Cause**: Frontend can't reach backend WebSocket endpoint.

**Solution**: Use Railway template with Caddy proxy configuration.

### Issue 4: OpenAI API Errors  
**Cause**: Old OpenAI library syntax.

**Solution**: Update to modern client initialization pattern.

### Issue 5: "Built with Reflex" Badge Covering UI
**Solution**: 
```python
# In rxconfig.py
config = rx.Config(
    show_built_with_reflex=False,  # May require paid plan
)

# Or move conflicting elements to different positions
rx.button(position="fixed", top="1em", right="1em")
```

---

## Migration Checklist

### Before Migration:
- [ ] Backup your old project
- [ ] Note your current Reflex version: `pip show reflex`
- [ ] List all custom components and state variables used
- [ ] Document any third-party integrations (OpenAI, etc.)

### During Migration:
- [ ] Update function return types (`rx.component()` → `rx.Component`)
- [ ] Fix heading sizes (`"xl"` → `"8"`)
- [ ] Replace layout components (`rx.responsive_grid` → `rx.container`)
- [ ] Update spacing props (`"1em"` → `"4"`)
- [ ] Fix select components (static items)
- [ ] Update app initialization (remove state parameter)
- [ ] Modernize API integrations (OpenAI, etc.)
- [ ] Update styling (gradient text, etc.)

### After Migration:
- [ ] Test all functionality locally
- [ ] Deploy to Railway using template
- [ ] Set environment variables
- [ ] Test production deployment
- [ ] Monitor for any remaining issues

---

## Version Compatibility

| Component | Old Reflex (≤0.5.x) | New Reflex (≥0.8.x) |
|-----------|-------------------|-------------------|
| Function types | `rx.component()` | `rx.Component` |
| Heading sizes | `"xl", "lg"` | `"8", "6"` |
| Layout | `rx.responsive_grid` | `rx.container` + `rx.center` |
| Flex wrap | `rx.wrap` | `rx.flex(flex_wrap="wrap")` |
| Spacing | `"1em"` | `"4"` |
| Select | State variables | Static lists |
| App init | `rx.App(state=State)` | `rx.App()` |
| OpenAI | `openai.ChatCompletion` | `client.chat.completions` |

---

*This guide was created during the migration of a language translation app from Reflex 0.2.0 to 0.8.4 with Railway deployment. It documents real-world breaking changes encountered in production.*