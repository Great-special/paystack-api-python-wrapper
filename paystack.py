import requests
import json
import uuid

class PayStack:
    """
    A comprehensive wrapper for the Paystack API with easy-to-use methods
    for various financial transactions and operations.
    """
    
    def __init__(self, secret_key, default_currency='NGN'):
        """
        Initialize the PayStack client
        
        :param secret_key: Your Paystack secret key
        :param default_currency: Default transaction currency (default: NGN)
        """
        self.secret_key = secret_key
        self.base_url = 'https://api.paystack.co'
        self.default_currency = default_currency
    
    def _prepare_request(self, method, endpoint, data=None, params=None):
        """
        Prepare and execute API requests with comprehensive error handling
        
        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param endpoint: API endpoint
        :param data: Request payload
        :param params: Query parameters
        :return: Tuple of (success, response_data)
        """
        # Construct full URL
        url = f"{self.base_url}{endpoint}"
        
        # Prepare headers
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare payload
        payload = json.dumps(data) if data else None
        
        # Map HTTP methods
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }
        
        try:
            # Execute request
            response = method_map[method](
                url, 
                headers=headers, 
                data=payload, 
                params=params
            )
            
            # Process response
            if response.status_code in [200, 201]:
                response_data = response.json()
                return True, response_data.get('data', response_data)
            else:
                return False, response.json()
        
        except requests.RequestException as e:
            return False, {"error": str(e)}
    
    def initialize_transaction(self, email, amount, **kwargs):
        """
        Initialize a transaction
        
        :param email: Customer email
        :param amount: Transaction amount
        :param kwargs: Additional transaction parameters
        :return: Transaction initialization details
        """
        # Convert amount to kobo
        amount_kobo = int(amount * 100)
        
        # Prepare payload
        payload = {
            "email": email,
            "amount": amount_kobo,
            "currency": kwargs.get('currency', self.default_currency),
            **kwargs
        }
        
        return self._prepare_request('POST', '/transaction/initialize', payload)
    
    def verify_transaction(self, reference):
        """
        Verify a transaction
        
        :param reference: Transaction reference
        :return: Transaction verification details
        """
        return self._prepare_request('GET', f'/transaction/verify/{reference}')
    
    def charge_card(self, email, amount, card_details, **kwargs):
        """
        Charge a card
        
        :param email: Customer email
        :param amount: Charge amount
        :param card_details: Card information
        :param kwargs: Additional parameters
        :return: Card charge response
        """
        # Convert amount to kobo
        amount_kobo = int(amount * 100)
        
        # Prepare payload
        payload = {
            "email": email,
            "amount": amount_kobo,
            "card": card_details,
            "currency": kwargs.get('currency', self.default_currency),
            "reference": kwargs.get('reference', str(uuid.uuid4())),
            **kwargs
        }
        
        return self._prepare_request('POST', '/charge', payload)
    
    def bank_transfer(self, recipient, amount, **kwargs):
        """
        Perform a bank transfer
        
        :param recipient: Recipient details (dict with account details)
        :param amount: Transfer amount
        :param kwargs: Additional transfer parameters
        :return: Transfer response
        """
        # Convert amount to kobo
        amount_kobo = int(amount * 100)
        
        # Prepare payload
        payload = {
            "source": "balance",
            "amount": amount_kobo,
            "recipient": recipient.get('recipient_code'),
            "currency": kwargs.get('currency', self.default_currency),
            "reference": kwargs.get('reference', str(uuid.uuid4())),
            **kwargs
        }
        
        return self._prepare_request('POST', '/transfer', payload)
    
    def bulk_transfer(self, transfers):
        """
        Perform bulk transfers
        
        :param transfers: List of transfer details
        :return: Bulk transfer response
        """
        # Prepare transfers (convert amounts to kobo)
        prepared_transfers = []
        for transfer in transfers:
            transfer_data = transfer.copy()
            transfer_data['amount'] = int(transfer['amount'] * 100)
            transfer_data['reference'] = transfer.get('reference', str(uuid.uuid4()))
            prepared_transfers.append(transfer_data)
        
        payload = {
            "currency": self.default_currency,
            "source": "balance",
            "transfers": prepared_transfers
        }
        
        return self._prepare_request('POST', '/transfer/bulk', payload)
    
    def list_banks(self, country='Nigeria', **kwargs):
        """
        List available banks
        
        :param country: Country to list banks for
        :param kwargs: Additional filtering parameters
        :return: List of banks
        """
        params = {
            "country": country.lower(),
            **kwargs
        }
        
        return self._prepare_request('GET', '/bank', params=params)
    
    def resolve_bank_account(self, account_number, bank_code):
        """
        Resolve bank account details
        
        :param account_number: Account number
        :param bank_code: Bank code
        :return: Account resolution details
        """
        params = {
            "account_number": account_number,
            "bank_code": bank_code
        }
        
        return self._prepare_request('GET', '/bank/resolve', params=params)
    
    def create_transfer_recipient(self, account_details):
        """
        Create a transfer recipient
        
        :param account_details: Recipient account information
        :return: Recipient creation response
        """
        payload = {
            "type": account_details.get('type', 'nuban'),
            "name": account_details['name'],
            "account_number": account_details['account_number'],
            "bank_code": account_details['bank_code'],
            "currency": account_details.get('currency', self.default_currency)
        }
        
        return self._prepare_request('POST', '/transferrecipient', payload)
