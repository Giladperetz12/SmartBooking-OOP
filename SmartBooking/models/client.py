class Client:
    def __init__(self, client_id: int, name: str, email: str, phone_number: str):
        # checking validation

        # client id must be a positive integer
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError('Client ID must be positive integer')

        # the name must not be an empty string
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError('Name cannot be an empty string')

        # the phone number must be string of digits with normal length
        if (
                not isinstance(phone_number, str) or
                not phone_number.isdigit() or
                len(phone_number) > 12 or
                len(phone_number) < 9
        ):
            raise ValueError("Phone number must contain only digits and be 9–12 characters long")

        # basic email validation - domain , length etc..
        if not isinstance(email, str) or '@' not in email or '.' not in email.split('@')[-1]:
            raise ValueError("Invalid email address")

        self._client_id = client_id
        self._name = name
        self._email = email
        self._phone_number = phone_number
        self._orders = []
