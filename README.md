# WL-Api-App
Web app using Wolne Lektury (polish book service) API and AI services to create educational summaries.

## Instalation
<h3>1. After cloning the repository you might have to create new venv.</h4>
If you're using Pycharm:\
File > Settings > Python Interpreter > Add Interpreter > Add local interpreter

You will need to rerun the terminal for the new venv to actually start working.
<h3>2. Install the requirements.</h4>
This step might be tricky but IDE should be helpful.\
Requirements are saved in "requirements.txt" file
but sometimes they won't be installed correctly and you might need to manually take care of it.

Command for automatic requirements install:\
pip install -r requirements.txt

Some of the packages I've had problems with and had to install them manually:
- streamlit==1.44.1
- google.genai
- openai
- aiohttp

<h3>3. Create secrets.toml.</h3>
You will need to create a folder ".streamlit" and a file "secrets.toml" inside it.
The file will contain your API keys.\
The whole path should be "project_folder/.streamlit/secrets.toml" and underneath you can see an example of the correct configuration.\
GEMINI_API_KEY = 'YOURKEY'\
GPT_API_KEY = 'YOURKEY'

That's everything, you just need to paste your keys in there.

<h3>4. Now you can run the app but it's not configured yet</h3>
Run the app by using that command:\
streamlit run .\ui\streamlit_app\main.py
\
\
Streamlit will show you the apps address in your Python terminal and most probably will open the app automatically in your browser.

<h3>5. Create input/output folders for books data</h3>
The project doesn't include the folders for you books data but it has a admin panel that will let you create them with only few buttons.

After running the app you will be in the main view. On the sidebar navigate to "Admin" and then click on buttons:
* Utwórz katalogi na dane...
* Usuń wszystkie książki...
* Zaktualizuj indeksy książek

If every file and folder was created correctly, your app should now be ready to rock.

<h3> Some useful things </h3>
In core/config you will find some config files like gemini_config - feel free to change model or whatever you want.

**Kill the process**\
taskkill /f /im streamlit.exe\

### Requirements generation (for example, for copying the project).
pip freeze > requirements.txt

### Modele Gemini
// gemini-flash-latest
// gemini-flasj-3.1
  "model": "gemini-2.5-flash-lite",

### Wersja streamlit (zalecana, bezpieczna) streamlit==1.44.1

