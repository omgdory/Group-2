"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# TODO 1: Test Account Serialization
# - Ensure `to_dict()` correctly converts an account to a dictionary format.
# - Verify that all expected fields are included in the dictionary.

# TODO 2: Test Invalid Email Input
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.

# TODO 4: Test Positive Deposit
# - Ensure `deposit()` correctly increases the account balance.
# - Verify that depositing a positive amount updates the balance correctly.


# ===========================
# Test: Test Deposit with Zero/Negative Values
# Author: Ashley Arellano
# Date: 2025-02-02
# Description: Ensure `deposit()` raises an error for zero or negative amounts
# and verify that balance remains unchanged after an invalid deposit attempt
# ===========================
# TODO 5: Test Deposit with Zero/Negative Values
@pytest.mark.parametrize("invalid_amount", [0, -10.00])  # Test with both 0 and a negative value
def test_deposit_invalid_values(invalid_amount):
    # Creating a generic account to test `deposit()` with invalid values
    account = Account(name="John Doe", email="johndoe@example.com",balance=0.00)
    db.session.add(account)
    db.session.commit()
    
    # Setting a negative amount to test with and retrieving account from database
    retrieved_account = Account.query.filter_by(email="johndoe@example.com").first()

    # Attempt to deposit amount
    with pytest.raises(DataValidationError, match="Deposit amount must be positive"):
        retrieved_account.deposit(invalid_amount) #Should raise error if amount is zero or negative
    # Update account
    db.session.commit() 

    # Retrieve updated account
    updated_account = Account.query.filter_by(email="johndoe@example.com").first()
    # Verify that balance remains unchanged
    assert retrieved_account.balance == updated_account.balance

# TODO 6: Test Valid Withdrawal
# - Ensure `withdraw()` correctly decreases the account balance.
# - Verify that withdrawals within available balance succeed.

# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# ===========================
# Test: Withdrawal with Insufficient Funds
# Author: Franklin La Rosa Diaz
# Date: 2025-02-02
# Description: Ensure `withdraw()` prevents withdrawals that exceed available balance.
# ===========================

def test_withdraw_insufficient_funds():
    """Test that withdrawing more than the available balance fails and does not change balance."""

    # Create an account with a small balance
    account = Account(name="Test User", email="testuser@example.com", balance=50.00)

    # Add the account to the session and commit it to the database
    db.session.add(account)
    db.session.commit()

   # Attempt to withdraw more than the balance
    with pytest.raises(DataValidationError, match="Insufficient balance"):
        account.withdraw(100.0)  ## Trying to withdraw 100.0, which exceeds the balance of 50.0

    # Retrieve the account from the database to ensure the balance hasn't been changed
    retrieved_account = Account.query.filter_by(email="testuser@example.com").first()
    # Verify balance remains unchanged
    assert retrieved_account.balance == 50.0  # Balance should not have changed

# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.

