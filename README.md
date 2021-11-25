# Chainlink_Polygon_Matic_Balancer
Checks the node MATIC balance and refills it.

1. Checks node wallet MATIC balance.
2. Withdraws LINK from contract.
3. Swaps ERC721 LINK for ERC20 LINK on pegswap.
4. Swaps LINK for MATIC on quickswap.
5. Sends Telegram message with TX id's. (OPTIONAL)

Before you start:
1. Edit configuration variables in main.py
2. Approve spending of 0xb0897686c545045aFc77CF20eC7A532E3120E0F1 (ERC721 LINK) from 0xAA1DC356dc4B18f30C347798FD5379F3D77ABC5b (Pegswap).
3. Approve spending of 0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39 (ERC20 LINK) from 0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff (Quickswap).

To get telegram ID use @myidbot.
