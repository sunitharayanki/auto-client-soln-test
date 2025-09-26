from faker import Faker
from datetime import datetime, timedelta
import random
import csv

# Initialize Faker with a specific locale
fake = Faker('en_US')

# --- Helper Functions for Specific Field Requirements ---

def generate_svc_ref_nbr():
    """Generates a random 5-character string."""
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))

def generate_invalid_email():
    """Generates a clearly invalid email address."""
    choices = [
        "not-an-email",
        f"{fake.word()}@missing-dot",
        f"{fake.word()}{fake.word()}{fake.word()}",
        f"{fake.word()}@{fake.word()}@{fake.word()}.com",
        f"{fake.word()}@{fake.word()}",
    ]
    return random.choice(choices)

def generate_vin_and_vehicle():
    """Generates a valid-looking VIN and associated vehicle data."""
    vin = fake.vin()
    
    # Placeholder logic to associate a basic make/model/year with the VIN
    year_choice = random.randint(2010, 2025)
    make_model_choices = {
        'Ford': ['F-150', 'Focus', 'Mustang'],
        'Honda': ['CRV', 'Civic', 'Pilot'],
        'Toyota': ['Camry', 'Corolla', 'Tacoma'],
        'Chevrolet': ['Silverado', 'Equinox', 'Malibu']
    }
    make_choice = random.choice(list(make_model_choices.keys()))
    model_choice = random.choice(make_model_choices[make_choice])
    
    return {
        'vin': vin,
        'year': year_choice,
        'make': make_choice,
        'model': model_choice
    }

# --- Main Script ---

# File name for the output
filename = 'test_data_50_rows.psv'

# The field names in order, including placeholders for unknown/blank fields
fieldnames = [
    'svc_ref_nbr', 'transaction_Type', 'contract_number', 'client_note_1', 'plan_code',
    'effective_date', 'unknown_7', 'unknown_8', 'first_name', 'last_name',
    'address1', 'address2', 'city', 'state', 'zip_code', 'phone', 'email',
    'year', 'make', 'model', 'vin', 'unknown_22', 'unknown_23', 'unknown_24',
    'expiration_date', '', 'billing_data_element'
]

# Generate 50 rows of data
data = []
for _ in range(50):
    effective_date_obj = fake.date_object()
    expiration_date_obj = effective_date_obj + timedelta(days=365*10)
    
    vin_data = generate_vin_and_vehicle()

    # Generate a random `billing_data_element` in the specified format
    billing_data = f"MPP-767-{random.randint(1000000000, 9999999999)}"

    # Create the row as a dictionary
    row_data = {
        'svc_ref_nbr': generate_svc_ref_nbr(),
        'transaction_Type': random.choice(['N', 'C', 'R', 'U']),
        'contract_number': f"MPP{random.randint(10000000000000000000, 99999999999999999999)}",
        'client_note_1': f"{random.randint(100, 999)}",
        'plan_code': random.choice(['AB', 'AC', 'AA']),
        'effective_date': effective_date_obj.strftime('%Y%m%d'),
        'unknown_7': '',
        'unknown_8': '',
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'address1': fake.street_address(),
        'address2': fake.secondary_address(),
        'city': fake.city(),
        'state': fake.state_abbr(),
        'zip_code': fake.zipcode(),
        'phone': fake.phone_number(),
        'email': generate_invalid_email(),
        'year': vin_data['year'],
        'make': vin_data['make'],
        'model': vin_data['model'],
        'vin': vin_data['vin'],
        'unknown_22': '',
        'unknown_23': '',
        'unknown_24': '',
        'expiration_date': expiration_date_obj.strftime('%Y%m%d'),
        'billing_data_element': billing_data
    }
    data.append(row_data)

# Write the data to a file
with open(filename, 'w', newline='') as f:
    # Use DictWriter to handle the dictionary structure, specifying the pipe delimiter
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|', extrasaction='ignore')
    
    # Write the header row
    writer.writeheader()
    
    # Write the data rows
    for row in data:
        # Convert dictionary to a list to handle position 26 which is empty
        row_list = [row.get(field, '') for field in fieldnames]
        f.write('|'.join(map(str, row_list)) + '\n')

print(f"Successfully generated {len(data)} rows of test data in '{filename}'.")

