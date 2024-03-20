import requests
import uuid

# Sample fee data
fees = [
    {'fee_set_name': 'NEC127A PPC Pass Thru Fee Set 1',
     'description': 'CE Pays CRx $0.05 Per Click | $0.01 Pass Thru',
     'fee_set_effectiveDate': '2019-04-23',
     'feeSetTypeId': '486a88da-fe9e-4a03-acf2-677fe13c0f8f',
     'isBillReplenishment': False,
     'ownerId': '8ab76b27-a595-4f37-a563-323c5c97ab78',
     'ownerTypeId': '112efb8d-3245-4ca5-a612-f5250dd99a94',
     'feeGroupId': 'b64bc53e-d9e4-4692-9340-af116e90e090',
     'feePriorityId': 'f5986f18-233a-4ef7-b484-ed983b91d4d3',
     'feeTypeId': '258e3b15-3ac5-4a88-9963-3beec90ef834',
     'payeeId': '75e401d1-f4a3-452a-bd4f-200e3aefee16',
     'payorId': '9096b5f0-31ef-42a9-9b53-80d825e88722',
     'chargeSummary': '$.05',
     'effectiveDate': '2019-04-23',
     'chargeTypeId': 'd6dd76e7-e3bf-4a8a-890f-bfd827eae7bc',
     'chargeValue': '0.05',
     'max': '',
     'name': 'Per Click',
     'qualifierSummary': None},
]

# API URLs
fee_set_URL = 'https://api.example.com/fee_sets/'
fee_events_URL = 'https://api.example.com/fee_events/'
fee_details_URL = 'https://api.example.com/fee_details/'

# Authorization token
auth_token = 'YOUR_AUTH_TOKEN'

# Header for API requests
header = {'Authorization': 'Bearer ' + auth_token}

# List to store failed fee data
failures = []

# Dictionary to store fee set IDs
list_of_fees = {}

# Iterate through fees
for fee in fees:
    fee_set_guid = ''
    fee_events_guid = str(uuid.uuid4())
    fee_detail_guid = str(uuid.uuid4())
    fee_guid = str(uuid.uuid4())

    # Check if fee set exists
    if fee['fee_set_name'] in list_of_fees.keys():
        fee_set_guid = list_of_fees[fee['fee_set_name']]
        print(fee_set_guid, '\n')
    else:
        fee_set_guid = str(uuid.uuid4())
        list_of_fees[fee['fee_set_name']] = fee_set_guid
        print('Added ' + fee_set_guid)

        # Create new fee set
        fee_set = {
            'id': fee_set_guid,
            'name': fee['fee_set_name'],
            'description': fee['description'],
            'effectiveDate': fee['fee_set_effectiveDate'],
            'feeEventsDTOList': [],
            'feeSetTypeId': fee['feeSetTypeId'],
            'isBillReplenishment': fee['isBillReplenishment'],
            'ownerId': fee['ownerId'],
            'ownerTypeId': fee['ownerTypeId'],
        }

        # Send POST request to create fee set
        response = requests.post(fee_set_URL, json=fee_set, headers=header)
        print(response)
        print(response.text)

    # Create new fee event
    fee_to_add = {
        'id': fee_events_guid,
        'feeSetId': fee_set_guid,
        'feeGroupId': fee['feeGroupId'],
        'feePriorityId': fee['feePriorityId'],
        'feeTypeId': fee['feeTypeId'],
        'payeeId': fee['payeeId'],
        'payorId': fee['payorId'],
    }

    # Send POST request to create fee event
    response2 = requests.post(fee_events_URL, json=fee_to_add, headers=header)
    print(response2)
    print(response2.text, '\n')

    # Create new fee details
    fee_to_add_details = {
        'id': fee_detail_guid,
        'feeEventId': fee_events_guid,
        'chargeSummary': fee['chargeSummary'],
        'effectiveDate': fee['effectiveDate'],
        'feePricesDTOList': [{
            'id': fee_guid,
            'feeDetailsId': fee_detail_guid,
            'chargeTypeId': fee['chargeTypeId'],
            'chargeValue': fee['chargeValue']
        }],
        'max': fee['max'],
        'name': fee['name'],
        'qualifierSummary': fee['qualifierSummary']
    }

    # Send POST request to create fee details
    response3 = requests.post(fee_details_URL, json=fee_to_add_details, headers=header)
    print(response3)
    print(response3.text, '\n')

    # Check for failures
    if (response.status_code != 201 or response2.status_code != 201 or response2.status_code != 201):
        failures.append(fee)

# Write failed fee set names to file
with open('failures.txt', 'w') as f:
    for failure in failures:
        f.write(failure['fee_set_name'])
