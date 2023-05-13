import json
from datetime import datetime, date
from uuid import uuid4
import requests


from .banking import Banking
from .utils import loginrequired


class Hype(Banking):
    """
    A class for interacting with the Hype banking API.

    Attributes:
    - ENROLL_URL (str): The URL for enrolling in the Hype service.
    - PROFILE_URL (str): The URL for retrieving the user profile.
    - BALANCE_URL (str): The URL for retrieving the account balance.
    - CARD_URL (str): The URL for retrieving the user's card information.
    - MOVEMENTS_URL (str): The URL for retrieving the user's recent movements.
    - APP_VERSION (str): The version of the Hype mobile app.
    - DEVICE_ID (str): The unique device ID used for authentication.
    - DEVICE_INFO (str): JSON string containing device information.

    Methods:
    - __init__(): Initializes the Hype instance.
    - login(username, password, birthdate): Logs in to the Hype service with the provided credentials.
    - otp2fa(code): Performs OTP verification using the provided code.
    - renew(): Renews the authentication token.
    - get_movements(limit=5): Retrieves recent movements with an optional limit.
    - get_card(): Retrieves the user's card information.
    - get_profile(): Retrieves the user's profile information.
    - get_balance(): Retrieves the account balance.

    """
    ENROLL_URL = "https://api.hype.it/v2/auth/hypeconnector.aspx"
    PROFILE_URL = "https://api.hype.it/v1/rest/u/profile"
    BALANCE_URL = "https://api.hype.it/v1/rest/u/balance"
    CARD_URL = "https://api.hype.it/v1/rest/your/card"
    MOVEMENTS_URL = "https://api.hype.it/v1/rest/m/last/{}"
    APP_VERSION = "5.1.6"
    DEVICE_ID = str(uuid4()).replace("-", "") + "hype"
    DEVICE_INFO = json.dumps({
        "jailbreak": "false",
        "osversion": "13.3.1",
        "model": "iPhone11,2"
    })

    def __init__(self):
        """
        Initializes a new instance of the Hype class.
        """
        self._username = None
        self.newids = None
        self.bin = None
        self.checksum = None
        super().__init__()

    def login(self, username, password, birthdate):
        """
        Logs in to the Hype service with the provided credentials.

        Args:
        - username (str): The username or codiceinternet of the user.
        - password (str): The password for the user's account.
        - birthdate (datetime.date or str or None): The birthdate of the user in datetime.date or string format. None if birthdate is not available.

        Raises:
        - ValueError: If the birthdate is invalid.
        - AuthenticationError: If the login fails or response parsing fails.

        """
        if isinstance(birthdate, (date, datetime)):
            dob = birthdate.strftime("%d/%m/%Y")
        elif isinstance(birthdate, str):
            dob = datetime.fromisoformat(birthdate).strftime("%d/%m/%Y")
        elif birthdate is None:
            dob = None
        else:
            raise ValueError("Invalid birth date")
        enroll1 = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "codiceinternet": username,
                "datanascita": dob,
                "deviceid": self.DEVICE_ID,
                "function": "FREE/LOGINFIRSTSTEP.SPR",
                "pin": password,
                "platform": "IPHONE"
            },
            timeout=10
        )
        try:
            if enroll1.json()["Check"] != "OK":
                raise self.AuthenticationError("Login failed")
        except json.decoder.JSONDecodeError:
            raise self.AuthenticationError(
                "Failed to parse response for login request")
        except KeyError:
            raise self.AuthenticationError("Login failed")
        enroll2 = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "deviceid": self.DEVICE_ID,
                "function": "INFO/ENROLLBIO.SPR",
                "platform": "IPHONE"
            },
            timeout=10
        )
        try:
            if enroll2.json()["ErrorMessage"] != "":
                raise self.AuthenticationError(
                    "Server returned error: " + enroll2.json()["ErrorMessage"])
        except json.decoder.JSONDecodeError:
            raise self.RequestException(
                "Failed to parse response for bioToken request")
        except KeyError:
            raise self.AuthenticationError(
                "Missing data in response for bioToken request")
        self.bin = enroll2.json()["Bin"]
        self._username = username

    def otp2fa(self, code):
        """
        Performs OTP verification using the provided code.

        Args:
        - code (str): The OTP code to verify.

        Raises:
        - Exception: If login() has not been called before OTP verification.
        - AuthenticationError: If the OTP verification fails or response parsing fails.

        """
        if self._username is None:
            raise Exception("Please login() before verifying OTP code")
        otp = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "codiceinternet": self._username,
                "deviceid": self.DEVICE_ID,
                "function": "FREE/LOGINSECONDSTEP.SPR",
                "pwd": str(code),
                "platform": "IPHONE"
            },
            timeout=10
        )
        try:
            if otp.json()["Check"] != "OK":
                raise self.AuthenticationError(
                    "OTP verification failed. Please login() again")
        except json.decoder.JSONDecodeError:
            raise self.RequestException(
                "Failed to parse response for OTP verification request")
        except KeyError:
            raise self.AuthenticationError(
                "OTP verification failed. Please login() again")
        self.checksum = otp.json()["Checksum"]
        self.token = self._session.cookies.get_dict()["token"]
        self.newids = self._session.cookies.get_dict()["newids"]
        self._session = requests.Session()
        self._session.headers.update({
            "hype_token": self.token,
            "newids": self.newids,
            "App-Version": self.APP_VERSION
        })

    @loginrequired
    def renew(self):
        """
        Renews the authentication token.

        Raises:
        - AuthenticationError: If the token renewal fails or response parsing fails.

        """
        renewal = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "bin": self.bin,
                "checksum": self.checksum,
                "deviceid": self.DEVICE_ID,
                "function": "FREE/LOGINFIRSTSTEPFA.SPR",
                "platform": "IPHONE"
            },
            timeout=10
        )
        try:
            if renewal.json()["Check"] != "OK":
                raise self.AuthenticationError("Renewal failed")
        except json.decoder.JSONDecodeError:
            raise self.AuthenticationError(
                "Failed to parse response for renewal request")
        except KeyError:
            raise self.AuthenticationError("Renewal failed")
        reenroll = self._session.post(
            self.ENROLL_URL,
            data={
                "additionalinfo": self.DEVICE_INFO,
                "deviceid": self.DEVICE_ID,
                "function": "INFO/ENROLLBIO.SPR",
                "platform": "IPHONE"
            },
            timeout=10
        )
        try:
            if reenroll.json()["ErrorMessage"] != "":
                raise self.AuthenticationError(
                    "Server returned error: " + reenroll.json()["ErrorMessage"])
        except json.decoder.JSONDecodeError:
            raise self.RequestException(
                "Failed to parse response for bioToken request")
        except KeyError:
            raise self.AuthenticationError(
                "Missing data in response for bioToken request")
        self.token = self._session.cookies.get_dict()["token"]
        self.newids = self._session.cookies.get_dict()["newids"]
        self._session = requests.Session()
        self._session.headers.update({
            "hype_token": self.token,
            "newids": self.newids,
            "App-Version": self.APP_VERSION
        })
        self.bin = reenroll.json()["Bin"]

    @loginrequired
    def get_movements(self, limit=5):
        """
        Retrieves recent movements with an optional limit.

        Args:
        - limit (int): The maximum number of movements to retrieve. Defaults to 5.

        Returns:
        - dict: The JSON response containing the movements.

        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
        return self._api_request(method="GET", url=self.MOVEMENTS_URL.format(limit))

    @loginrequired
    def get_card(self):
        """
        Retrieves the user's card information.

        Returns:
        - dict: The JSON response containing the card information.

        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
        return self._api_request(method="GET", url=self.CARD_URL)

    @loginrequired
    def get_profile(self):
        """
        Retrieves the user's profile information.

        Returns:
        - dict: The JSON response containing the profile information.

        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
        return self._api_request(method="GET", url=self.PROFILE_URL)

    @loginrequired
    def get_balance(self):
        """
        Retrieves the account balance.

        Returns:
        - dict: The JSON response containing the account balance.

        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
        return self._api_request(method="GET", url=self.BALANCE_URL)
