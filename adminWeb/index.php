<?php
@include 'config.php';

session_start();
if(!isset($_SESSION['logedIn'])){
    header('location:login_form.php');
}

//Pagination
if(isset($_GET['page'])){
    $page = $_GET['page'];
}else{
    $page = 1;
}

$num_per_page = 10;
$start_from = ($page -1) * 10;

$sql = "SELECT * FROM access a ";

if(isset($_GET['id']) or isset($_GET['startTime']) or isset($_GET['endTime'])){
    $filters = [];
        if($_GET['id'] != ""){
            $id = $_GET['id'];
            array_push($filters, "a.personId like '$id' ");
        }

        if($_GET['startTime'] != "" && $_GET['endTime'] != ""){
            $startTime = str_replace("T", " ", $_GET['startTime']) . ":00";
            $endTime = str_replace("T", " ", $_GET['endTime']) . ":59";
            array_push($filters,"a.dateTime >= '$startTime' and a.dateTime <= '$endTime' " );
        }


    if(sizeof($filters)>0){
        $sql = $sql . "where ";
        for ($i = 0 ; $i < sizeof($filters); $i++){
            $sql = $sql . $filters[$i] ;
            if($i != sizeof($filters) - 1){
                $sql = $sql . "and ";
            }
        }
    }
}

$result = mysqLi_query($conn, $sql);
$nr = mysqLi_num_rows($result); 
$total_page = ceil($nr/$num_per_page);

$sql = $sql . "ORDER BY dateTime DESC limit $start_from, $num_per_page";
$result = mysqLi_query($conn, $sql);

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
    <a id="logout-btn" href="logout.php">Logout</a>
    
    <div class="page-container">

        <div class="search-area">
            <form action="index.php" method="get" >
                <p>Filter access data:</p>
                <label for="search-bar">Enter student or staff id:</label>
                <input type="text" id="search-bar" name="id"
                value = "<?= (isset($_GET['id'])) ? $_GET['id'] : ""?>"
                >
                <label for="start-time-range">Start date-time:</label>
                <input type="datetime-local" id="start-time-range" name="startTime"
                value = "<?= (isset($_GET['startTime'])) ? $_GET['startTime'] : ""?>"
                >
                <label for="end-time-range">End date-time:</label>
                <input type="datetime-local" id="end-time-range" name="endTime"
                value = "<?= (isset($_GET['endTime'])) ? $_GET['endTime'] : ""?>"
                >
                <input type="submit" name="filter" class="filter-btn" value="Filter">
                <button class="cancel-btn"><a class="cancel-btn" href="index.php" >Cancel</a></button>
            </form>
            <?php

            ?>
        </div>

        <div class="table-div">
            <table class="main-table">
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Access time</th>
                </tr>
                <?php
                if(mysqLi_num_rows($result) >0){

                    while($row = mysqli_fetch_array($result)){
                        echo "<tr> <td>". $row['personId']."</td>";
                        echo "<td>". $row['name']."</td>";
                        echo "<td>". $row['dateTime']."</td> </tr>";
                    }
                }
                ?>
            </table>

            <div class="page">

            <?php for($i=1;$i<= $total_page;$i++){
                if(isset($_GET['id']) or isset($_GET['startTime']) or isset($_GET['endTime'])){?>

                <form action="index.php" method="get">
                    <input type="hidden" name="id" value=<?=$_GET['id']?>>
                    <input type="hidden" name="startTime" value=<?=$_GET['startTime']?>>
                    <input type="hidden" name="endTime" value=<?=$_GET['endTime']?>>
                    <input type="submit" name="page" value="<?=$i?>" class ="page-btn">
                </form>

                <?php } else{
                    echo "<a href='index.php?page=".$i."' class='page-btn'>$i</a>";
                }
            }?>

            </div>
        </div>
    </div>
</body>
</html>