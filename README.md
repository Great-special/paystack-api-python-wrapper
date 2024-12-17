# Example Usage
"""
Example of how to use the PayStack API wrapper
"""
# Initialize the PayStack client
paystack = PayStack('your_secret_key')


# Initialize a transaction
success, transaction = paystack.initialize_transaction(
    email='customer@example.com',
    amount=5000  # 50.00 in base currency
)

# Charge a card
card_details = {
    "number": "4084084084084081",
    "cvv": "123",
    "expiry_month": "12",
    "expiry_year": "25"
}


success, charge_response = paystack.charge_card(
    email='customer@example.com', 
    amount=5000, 
    card_details=card_details
)

# Create a transfer recipient
success, recipient = paystack.create_transfer_recipient({
    "name": "John Doe",
    "account_number": "0123456789",
    "bank_code": "044"
})

# Perform a bank transfer
success, transfer = paystack.bank_transfer(
    recipient=recipient, 
    amount=1000
)
