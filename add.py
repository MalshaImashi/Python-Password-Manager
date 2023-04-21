from getpass import getpass # imports the getpass function from the getpass module, which prompts the user for input without displaying the text on the screen (useful for inputting passwords securely).
from Crypto.protocol.KDF import PBKDF2 # imports the PBKDF2 key derivation function from the Crypto library's protocol.KDF module.
from Crypto.Hash import SHA512 # imports the SHA512 hash function from the Crypto library's Hash module.
from Crypto.Random import get_random_bytes #  imports the get_random_bytes function from the Crypto library's Random module.

import utils.aesutil # imports the aesutil module from the utils package.

def computeMasterKey(mp,ds):
    """
    This function computes the master key using the master password and device secret.
    It uses the PBKDF2 key derivation function from the Crypto library to generate a
    32-byte key from the provided password and salt (device secret).
    """
    password = mp.encode() # Convert master password to bytes
    salt = ds.encode() # Convert device secret to bytes
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512) # Generate key using PBKDF2
    return key

def addEntry(mp, ds, sitename, siteurl, email, username):
    """
    This function adds an entry to the password manager database.
    It prompts the user for the password, computes the master key using
    the provided master password and device secret, encrypts the password
    using the master key, and adds the encrypted entry to the database.
    """
    # get the password
    password = getpass("password: ")
	
    # compute master key
    mk=computeMasterkey(mp, ds)
	
    # encrypt password with mk
    encrypted = utils.aesutil.encrypt(key=mk, source=password, keyType="bytes")
	
    # Add to db
    db = dbconfig() # Connect to the database
    cursor = db.cursor() # Create a cursor object
    query = "INSERT INTO pm.entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)"
    val = (sitename,siteurl,email,username,encrypted)
    cursor.execute(query, val) # Execute the query with the provided values
    db.commit() # Commit the changes to the database

    printc("[green][+][/green] Added entry ") addEntry function prints a message to the console indicating that the entry has been successfully added to the password manager database. The message is printed using the printc function with ANSI escape codes for formatting the text with green color and a plus sign symbol. The message is enclosed in square brackets to highlight it and make it stand out from other messages.
