# 🌟 HypeAPI

Unofficial Python module for interacting with the HYPE card API.

## 📝 Notes
- HYPE only allows the use of one device at a time. Logging in with this module will disconnect you from the application and vice versa.

## 🐳 Docker
`start.sh` will run the python script and then build the image with all the data generated:
```sh
./start.sh
docker run -p 8501:8501 hype_dashboard
```
Then visit [http://127.0.0.1:8501](http://127.0.0.1:8501) to view the Streamlit app!

## 🚀 Standalone
The `main.py` script supports argparse for command line arguments:
```python
python main.py -m EMAIL -b BIRTHDATE [-v]
```
The script is invoked using the following command-line arguments:
- `-m EMAIL`, `--email EMAIL`: Specifies the email address. It is a required argument.
- `-b BIRTHDATE`, `--birthdate BIRTHDATE`: Specifies the birth date. It is a required argument.
- `-v`, `--verbose`: Enables verbose output. It is an optional flag argument.

In order to run the Streamlit app, you need to run `main.py` and then execute:
```python
streamlit run Home.py --server.port=8501 --server.address=127.0.0.1
```
> 📄 Home.py is the main Streamlit page. The WebApp has multiple pages inside the `pages` folder!

## ⚠️ Disclaimer
The contents of this repository are for informational purposes and the result of personal research. The author is not affiliated, associated, authorized, endorsed by, or in any way connected with Banca Sella S.p.A., or with its affiliated companies. All registered trademarks belong to their respective owners.

## 🙏 Acknowledgments
- [@jacopo-j/HypeAPI](https://github.com/jacopo-j/HypeAPI) for the API interface.

## Contributing
Thank you for considering contributing to the HypeAPI project! Please read the [Contributing Guidelines](CONTRIBUTING.md) for more information on how to contribute.

## Code of Conduct
We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the behavior we expect from our community members.