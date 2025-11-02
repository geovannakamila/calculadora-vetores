# Calculadora Vetorial (Flask)

## Rodar localmente
```bash
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```

## Deploy no Render (grátis)
1. Suba estes arquivos para um repositório no GitHub.
2. No https://render.com crie **New +** → **Web Service** → **Build from repo**.
3. **Runtime**: Python.  
   **Build Command**: `pip install -r requirements.txt`  
   **Start Command**: `gunicorn app:app`
4. Deploy. O Render gerará uma URL pública.

## Deploy no PythonAnywhere
1. Faça upload dos arquivos para o **Files**.
2. Em **Web** → **Add a new web app** → **Manual config** → escolha Python 3.11.
3. Crie um virtualenv, instale requirements, e aponte o WSGI para `app:app`.
4. **Reload** do site.
