<?php
  extract($_POST);
  $myfile = fopen("inp.txt", "w") or die("Unable to open the file : 'inp' !");
  fwrite($myfile, $inp_code);

  // $shell_command = "/usr/local/bin/python3.x ../tester/tester_controller.py testfile.c output.c > met_op.txt"; // => macos 10+
  $shell_command = "python3 ../tester/tester_controller.py testfile.c output.c > met_op.txt"; // => linux
  shell_exec($shell_command);

  $unop = file_get_contents("unop_output.txt");
  $op = file_get_contents("op_output.txt");
  $met = file_get_contents("met_op.txt");
  $ret_array = array("unop_output" => $unop, "op_output" => $op, "met_op" => $met);

  fclose($myfile);

  echo json_encode($ret_array);
 ?>
