<?php
	extract($_POST);
	$myfile = fopen("testfile.c", "w") or die("Unable to open the file!");
	fwrite($myfile, $code);

	$myfile1 = fopen("flags.json", "w") or die("Unable to open the file!");
	fwrite($myfile1, $menu_opt_json_str);

	$output = null;

	$shell_command = "sh ../env/Coptimizer_script testfile.c";
	exec(escapeshellcmd($shell_command));

	$op = file_get_contents("../env/output.c");
	$inp_json = file_get_contents("../env/check_input.txt");
	$ret_array = array("op" => $op, "inp_json" => $inp_json);

	fclose($myfile);
	fclose($myfile1);

  echo json_encode($ret_array);
?>
