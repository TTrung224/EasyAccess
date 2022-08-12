<?php
@include 'config.php';

session_start();
if(isset($_SESSION['logedIn'])){
   header('location:index.php');
}

if(isset($_POST['submit'])){
   $email = mysqli_real_escape_string($conn, $_POST['email']);
   $pass = $_POST['password'];

   $select = "SELECT * FROM acc WHERE email = '$email'";

   $result = mysqli_query($conn, $select);

   if(mysqli_num_rows($result) > 0){
      $row = mysqli_fetch_array($result);

      if(password_verify($pass, $row['password'])){
         $_SESSION['logedIn'] = true;
         header('location: index.php');
      }else{
         $error[] = 'incorrect email or password!';
      }
   }else{
      $error[] = 'incorrect email or password!';
   }
};
?>

<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>login form</title>

   <!-- custom css file link  -->
   <link rel="stylesheet" href="style.css">
</head>
<body>
   <div class="form-container">
      <form action="login_form.php" method="post">
         <h3>login now</h3>
         <?php
         if(isset($error)){
            foreach($error as $error){
               echo '<span class="error-msg">'.$error.'</span>';
            };
         };
         ?>
         <input type="email" name="email" required placeholder="enter your email">
         <input type="password" name="password" required placeholder="enter your password">
         <input type="submit" name="submit" value="login now" class="form-btn">
         <!-- <p>don't have an account? <a href="register_form.php">register now</a></p> -->
      </form>
   </div>
</body>
</html>