<?php
$servername = "us-cdbr-east-06.cleardb.net";
$username = "b19dfc7a972b92";
$password = "5af8fdbd";
$dbname = "heroku_a0c3ccec1186e2e";


// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
  die("Connection failed: " . mysqli_connect_error());
}
echo "Connected successfully";

$sql = "SELECT * FROM access";
$result = mysqLi_query($conn, $sql)

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Admin Page</title>
</head>
<body>  
    <h1>Access Info</h1>
    <div class="page-container">
        <div class="search-area">
            <form action="">
                <p>Search for Student or Staff</p>
                <label for="search-bar">Enter student or staff id/name</label>
                <input type="text" id="search-bar">
            </form>
        </div>
            <div class="table-div">
                <table class="main-table">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Access time</th>
                        <th>Access day</th>
                    </tr>
                    <tr>
                        <td>test</td>
                </tr>
                </table>
            </div>
    </div>
</body>
</html>
<?php
echo "testing";
