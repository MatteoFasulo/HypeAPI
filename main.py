import banking
from hype import Hype
from getpass import getpass  # For interactive password input
from utils import save_json

h = Hype()
h.login("EMAIL", getpass(), "BIRTH DATE")

# Wait for OTP code to arrive via SMS

h.otp2fa(int(input("OTP: ")))

# You are now logged in

try:
    profile = h.get_profile()
    balance = h.get_balance()
    card = h.get_card()
    movements = h.get_movements(limit=50)

    save_json(profile, 'profile.json')
    save_json(balance, 'balance.json')
    save_json(card, 'card.json')
    save_json(movements, 'movements.json')
    
except banking.Banking.AuthenticationFailure:
    # Token has expired
    h.renew()
    print('Renew Token')