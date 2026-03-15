# Crea tu venv

python3 -m venv .venv

# Activa tu ambiente

.venv\Scripts\activate

# Instalar SDK de Ollama

pip install ollama

# Desactiva tu ambiente al terminar

deactivate

# Freeze

pip freeze > requirements.txt

# Requirements install

pip install -r requirements.txt
