"""
Test Cases for Account Model
"""
import json
import random
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
# ===========================
# Test: Account Serialization
# Author: Dorian Akhavan
# Date: 2025-02-04
# Description: Ensure account can be serialized.
# ===========================

def test_account_serialization():
    """Test assigning roles to an account"""
    account = Account(name="Dorian Akhavan", email="dorian@cs472.com", role="user")

    # serialize
    test_dict = account.to_dict()

    # ensure that serialization worked (check every value)
    assert test_dict["id"] == account.id
    assert test_dict["name"] == account.name
    assert test_dict["email"] == account.email
    assert test_dict["phone_number"] == account.phone_number
    assert test_dict["disabled"] == account.disabled
    assert test_dict["date_joined"] == account.date_joined
    assert test_dict["balance"] == account.balance
    assert test_dict["role"] == account.role

# TODO 2: Test Invalid Email Input
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.

# ===========================
# Test: Test Invalid Email Input
# Author: Jose Alarcon
# Date: 2025-02-02
# Description: Ensure accounts without an email cannot be created.
# ===========================
@pytest.mark.parametrize("invalid_email", [
    "email",
    "@usernamemissing.com",
    "no_at.com",
    "username@.com",
    "username@com",
    "not-an-email"
])

def test_invalid_email(invalid_email):
    account = Account(name="Test User", email=invalid_email)  # account with invalid email

    with pytest.raises(DataValidationError, match="Invalid email format"):
        account.validate_email()  # raise an exception

def test_missing_email():
    with pytest.raises(TypeError):
        account = Account(name="Test User", email=None)  # pass None
        account.validate_email()  # raise TypeError (None != string)

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.

# ===========================
# Test: Missing Required Fields in Account()
# Author: [Abdulrahman Alharbi]
# Date: [02.02.2025]
# Description: Ensure that an account cannot be created without required fields.
# ===========================


import pytest
from models.account import Account
from sqlalchemy.exc import IntegrityError
from models import db

def test_missing_required_fields():
    """Test that creating an account with missing fields raises an IntegrityError."""
    
    # Attempt to create an account with no name
    with pytest.raises(IntegrityError):
        account = Account(email="missingname@example.com")
        db.session.add(account)
        db.session.commit()
    db.session.rollback()  # Reset DB state

    # Attempt to create an account with no email
    with pytest.raises(IntegrityError):
        account = Account(name="Missing Email")
        db.session.add(account)
        db.session.commit()
    db.session.rollback()  # Reset DB state

# TODO 4: Test Positive Deposit
# ===========================
# Test: Test Positive Deposit
# Author: Aviendha Andrus
# Date: 2025-02-3
# Description: Ensure `deposit()` correctly increases account balance
# and verifies that depositing a positive amount updates balance correctly.
# ===========================
def test_positive_deposit():
   """Test that depositing a positive amount increases the balance"""

   # create new account with existing balance
   account = Account(name="John Doe", email="johndoe@example.com",balance=0.00)
   db.session.add(account)
   db.session.commit()

   old_balance = account.balance
   deposit_amount = random.randint(1, 101)
   account.deposit(deposit_amount)
  
   # testing line 55 of account.py 'self.balance += amount'
   assert account.balance == old_balance + deposit_amount


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


# ===========================
# Test: Test Valid Withdrawal
# Author: Charles Joseph (CJ) Ballesteros
# Date: 2025-02-02
# Description:
# - Ensure `withdraw()` correctly decreases the account balance.
# - Verify that withdrawals within available balance succeed.
# ===========================
# TODO 6: Test Valid Withdrawal
@pytest.mark.parametrize("invalid_amount", [0.00, 100.00])  # Test with both 0 and a negative value
def test_valid_withdraw(invalid_amount):
    account = Account(name="Yukino Sakimuri", email="YukinoSakimuri@gmail.com", balance=101.00)
    db.session.add(account)
    db.session.commit()

    old_balance = account.balance
    withdraw_amount = random.randint(0, 100)
    account.withdraw(withdraw_amount)

    assert account.balance == old_balance - withdraw_amount

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

# ===========================
# Test: Password Hashing
# Author: Sameer Issa
# Date: 2025-02-03
# Description: Ensure that passwords are hashed and set properly
# ===========================
# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.
def test_set_password():
    """Test that the password is hashed and stored correctly"""
    
    password = "password1"

    # create account and set password, then commit to db
    account = Account(name="person one",email="person1@example.com",role="user")
    account.set_password(password)
    db.session.add(account)
    db.session.commit

    # check that the password is stored 
    assert account.password_hash is not None
    
    # check that password is hashed
    assert account.password_hash != password
    
def test_check_password():
    """Test that given password matches the stored password"""
    
    password = "password1"

    # create account and set password, then commit to db
    account = Account(name="person two",email="person2@example.com",role="user")
    account.set_password(password)
    db.session.add(account)
    db.session.commit

    # check for correct password
    assert account.check_password(password)
    # check for wrong password
    assert not account.check_password("password2")
    


# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# ===========================
# Test: Test invalid role assignment
# Author: Christopher Liscano
# Date: 2025-02-3
# Description: Ensure that assigning an invalid role raises an appropriate error.
#              Verify that only allowed roles (`admin`, `user`, etc.) can be set.
# ===========================
def test_invalid_role_assignment():
    # create an account with valid role
    account = Account(name="John Doe", email="johndoe@example.com", role="admin")
    db.session.add(account)
    db.session.commit()

    # showing that attempting an invalid role causes an error
    invalid_roles = ["Chris", "guest", "test", "", None, ":>", "idk"]
    for invalid_role in invalid_roles:
        with pytest.raises(DataValidationError, match="Invalid role"):
            account.change_role(invalid_role)

    # get account from database
    get_account = Account.query.filter_by(email="johndoe@example.com").first()

    # check if role is unchanged
    assert get_account.role == "admin"

    # verifying that only allowed roles can be set
    account.change_role("admin")
    db.session.commit()

    # check if change was successful
    check_account = Account.query.filter_by(email="johndoe@example.com").first()
    assert check_account.role == "admin"

# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.

