# 🌟 HypeAPI

Unofficial Python module for interacting with the HYPE card API.

## 📝 Notes
- HYPE only allows the use of one device at a time. Logging in with this module will disconnect you from the application and vice versa.

## 🚀 Usage
```python
from hypebankapi import Hype, utils
from getpass import getpass

h = Hype()
h.login(EMAIL, getpass(), BIRTH-DATE) # Change EMAIL and BIRTH-DATE

# Wait for OTP code to arrive via SMS

h.otp2fa(int(input("OTP: ")))

profile = h.get_profile()
balance = h.get_balance()
card = h.get_card()
movements = h.get_movements(limit=50) # change the limit of transactions fetched

utils.save_json(profile, 'profile.json')
utils.save_json(balance, 'balance.json')
utils.save_json(card, 'card.json')
utils.save_json(movements, 'movements.json')
```

## ⚠️ Disclaimer
The contents of this repository are for informational purposes and the result of personal research. The author is not affiliated, associated, authorized, endorsed by, or in any way connected with Banca Sella S.p.A., or with its affiliated companies. All registered trademarks belong to their respective owners.

## 🙏 Acknowledgments
- [@jacopo-j/HypeAPI](https://github.com/jacopo-j/HypeAPI) for the API interface.

## Contributing
Thank you for considering contributing to the HypeAPI project! Please read the [Contributing Guidelines](CONTRIBUTING.md) for more information on how to contribute.

## Code of Conduct
We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the behavior we expect from our community members.