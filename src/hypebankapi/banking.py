from abc import ABC, abstractmethod
import json
import requests


from .utils import loginrequired


class Banking(ABC):
    """
    An abstract base class for banking operations.

    Exceptions:
    - AuthenticationError: Raised when an error occurs during authentication.
    - AuthenticationFailure: Raised when an authentication error occurs during a request
      for which the user should already be authenticated.
    - RequestException: Raised when an error occurs during a request to the backend.

    Abstract Methods:
    - ENROLL_URL (property): The URL for enrolling in the banking service.
    - PROFILE_URL (property): The URL for retrieving the user profile.
    - BALANCE_URL (property): The URL for retrieving the account balance.
    - CARD_URL (property): The URL for retrieving the user's card information.
    - MOVEMENTS_URL (property): The URL for retrieving the user's movements.
    - login(*args, **kwargs): Performs user login.
    - otp2fa(*args, **kwargs): Performs OTP verification for two-factor authentication.
    - renew(*args, **kwargs): Renews the authentication token.
    - get_movements(*args, **kwargs): Retrieves user movements.

    Methods:
    - _api_request(**kwargs): Wrapper for requests to the backend.

    """
    class AuthenticationError(Exception):
        """
        Raised when an error occurs during authentication.
        """

    class AuthenticationFailure(Exception):
        """
        Raised when an authentication error occurs during a request
        for which the user should already be authenticated.
        """

    class RequestException(Exception):
        """
        Raised when an error occurs during a request to the
        backend.
        """

    @property
    @classmethod
    @abstractmethod
    def ENROLL_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def PROFILE_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def BALANCE_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def CARD_URL(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def MOVEMENTS_URL(cls):
        return NotImplementedError

    def __init__(self):
        """
        Initializes a new instance of the Banking class.
        """
        self.token = None
        self._session = requests.Session()
        super().__init__()

    def _api_request(self, **kwargs):
        """
        Wrapper for requests to the backend. Checks if the request was
        successful, then returns the response data.

        Args:
        - **kwargs: Keyword arguments for the request.

        Returns:
        - dict: The response data.

        Raises:
        - RequestException: If an error occurs during the request.

        """
        response = self._session.request(**kwargs)
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise self.RequestException("Failed to parse response: " + response.text)
        if "responseCode" not in data:
            raise self.RequestException("Missing response code from response: " + response.text)
        if data["responseCode"] in ("401", "007"):
            raise self.AuthenticationFailure
        if data["responseCode"] != "200":
            raise self.RequestException("Server returned response {responseCode}: {responseDescr}".format(**data))
        return data["data"]

    @abstractmethod
    def login(self, *args, **kwargs):
        """
        Performs user login.

        Args:
        - *args: Variable length arguments.
        - **kwargs: Keyword arguments.

        """

    @abstractmethod
    def otp2fa(self, *args, **kwargs):
        """
        OTP code verification for two-factor authentication.

        Args:
        - *args: Variable length arguments.
        - **kwargs: Keyword arguments.

        """

    @abstractmethod
    def renew(self, *args, **kwargs):
        """
        Renews the authentication token.

        Args:
        - *args: Variable length arguments.
        - **kwargs: Keyword arguments.

        """

    @loginrequired
    def get_profile_info(self):
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

    @loginrequired
    def get_card_info(self):
        """
        Retrieves the user's card information.

        Returns:
        - dict: The JSON response containing the card
        
        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
        return self._api_request(method="GET", url=self.CARD_URL)

    @abstractmethod
    def get_movements(self, *args, **kwargs):
        """
        Retrieves the user's movements.

        Args:
        - *args: Variable length arguments.
        - **kwargs: Keyword arguments.

        Returns:
        - dict: The JSON response containing the movements.

        Raises:
        - AuthenticationError: If the user is not logged in.
        - RequestException: If the API request fails.

        """
