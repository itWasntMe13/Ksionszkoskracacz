# WL-Api-App
Web app using Wolne Lektury (polish book service) API to download and present some of the first features of my degree project.

## Quick installation info
Important note - you need to specify your own **OPENAI_API_KEY** key:\
If you are using Windows, Streamlit will try to find your GPT API key in:\
X:/Users/(user)/.streamlit/secrets.toml file.\
**If you don't have it, create it and add one line - OPENAI_API_KEY = (your_key).**\
It might be different for you, but I was too lazy to do something more sophisticated.

1. **Create venv if you don't have it already. Pycharm will do it for you: Settings > Python Interpreter  > Add Interpreter > Add local interpreter.**
2. **Remember to rerun the terminal after configuring venv or it won't behave like it should.** 
3. **Install the requirements.**\
pip install -r requirements.txt
4. **Run the Streamlit app.**\
streamlit run ui/streamlit_app/main.py\
**By default the app will be on: http://localhost:8501**

### Important note for editing Streamlit front app: If you edit anything other than main.py, then Streamlit might have some trouble with detecting/reruning these changes. I recommend killing the process from CMD and reruning it from IDE terminal.
**Kill the process**\
taskkill /f /im streamlit.exe\
**Rerun from IDE**\
streamlit run ui/streamlit_app/main.py

## Some useful things
### Requirements generation (for example, for copying the project).
pip freeze > requirements.txt

### Requirements installation.
pip install -r requirements.txt

### Streamlit app run
streamlit run path_to_file.py\
**example:**\
streamlit run ui/streamlit_app/main.py

### Zabicie Streamlita
taskkill /f /im streamlit.exe   - Windows\
killall streamlit               - Linux/macOS (jeśli dostępne)
