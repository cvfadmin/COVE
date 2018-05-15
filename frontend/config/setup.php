<?php
// Setup File 

# include CSS and JS

include('css/style.css');
include('css/flexboxgrid.css');


# Database Connection
$host        = "host = 127.0.0.1";
$port        = "port = 5432";
$dbname      = "dbname = cove";
$credentials = "user = cove password = covepw";

$link = pg_connect( "$host $port $dbname $credentials") OR die('Error: '.pg_last_error());


# Constants:
DEFINE('ROW', 2);
DEFINE('COL', 4);
/*

# Functions and Scripts:
include('functions/functions.php');
include('scripts/scripts.php');

$site_title = 'COVE';

# Dataset 
$query = 'SELECT * FROM datasets';

$result = mysqli_query($link, $query); */

?>