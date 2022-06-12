<?php 

$in_array = array(1, 2, 3);
$in_values = implode(',', $in_array)
$donne = $dbh->prepare("SELECT donne, valeur, time FROM data IN(".$in_values.")");
$donne->execute();
$donne = $donne->fetchAll()
print_r($donne);
print("\n");
?>
