import uvicorn
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Abre o navegador após 1.5 segundos para garantir que o server subiu
    Timer(1.5, open_browser).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

