import mysql.connector

# connect to mariaDB
mysql_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="zks-nft-event"
)
mysql_cursor = mysql_connection.cursor()



# 0 ---  create collections table
create_collection_table_query = """
CREATE TABLE IF NOT EXISTS zks_collections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  collection_address VARCHAR(42),
  collection_name LongText,
  collection_symbol LongText
)
"""
mysql_cursor.execute(create_collection_table_query)

# 1 --- create owners table
create_owner_table_query = """
CREATE TABLE IF NOT EXISTS zks_owners (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_address VARCHAR(42)
)
"""
mysql_cursor.execute(create_owner_table_query)



# 2 --- create collections__owners table
create_zks_collections__zks_owners_table_query = """
CREATE TABLE IF NOT EXISTS zks_collections__zks_owners (
  id INT AUTO_INCREMENT PRIMARY KEY,
  zks_collections_id INT,
  FOREIGN KEY (zks_collections_id) REFERENCES zks_collections(id),
  zks_owners_id INT,
  FOREIGN KEY (zks_owners_id) REFERENCES zks_owners(id),
  tokenId INT,
  tokenURI LongText,
  lastUpdateTx LongText,
  error_status BOOLEAN DEFAULT FALSE,
  error_detail LongText
)
"""
mysql_cursor.execute(create_zks_collections__zks_owners_table_query)



# 3 --- create block number record table
create_block_table_query = """
CREATE TABLE IF NOT EXISTS zks_processed_blocks (
  block_number INT PRIMARY KEY
)
"""
mysql_cursor.execute(create_block_table_query)



# commit and close
mysql_connection.commit()
mysql_cursor.close()
mysql_connection.close()
