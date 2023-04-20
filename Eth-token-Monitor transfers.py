from decimal import Decimal
from web3 import Web3
import time
import json

bsc = 'https://bsc-dataseed.binance.org'
web3 = Web3(Web3.HTTPProvider(bsc))
token_contract_address = '0x...'

with open(".../usdt.json") as f:
    token_abi = json.load(f)

token = web3.eth.contract(address=token_contract_address, abi=token_abi)

def transfer_token(private_key, from_account, to, amount):
    gasPrice = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(from_account)
    tx = {
        'nonce': nonce,
        'value': 0,
        'gas': 0,
        'gasPrice': gasPrice,
        'chainId': 56
    }
    gas = web3.eth.estimate_gas(tx)
    tx.update({'gas': gas})
    txn = token.functions.transfer(to, web3.to_wei(amount, 'ether')).build_transaction(tx)
    signed_tx = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(web3.to_hex(tx_hash))

if __name__ == '__main__':
    private_key = '0x...'
    recipient = '0x...'
# Change the name to main.py
    sender = web3.eth.account.from_key(private_key).address
    transfer_amount = Decimal(web3.from_wei(token.functions.balanceOf(sender).call(), 'ether'))
    while True:
        if transfer_amount > Decimal(1000):
            transfer_token(private_key, sender, recipient, transfer_amount)
            print("Token transfer: " + str(transfer_amount))
            continue
        else:
            print("NOW Token balance: " + str(transfer_amount))
            print("Insufficient funds, 3 second init...")
            time.sleep(3)
