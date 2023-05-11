# HypeAPI

Modulo Python non ufficiale per interagire con l'API delle carte HYPE.

## Note
- HYPE consente di utilizzare un solo dispositivo per volta. Effettuando il login con questo modulo si verrà disconnessi dall'applicazione e viceversa.

## Docker
`start.sh` will run the python script and then build the image with all the data generated:
```sh
./start.sh
docker run -p 8501:8501 hype_dashboard
```
Then visit http://127.0.0.1:8501 to view the Streamlit app!

## Standalone
The `main.py` script supports argparse for command line arguments:
```python
python main.py -m EMAIL -b BIRTHDATE [-v]
```
The script is invoked using the following command-line arguments:
- `-m EMAIL`, `--email EMAIL`: Specifies the email address. It is a required argument.
- `-b BIRTHDATE`, `--birthdate BIRTHDATE`: Specifies the birth date. It is a required argument.
- `-v`, `--verbose`: Enables verbose output. It is an optional flag argument.

In order to run the streamlit app you need to run `main.py` and then execute:
```python
streamlit run Home.py --server.port=8501 --server.address=127.0.0.1
```
>Home.py is the main Streamlit page. The WebApp has multiple pages inside the pages folder!

## Disclaimer
I contenuti di questo repository sono a scopo informativo e frutto di ricerca personale. L'autore non è affiliato, associato, autorizzato, appoggiato da o in alcun modo legato con Banca Sella S.p.A., o con le società controllate da esse. Tutti i marchi registrati appartengono ai rispettivi proprietari.

## Ringraziamenti
- [@jacopo-j/HypeAPI](https://github.com/jacopo-j/HypeAPI) per l'interfaccia con l'API