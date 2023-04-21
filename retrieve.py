from utils.dbconfig import dbconfig   # import database configuration
from rich import print as printc   # import the rich library for pretty printing
from rich.console import Console   # import Console from rich library for more advanced console output
from rich.table import Table   # import Table from rich library for creating tables

import utils.aesutil   # import aesutil module from utils package
import pyperclip   # import pyperclip for copying text to clipboard

from getpass import getpass   # import getpass to get password from user input
from Crypto.protocol.KDF import PBKDF2   # import PBKDF2 from Crypto library for password-based key derivation
from Crypto.Hash import SHA512   # import SHA512 from Crypto library for hash function
from Crypto.Random import get_random_bytes   # import get_random_bytes from Crypto library for generating random bytes
python
Copy code
def computeMasterKey(mp, ds):
	password = mp.encode()   # encode the master password
	salt = ds.encode()   # encode the database salt
	key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)   # derive a key using PBKDF2
	return key   # return the derived key
	
#This function takes two parameters - mp (the master password) and ds (the database salt), encodes them as bytes, and uses PBKDF2 to derive a 32-byte key by using the SHA512 hash function with 1,000,000 iterations. The function returns the derived key.

python
Copy code
def retrieveEntries(mp, ds, search, decryptPassword=False):
	db = dbconfig()   # connect to the database using dbconfig
	cursor = db.cursor()   # create a cursor object

	if len(search) == 0:
		query = "SELECT * FROM pm.entries"
	else:
		query = "SELECT * FROM pm.entries WHERE "
		for i in search:
			query += f"{i} = '{search[i]}' AND "
		query = query[:-5]

	cursor.execute(query)   # execute the SQL query
	results = cursor.fetchall()   # fetch all rows from the query result

	if len(results) == 0:   # if no rows found
		printc("[yellow][-][/yellow] No results for the search")
		return

	if (decryptPassword and len(results) > 1) or (not decryptPassword):
		table = Table(title="Results")
		table.add_column("Site Name")
		table.add_column("URL",)
		table.add_column("Email")
		table.add_column("Username")
		table.add_column("Password")
    
    for i in results:   # loop through each row of the query result
			table.add_row(i[0], i[1], i[2], i[3], "{hidden}")   # add each row to the table with the password hidden
		console = Console()
		console.print(table)   # print the table to the console
		return

	if decryptPassword and len(results) == 1:   # if only one row found and decrypt password is True
    
		# Compute master key
		mk = computeMasterKey(mp, ds)   # derive the master key

		# decrypt password
		decrypted = utils.aesutil.decrypt(key=mk, source=results[0][4], keyType="bytes")   # decrypt the password using AES
		pyperclip.copy(decrypted.decode())   # copy the decrypted password to the clipboard
		printc("[green][+][/green] Password copied to clipboard
		
		# Close the database connection
    db.close()
