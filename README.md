This readme file was generated on 2026-06-10 by Michał Rakoczy

# GENERAL INFORMATION

**Project name:** Using the wolnelektury.pl API and language models for automation of creation of educational summaries
**Version:** v1.0.0
**Short description:** Python/Streamlit app designed to automate the process of creating educational summaries.

___

# PROJECT OVERVIEW

**Full description:** WL-Api-App is a web application using the Wolne Lektury (Polish book service) API and AI services to automatically create educational summaries of books.
**Date of creation:** 2026-06-10
**Project Organization:** Python and Streamlit-based project. Core configurations are located in `core/config`. The user interface and main execution script are located in `ui/streamlit_app`.
**Software project size:** 470 MiB   

___

# INSTALLATION

**Step by step instructions:** 
1. Clone the repository.
2. Create a new virtual environment. If you're using PyCharm: `File > Settings > Python Interpreter > Add Interpreter > Add local interpreter`. Restart your terminal to activate the environment.
3. Install the requirements via the command line: `pip install -r requirements.txt`.

**System requirements:** Python environment. Windows (to utilize specific process termination commands).
**Required libraries, packages, modules:** Dependencies are listed in `requirements.txt`. *(Note: For copying the project, you can generate this using `pip freeze > requirements.txt`)*
**Setup requirements:** Create a folder named `.streamlit` in the root directory and a file `secrets.toml` inside it to hold your API keys. The path should be `project_folder/.streamlit/secrets.toml`.

Example configuration:
```toml
GEMINI_API_KEY = 'YOURKEY'
GPT_API_KEY = 'YOURKEY'
```

**Known issues:** Sometimes dependencies won't install correctly from the `requirements.txt` file and you might need to manually install them. Known problematic packages include:
  - `streamlit==1.44.1` (This version is recommended and safe)
  - `google.genai`
  - `openai`
  - `aiohttp`

___

# USAGE
 
**Step by step instructions:** 
1. **Run the app:** Use the following command to start the app: 
   `streamlit run ui/streamlit_app/main.py`
   Streamlit will show you the app's address in your Python terminal and will likely open the app automatically in your browser.
2. **Create input/output folders for books data:** The project doesn't include folders for your books data initially, but has an admin panel to create them. On the app sidebar, navigate to "Admin" and then click on the following buttons:
   - Utwórz katalogi na dane...
   - Usuń wszystkie książki...
   - Zaktualizuj indeksy książek
   If every file and folder was created correctly, your app should now be ready to use.
3. **Customizing Configurations:** In `core/config` you will find config files like `gemini_config` - feel free to change the model (e.g., `gemini-2.5-flash-lite`, `gemini-flash-latest`, `gemini-flash-3.1`) or any other configurations you want.
4. **Killing the process (Windows):** If you need to force close the app, run `taskkill /f /im streamlit.exe`

**Known limitations:** None known at this time.

___

# LICENSE

**Software License:** [Licencja do uzupełnienia po konsultacji z promotorem]
**Preferred citation:** Rakoczy, M. (2026). Using the wolnelektury.pl API and language models for automation of creation of educational summaries

___

# CONTACT INFORMATION

**Contact**
Name: Michał Rakoczy
Role: Developer
Institution: University of Economics in Katowice
Email: michal.rakoczy@edu.uekat.pl

___

# ACKNOWLEDGEMENTS

**Publications using our software:** [Do wstawienia po publikacji pracy]
**Related relationships:** Utilizes the Wolne Lektury API, OpenAI API, and Google Gemini API.
**Contributors:** Michał Rakoczy
