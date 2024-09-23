from web3 import Web3
from django.conf import settings
import json

def get_web3():
    return Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))

def get_contract():
    web3 = get_web3()
    with open(settings.CONTRACT_ABI_PATH, 'r') as abi_file:
        abi = json.load(abi_file)
    return web3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=abi)

def create_record(patient_address, record_id, ipfs_hash):
    contract = get_contract()
    tx_hash = contract.functions.createRecord(record_id, ipfs_hash).transact({'from': patient_address})
    tx_receipt = get_web3().eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def grant_access(patient_address, record_id, doctor_address):
    contract = get_contract()
    tx_hash = contract.functions.grantAccess(record_id, doctor_address).transact({'from': patient_address})
    tx_receipt = get_web3().eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def revoke_access(patient_address, record_id, doctor_address):
    contract = get_contract()
    tx_hash = contract.functions.revokeAccess(record_id, doctor_address).transact({'from': patient_address})
    tx_receipt = get_web3().eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def get_record(address, record_id):
    contract = get_contract()
    return contract.functions.getRecord(record_id).call({'from': address})