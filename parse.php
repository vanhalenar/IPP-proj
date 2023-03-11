<?php
ini_set('display_errors', 'stderr');

$doc = new DOMDocument('1.0', 'UTF-8');

$doc->formatOutput = true;

$order = 0;

$header = false;

$program = $doc->appendChild($doc->createElement('program'));
$program->setAttribute("language", "IPPcode23");

if (count($argv)>1){

    if (count($argv)!=2){
        exit(10);
    }

    if ($argv[1] == "--help"){
        
        echo("***********************\n");
        echo("*******parse.php*******\n");
        echo("***********************\n");
        echo("description: reads IPPcode23 source from STDIN, performs lexical and syntactic checks and outputs XML representation to STDOUT.\n");
        echo("usage: php parse.php <inputfile.ipp23\n");
        echo("***********************\n");


        exit(0);
    }
    else{
        exit(10);
    }
}

//parses line to XML and adds it to the main document
function line_to_xml($line, $program, $doc, $order){
    $newline = $program->appendChild($doc->createElement('instruction'));
    $newline->setAttribute("order", $order);
    $newline->setAttribute("opcode", strtoupper($line[0]));
    if (count($line)==1){
        return;
    }
    if(count($line)>=2){
        $type_value = determine_arg_type($line[1]);
        $arg1 = $newline->appendChild($doc->createElement('arg1', htmlspecialchars(rtrim($type_value[1]))));
        $arg1->setAttribute('type', $type_value[0]);
    }
    if(count($line)>=3){
        $type_value = determine_arg_type($line[2]);
        $arg1 = $newline->appendChild($doc->createElement('arg2', htmlspecialchars(rtrim($type_value[1]))));
        $arg1->setAttribute('type', $type_value[0]);
    }
    if(count($line)==4){
        $type_value = determine_arg_type($line[3]);
        $arg1 = $newline->appendChild($doc->createElement('arg3', htmlspecialchars(rtrim($type_value[1]))));
        $arg1->setAttribute('type', $type_value[0]);
    }
}

//compares argument with expected type using determine_arg_type() function
function check_arg($arg, $type){
    $type_value = determine_arg_type($arg);
    if ($type_value[0]==$type){
        return 0;
    }
    else{
        return 1;
    }
}

//checks, whether argument is in <symb> category
function check_symb($arg){
    if (check_arg($arg, "var") == 1){
        if (check_arg($arg, "bool") == 1){
            if (check_arg($arg, "string") == 1){
                if (check_arg($arg, "int") == 1){
                    if (check_arg($arg, "nil") == 1){
                        exit(23);
                    }
                }
            }
        }
    }
}

//checks, whether argument is <var>
function check_var($arg){
    if (check_arg($arg, "var") == 1){
        exit(23);
    }
}

//checks, whether argument is <label>
function check_label($arg){
    if (check_arg($arg, "label") == 1){
        exit(23);
    }
}

//checks, whether argument is <type>
function check_type($arg){
    if ($arg != "string"){
        if ($arg != "int"){
            if ($arg != "bool"){
                exit(23);
            }
        }
    }
}

//determines argument type and parses argument
//return: $type_value[] array containing argument type and parsed argument itself
function determine_arg_type($arg){
    $type_value = [];
    if (preg_match("/^GF@|LF@|TF@/", $arg)){
        $type_value[0] = "var";
        $type_value[1] = $arg;
        if (!preg_match("/(LF@|GF@|TF@)[a-zA-Z_\-$&%*!?]+.*/", $arg)){
            exit(23);
        }

        return $type_value;
    }
    elseif (preg_match("/^int@/", $arg)){
        $type_value[0] = "int";
        preg_match("/(?<=@).*/", $arg, $match);
        $type_value[1] = $match[0];
        return $type_value;
    }
    elseif (preg_match("/^string@/", $arg)){
        $type_value[0] = "string";
        preg_match("/(?<=@).*/", $arg, $match);
        $type_value[1] = $match[0];
        if (preg_match("/\\\\\d{0,2}(?!\d)/", $type_value[1])){
            exit(23);
        }
        return $type_value;
    }
    elseif (preg_match("/^bool@/", $arg)){
        $type_value[0] = "bool";
        preg_match("/(?<=@).*/", $arg, $match);
        $bool_array = ["true", "false"];
        if (!in_array($match[0], $bool_array)){
            exit(23);
        }
        $type_value[1] = $match[0];
        return $type_value;
    }
    elseif (preg_match("/^nil@/", $arg)){
        $type_value[0] = "nil";
        if (!preg_match("/(?<=@)nil$/", $arg, $match)){
            exit(23);
        }
        $type_value[1] = $match[0];
        return $type_value;
    }
    else{
        $type_value[0] = "label";
        $type_value[1] = $arg;
        if (!preg_match("/^[a-zA-Z_\-$&%*!?]+.*/", $arg)){
            exit(23);
        }
        return $type_value;
    }
}

//main loop for reading input
while ($f = fgets(STDIN)){
    
    //remove comments
    $f = preg_replace("/#.*/", '', $f);

    //check for empty lines
    if (preg_match("/^\s*$/", $f)){
        continue;
    }

    $f = rtrim($f);
    $f = trim(preg_replace('/\s\s+/', ' ', str_replace("\n", " ", $f)));
    $array = explode(' ', $f);

    //check for header
    if ($header == false){
        if (strcmp($array[0], ".IPPcode23") == 0){
            $header = true;
            continue;
        }
        else{
            exit(21);
        }
    }
    
    switch(strtoupper($array[0])){
        //no args
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=1){
                exit(23);
            }
            break;
        //<var>
        case "DEFVAR":
        case "POPS":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            
            if (count($array)!=2){
                exit(23);
            }

            check_var($array[1]);

            break;
        //<var><symb>
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
        case "NOT":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=3){
                exit(23);
            }

            check_var($array[1]);
            
            check_symb($array[2]);
            
            break;
        //<label>
        case "CALL":
        case "LABEL":
        case "JUMP":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=2){
                exit(23);
            }

            check_label($array[1]);
            
            break;
        //<symb>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=2){
                exit(23);
            }
            check_symb($array[1]);
            break;
        //<var><symb1><symb2>
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=4){
                exit(23);
            }
            check_var($array[1]);

            check_symb($array[2]);

            check_symb($array[3]);
            
            break;
        //<var><type>
        case "READ":
            $order++;
            if (count($array)!=3){
                exit(23);
            }

            check_var($array[1]);

            check_type($array[2]);
            /*
            if ($array[2] != "string"){
                if ($array[2] != "int"){
                    if ($array[2] != "bool"){
                        exit(23);
                    }
                }
            }
            */
            $newline = $program->appendChild($doc->createElement('instruction'));
            $newline->setAttribute("order", $order);
            $newline->setAttribute("opcode", $array[0]);
            $type_value = determine_arg_type($array[1]);
            $arg1 = $newline->appendChild($doc->createElement('arg1', rtrim($type_value[1])));
            $arg1->setAttribute('type', $type_value[0]);
            $arg2 = $newline->appendChild($doc->createElement('arg2', $array[2]));
            $arg2->setAttribute('type', 'type');
            break;
        //<label><symb1><symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            $order++;
            line_to_xml($array, $program, $doc, $order);
            if (count($array)!=4){
                exit(23);
            }

            check_label($array[1]);
            
            check_symb($array[2]);

            check_symb($array[3]);
            
            break;
        default:
            //comment
            if (preg_match("/#/", $array[0])){
                break;
            }
            else{
                exit(22);
            }
    }
}

//print final XML document
echo $doc->saveXML();

?>