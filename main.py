import requests
from web3 import Web3, HTTPProvider
import time

# Approve spending for ERC721 LINK on Pegswap address. Approve spending for ERC20 LINK on Quickswap router address.

# Configuration
RPC_URL = '' # RPC to desired chain.
WALLET = '' # Oracle owner address.
PRIVATE_KEY = '' # Oracle owner wallet private key.
NODE_WALLET = '' # Node wallet.
NODE_PRIVATE = '' # Node wallet private key.
ORACLE = '' # Oracle address.
MINIMUM = 15 * 10 ** 18 # 15 MATIC.
SWAPAMOUNT = 1 * 10 ** 18 # 1 LINK.

# Telegram configuration
key = '' # Telegram bot API key.
messageid = '' # Telgram receiver ID.
enabled = True # Switch True/False.

# Contract configuration
ORACLE_ABI = '[{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_payment","type":"uint256"},{"name":"_specId","type":"bytes32"},{"name":"_callbackAddress","type":"address"},{"name":"_callbackFunctionId","type":"bytes4"},{"name":"_nonce","type":"uint256"},{"name":"_dataVersion","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"oracleRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_requestId","type":"bytes32"},{"name":"_payment","type":"uint256"},{"name":"_callbackAddress","type":"address"},{"name":"_callbackFunctionId","type":"bytes4"},{"name":"_expiration","type":"uint256"},{"name":"_data","type":"bytes32"}],"name":"fulfillOracleRequest","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"EXPIRY_TIME","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"withdrawable","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_requestId","type":"bytes32"},{"name":"_payment","type":"uint256"},{"name":"_callbackFunc","type":"bytes4"},{"name":"_expiration","type":"uint256"}],"name":"cancelOracleRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_node","type":"address"},{"name":"_allowed","type":"bool"}],"name":"setFulfillmentPermission","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_sender","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"onTokenTransfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_node","type":"address"}],"name":"getAuthorizationStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_recipient","type":"address"},{"name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_link","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"specId","type":"bytes32"},{"indexed":false,"name":"requester","type":"address"},{"indexed":false,"name":"requestId","type":"bytes32"},{"indexed":false,"name":"payment","type":"uint256"},{"indexed":false,"name":"callbackAddr","type":"address"},{"indexed":false,"name":"callbackFunctionId","type":"bytes4"},{"indexed":false,"name":"cancelExpiration","type":"uint256"},{"indexed":false,"name":"dataVersion","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"OracleRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"requestId","type":"bytes32"}],"name":"CancelOracleRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"}],"name":"OwnershipRenounced","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]'
PEGSWAP = '0xAA1DC356dc4B18f30C347798FD5379F3D77ABC5b' #Pegswap address.
PEGSWAP_ABI = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"source","type":"address"},{"indexed":true,"internalType":"address","name":"target","type":"address"}],"name":"LiquidityUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferRequested","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"target","type":"address"}],"name":"StuckTokensRecovered","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"address","name":"source","type":"address"},{"indexed":true,"internalType":"address","name":"target","type":"address"},{"indexed":true,"internalType":"address","name":"caller","type":"address"}],"name":"TokensSwapped","type":"event"},{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"source","type":"address"},{"internalType":"address","name":"target","type":"address"}],"name":"addLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"source","type":"address"},{"internalType":"address","name":"target","type":"address"}],"name":"getSwappableAmount","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"targetData","type":"bytes"}],"name":"onTokenTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"target","type":"address"}],"name":"recoverStuckTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"source","type":"address"},{"internalType":"address","name":"target","type":"address"}],"name":"removeLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"source","type":"address"},{"internalType":"address","name":"target","type":"address"}],"name":"swap","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
LINK_ERC721 = '0xb0897686c545045aFc77CF20eC7A532E3120E0F1'
LINK_ERC20 = '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39'
QUICKSWAP = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff' #Quickswap router address.
QUICKSWAP_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
WMATIC = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270' #Matic address.

##################
w3 = Web3(HTTPProvider(RPC_URL))
print('Web3 Connected: ' + str(w3.isConnected()))

ORACLE_CONTRACT = w3.eth.contract(address=ORACLE, abi=ORACLE_ABI)  # Get Base token contract instance.
PEGSWAP_CONTRACT = w3.eth.contract(address=PEGSWAP, abi=PEGSWAP_ABI)  # Get Base token contract instance.
QUICKSWAP_CONTRACT = w3.eth.contract(address=QUICKSWAP, abi=QUICKSWAP_ABI)  # Get Base token contract instance.

def messageSend(tx1,tx2,tx3):
    message = 'Matic balance refilled.\n\nTx Withdraw: ' + str(tx1) + '\nTx Bridge: ' + str(tx2) + '\nTx Swap: ' + str(tx3)
    url = 'https://api.telegram.org/bot' + str(key) + '/sendMessage?chat_id=' + str(messageid) + '&disable_web_page_preview=true&parse_mode=HTML&text=' + message
    if enabled == True:
        requests.post(url)  # TELEGRAM

def withdrawLINK(AMOUNT):
    global tx1
    # Gas settings
    gas = 250000
    gasPrice = w3.toWei('40', 'gwei')
    print('Using max gas: ' + str(gas))
    print('Using max gas price: ' + str(gasPrice))

    # Nonce
    nonceCount = w3.eth.getTransactionCount(WALLET)
    print('Using nonce: ' + str(nonceCount))

    # Set TX parameters
    tx_params = {
        'from': WALLET,
        'gas': gas,
        'gasPrice': gasPrice,
        'value': 0,
        'nonce': nonceCount
    }

    # Call swap function
    witdraw = ORACLE_CONTRACT.functions.withdraw(
        str(NODE_WALLET),
        int(AMOUNT))

    transaction = witdraw.buildTransaction(tx_params)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    time.sleep(3)
    tx_token = w3.toHex(tx_token)
    print('Tx - Withdraw from oracle:')
    print(tx_token)
    checkConfirmation(tx_token)
    tx1 = tx_token

def bridgeLINK(AMOUNT):
    global tx2, nonceCount
    # Gas settings
    gas = 250000
    gasPrice = w3.toWei('100', 'gwei')
    print('Using max gas: ' + str(gas))
    print('Using max gas price: ' + str(gasPrice))

    # Nonce
    nonceCount = w3.eth.getTransactionCount(NODE_WALLET)
    print('Using nonce: ' + str(nonceCount))

    # Set TX parameters
    tx_params = {
        'from': NODE_WALLET,
        'gas': gas,
        'gasPrice': gasPrice,
        'value': 0,
        'nonce': nonceCount
    }

    # Call swap function
    bridge = PEGSWAP_CONTRACT.functions.swap(
        int(AMOUNT),
        str(LINK_ERC721),
        str(LINK_ERC20))

    transaction = bridge.buildTransaction(tx_params)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=NODE_PRIVATE)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    time.sleep(3)
    tx_token = w3.toHex(tx_token)
    print('Tx - Bridge LINK ERC721 to LINK ERC20:')
    print(tx_token)
    tx2 = tx_token

def swapLINK(AMOUNT,nonceCount):
    global tx3
    fromAmount = AMOUNT
    toAmount = 0

    # Gas settings
    gas = 250000
    gasPrice = w3.toWei('40', 'gwei')
    print('Using max gas: ' + str(gas))
    print('Using max gas price: ' + str(gasPrice))

    # PATH
    path = [LINK_ERC20,WMATIC]
    print('Using path: ' + str(path))

    # Nonce
    nonceCount = nonceCount + 1
    print('Using nonce: ' + str(nonceCount))

    # Set TX parameters
    tx_params = {
        'from': NODE_WALLET,
        'gas': gas,
        'gasPrice': gasPrice,
        'value': 0,
        'nonce': nonceCount
    }

    # Call swap function
    swap = QUICKSWAP_CONTRACT.functions.swapExactTokensForETH(
        int(fromAmount),
        int(toAmount),
        path,
        NODE_WALLET,
        int(time.time()) + 100 * 60)

    transaction = swap.buildTransaction(tx_params)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=NODE_PRIVATE)
    tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    time.sleep(3)
    tx_token = w3.toHex(tx_token)
    print('Tx - Swap to MATIC:')
    print(tx_token)
    checkConfirmation(tx_token)
    tx3 = tx_token

def checkConfirmation(tx_token):
    confirmed = 0
    statusTX = w3.eth.get_transaction(tx_token)
    # print(statusTX)
    if "None" in str(statusTX):
        print("Tx Still confirming")
        time.sleep(1)
    else:
        print("Tx confirmed")
        confirmed = confirmed + 1
        time.sleep(1)

if __name__ == '__main__':
    while True:
        print('LINK to MATIC, Current contract: ' + str(ORACLE))
        BALANCE = ORACLE_CONTRACT.functions.withdrawable().call({'from': WALLET})
        print('Current contract balance: ' + str(round(BALANCE / 10 ** 18,3)) + ' LINK')
        NODE_BALANCE = w3.eth.getBalance(NODE_WALLET)
        print('Current node balance: ' + str(round(NODE_BALANCE / 10 ** 18,3)) + ' MATIC')
        print('Current minimum balance: ' + str(round(MINIMUM / 10 ** 18, 3)) + ' MATIC')

        if NODE_BALANCE < MINIMUM:
            withdrawLINK(SWAPAMOUNT)
            bridgeLINK(SWAPAMOUNT)
            swapLINK(SWAPAMOUNT,nonceCount)
            messageSend(tx1,tx2,tx3)
            time.sleep(15)
        else:
            print('Enough matic available.')
            time.sleep(15)
