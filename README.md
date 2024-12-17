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


Here's the list of **covered Paystack API endpoints** based on your provided class:

---

### **Transaction Management**
1. **Initialize Transaction**:  
   - Endpoint: `/transaction/initialize`  
   - Method: `POST`  
   - Method: `initialize_transaction`

2. **Verify Transaction**:  
   - Endpoint: `/transaction/verify/{reference}`  
   - Method: `GET`  
   - Method: `verify_transaction`

---

### **Charge Management**
3. **Charge a Card**:  
   - Endpoint: `/charge`  
   - Method: `POST`  
   - Method: `charge_card`

---

### **Transfer Management**
4. **Single Bank Transfer**:  
   - Endpoint: `/transfer`  
   - Method: `POST`  
   - Method: `bank_transfer`

5. **Bulk Transfer**:  
   - Endpoint: `/transfer/bulk`  
   - Method: `POST`  
   - Method: `bulk_transfer`

---

### **Bank and Account Management**
6. **List Banks**:  
   - Endpoint: `/bank`  
   - Method: `GET`  
   - Method: `list_banks`

7. **Resolve Bank Account**:  
   - Endpoint: `/bank/resolve`  
   - Method: `GET`  
   - Method: `resolve_bank_account`

8. **Create Transfer Recipient**:  
   - Endpoint: `/transferrecipient`  
   - Method: `POST`  
   - Method: `create_transfer_recipient`

---

### Summary of Endpoints:
| **Feature**                    | **Endpoint**                    | **HTTP Method** | **Class Method**            |
|--------------------------------|---------------------------------|-----------------|-----------------------------|
| Initialize Transaction         | `/transaction/initialize`       | POST            | `initialize_transaction`    |
| Verify Transaction             | `/transaction/verify/{reference}`| GET            | `verify_transaction`        |
| Charge Card                    | `/charge`                       | POST            | `charge_card`               |
| Single Bank Transfer           | `/transfer`                     | POST            | `bank_transfer`             |
| Bulk Transfer                  | `/transfer/bulk`                | POST            | `bulk_transfer`             |
| List Banks                     | `/bank`                         | GET             | `list_banks`                |
| Resolve Bank Account           | `/bank/resolve`                 | GET             | `resolve_bank_account`      |
| Create Transfer Recipient      | `/transferrecipient`            | POST            | `create_transfer_recipient` |
| **Fetch Balances**             | `/balance`                      | GET             | `fetch_balance`             |
| **Retrieve Transfer**          | `/transfer/{transfer_id}`       | GET             | `retrieve_transfer`         |

---

Thanks to ChatGPT and Claude.
