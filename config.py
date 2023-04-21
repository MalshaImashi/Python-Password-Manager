from utils.dbconfig import dbconfig # Import the dbconfig module from the utils package

from rich import print as printc # Import the print function from the rich package and assign it an alias
from rich.console import Console # Import the Console class from the rich.console module

console = Console() # Create an instance of the Console class to display exceptions

def generateDeviceSecret(length=10): # Define a function to generate a random device secret
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

def config(): # Define the main function that sets up the database and configuration data
    
    # Create database
    db = dbconfig() # Create a database connection using the dbconfig function
    cursor = db.cursor() # Create a cursor object to execute SQL statements on the database
    
    try:
        cursor.execute("CREATE DATABASE pm") # Try to create a new database called 'pm'
    except Exception as e:
        # If the database already exists, print an error message and exit the program
        printc("[red][!] An error occurred while trying to create db. Check if database with name 'pm' already exists - if it does, delete it and try again.")
        console.print_exception(show_locals=True)
        sys.exit(0)

    printc("[green][+][/green] Database 'pm' created") # If the database is created successfully, print a success message to the console
  
    # Create tables
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)" # Define an SQL statement to create the 'secrets' table
    res = cursor.execute(query) # Execute the SQL statement
    printc("[green][+][/green] Table 'secrets' created ") # If the table is created successfully, print a success message to the console

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)" # Define an SQL statement to create the 'entries' table
    res = cursor.execute(query) # Execute the SQL statement
    printc("[green][+][/green] Table 'entries' created ") # If the table is created successfully, print a success message to the console
  
    mp = "" # Initialize an empty string to hold the user's master password
    printc("[green][+] A [bold]MASTER PASSWORD[/bold] is the only password you will need to remember in-order to access all your other passwords. Choosing a strong [bold]MASTER PASSWORD[/bold] is essential because all your other passwords will be [bold]encrypted[/bold] with a key that is derived from your [bold]MASTER PASSWORD[/bold]. Therefore, please choose a strong one that has upper and lower case characters, numbers and also special characters. Remember your [bold]MASTER PASSWORD[/bold] because it won't be stored anywhere by this program, and you also cannot change it once chosen. [/green]\n")
    
    while 1:
        mp = getpass("Choose a MASTER PASSWORD: ") # Prompt the user to choose a master password
        if mp == getpass("Re-type: ") and mp!="": # Confirm the master password
            break # If the passwords match, break out of the loop
        printc("[yellow][-] Please try again.[/yellow]") # If the passwords do not match, print an error message and try again

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest() # Hash the master password using SHA256 and store
    printc("[green][+][/green] Generated hash of MASTER PASSWORD") # Print a message indicating that the hash of the user's master password has been generated

    ds = generateDeviceSecret() # Generate a random device secret using the `generateDeviceSecret()` function that we defined earlier

   printc("[green][+][/green] Device Secret generated") # Print a message indicating that the device secret has been generated

   query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s, %s)" # Create an SQL query to insert the user's hashed master password and the device secret into the `secrets` table in the `pm` database

   cursor.execute(query, val) # Execute the SQL query that we just created and pass in the `val` tuple containing the hashed master password and the device secret

   db.commit() # Commit the changes to the database

  printc("[green][+][/green] Added to the database") # Print a message indicating that the master password and device secret have been added to the database

    printc("[green][+] Configuration done![/green]") # Print a message indicating that the configuration is complete

db.close() # Close the connection to the database


