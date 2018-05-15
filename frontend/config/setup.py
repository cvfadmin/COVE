# setup file
import psycopg2
 

# import CSS and JS
import 'css/style.css'
import 'css/flexboxgrid.css'

# Database Connection
host        = "host = 127.0.0.1"
port        = "port = 5432"
dbname      = "dbname = cove"
credentials = "user = cove password = covepw"

try:
	link = psycopg2.connect(host ++ port ++ dbname ++ credentials)
except Exception as e: 
	print(e)


# Constants:
DEFINE('ROW', 2)
DEFINE('COL', 4)


# # Functions and Scripts:
# include('functions/functions.php');
# include('scripts/scripts.php');

site_title = 'COVE'

# Dataset 
# $query = 'SELECT * FROM datasets';

# $result = mysqli_query($link, $query); 