import mysql.connector
from web3 import Web3, HTTPProvider
import time

# connect to mariaDB
mysql_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="zks-nft-event"
)
mysql_cursor = mysql_connection.cursor()

nft_abi = """[
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "name_",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "symbol_",
          "type": "string"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "approved",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "Approval",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "operator",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "bool",
          "name": "approved",
          "type": "bool"
        }
      ],
      "name": "ApprovalForAll",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "Transfer",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "approve",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "getApproved",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "operator",
          "type": "address"
        }
      ],
      "name": "isApprovedForAll",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "name",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "ownerOf",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        },
        {
          "internalType": "bytes",
          "name": "data",
          "type": "bytes"
        }
      ],
      "name": "safeTransferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "operator",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "approved",
          "type": "bool"
        }
      ],
      "name": "setApprovalForAll",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bytes4",
          "name": "interfaceId",
          "type": "bytes4"
        }
      ],
      "name": "supportsInterface",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "symbol",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "tokenURI",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "tokenId",
          "type": "uint256"
        }
      ],
      "name": "transferFrom",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]"""

# topic_filter
topic_filter = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'


# connect to rpc
def connect_to_rpc():
    w3 = Web3(HTTPProvider('https://1rpc.io/eth'))
    return w3


w3 = connect_to_rpc()

current_block_number = w3.eth.block_number

# get last block number
select_last_processed_block_query = "SELECT MAX(block_number) FROM zks_processed_blocks"
mysql_cursor.execute(select_last_processed_block_query)
last_processed_block = mysql_cursor.fetchone()[0]
start_block_number = last_processed_block + 1 if last_processed_block is not None else 17413150

# get events
for block_number in range(start_block_number, current_block_number + 1):

    # get all event from the block
    while True:
        try:
            block_logs = w3.eth.get_logs({
                'fromBlock': block_number,
                'toBlock': block_number,
                'topics': [topic_filter, None, None, None]
            })
            break
        except Exception as e:
            print(f"An error occurred while fetching logs for block {block_number}: {str(e)}")
            print("Retrying after 10 seconds...")
            time.sleep(10)
            w3 = connect_to_rpc()

    # get the real Transfer event of erc721
    for event in block_logs:

        if (len(event['topics']) == 4):


            #######################################################################
            #######                 collection_address                    #########
            #######################################################################

            # get event nft address
            collection_address = w3.toChecksumAddress(event['address'])

            # cheak if nft have been record
            select_query = "SELECT COUNT(*) FROM zks_collections WHERE collection_address = %s"
            select_values = (collection_address,)
            mysql_cursor.execute(select_query, select_values)
            count = mysql_cursor.fetchone()[0]

            nft_contract = w3.eth.contract(address=collection_address, abi=nft_abi)

            # insert collection data
            if count == 0:

                # get nft detail
                try:
                    name = nft_contract.functions.name().call()
                except Exception as e:
                    name = "NotValue"
                try:
                    symbol = nft_contract.functions.symbol().call()
                except Exception as e:
                    symbol = "NotValue"

                insert_query = "INSERT INTO zks_collections (collection_address, collection_name, collection_symbol) VALUES (%s, %s, %s)"
                insert_values = (collection_address, name, symbol)
                mysql_cursor.execute(insert_query, insert_values)
                mysql_connection.commit()
                print("zks_collection_address insert success")

            #######################################################################
            #######                        zks_owners                     #########
            #######################################################################

            # get new owner address
            tep_address = w3.toHex(event['topics'][2])
            tep_address = tep_address[2:].lstrip('0')
            owner_address = "0x" + tep_address.rjust(40, '0')
            owner_address = w3.toChecksumAddress(owner_address)

            # cheak if owner have been record
            select_query = "SELECT COUNT(*) FROM zks_owners WHERE owner_address = %s"
            select_values = (owner_address,)
            mysql_cursor.execute(select_query, select_values)
            count = mysql_cursor.fetchone()[0]

            # insert owner data
            if count == 0:
                insert_query = "INSERT INTO zks_owners (owner_address) VALUES (%s)"
                insert_values = (owner_address,)
                mysql_cursor.execute(insert_query, insert_values)
                mysql_connection.commit()
                print("zks_owners insert success")



            #######################################################################
            #######             zks_collections__zks_owners               #########
            #######################################################################

            # get collection id
            select_collection_id_query = "SELECT id FROM zks_collections WHERE collection_address = %s"
            mysql_cursor.execute(select_collection_id_query, (collection_address,))
            collection_id = mysql_cursor.fetchone()[0]

            # get owner id
            select_owner_id_query = "SELECT id FROM zks_owners WHERE owner_address = %s"
            mysql_cursor.execute(select_owner_id_query, (owner_address,))
            owner_id = mysql_cursor.fetchone()[0]

            # insert to middle table

            tokenId = w3.toInt(event['topics'][3])
            tx = w3.toHex(event['transactionHash'])

            try:
                tokenURI = nft_contract.functions.tokenURI(tokenId).call()
            except Exception as e:
                tokenURI = "NotValue"

            check_existing_record_query = "SELECT * FROM zks_collections__zks_owners WHERE zks_collections_id = %s AND tokenId = %s"
            mysql_cursor.execute(check_existing_record_query, (collection_id, tokenId))
            existing_record = mysql_cursor.fetchone()


            try:
                ## exist update, else insert
                if existing_record:
                    update_middle_table_query = "UPDATE zks_collections__zks_owners SET zks_owners_id = %s, tokenURI = %s, lastUpdateTx=  %s WHERE zks_collections_id = %s AND tokenId = %s"
                    mysql_cursor.execute(update_middle_table_query, (owner_id, tokenURI, tx, collection_id, tokenId))
                else:
                    insert_middle_table_query = "INSERT INTO zks_collections__zks_owners (zks_owners_id, tokenURI, lastUpdateTx, zks_collections_id, tokenId) VALUES (%s, %s, %s, %s, %s)"
                    mysql_cursor.execute(insert_middle_table_query, (owner_id, tokenURI, tx, collection_id, tokenId))
                print("zks_collections__zks_owners insert success")
            except Exception as e:
                print(f"An error occurred while update middle table: {str(e)}")
                insert_query = "INSERT INTO zks_collections__zks_owners (lastUpdateTx, error_status, error_detail) VALUES (%s, %s, %s)"
                insert_values = (tx, True, str(e))
                mysql_cursor.execute(insert_query, insert_values)
            mysql_connection.commit()


    # insert processed block
    insert_block_query = "INSERT INTO zks_processed_blocks (block_number) VALUES (%s)"
    insert_block_values = (block_number,)
    mysql_cursor.execute(insert_block_query, insert_block_values)
    mysql_connection.commit()

# close
mysql_cursor.close()
mysql_connection.close()
