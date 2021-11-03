<html>
<head>
<link rel="stylesheet" href="http://127.0.0.1/XSStrike-extension/src/xss_php.css"/>
</head>
<body>
<div align="center"><img src="./icons/logo-128.png"></div>
<div class='tagline'><h5>Browser Extension For Finding XSS<h5></div></div>
<h4>Have Issues?: <a href='https://github.com/tauh33dkhan/XSStrike-extension' target='_blank'>Report</a></h4>
<svg height="8" width="100%"><line x1="100%" y1="0" x2="0" y2="0" style="stroke:rgb(47,79,79);stroke-width:8" /> </svg>

<?php
$target = $_REQUEST[ 'target' ];
$skipDom = $_REQUEST[ 'skipDom' ];
$op = $_REQUEST[ 'op' ];
$raw_cookie = $_REQUEST['cookie'];
$url = '"' . $target . '"';
$c = '"' . $raw_cookie .'"';
$sucess = '"<h1><span class=&#x22;GreenDisplay&#x22;>3092</span></h2>"';
if ($skipDom == "yes") {
  $domArg = "--skip-dom";
 }
else{
  $domArg = "";
}

if ($op == "crawl"){
  $command = 'python3 -u ./XSStrike/xsstrike.py ' . $domArg . ' --crawl --level 10 --threads 10 -u' . $url . ' --headers ' . $c;
 }
else {
  $command = 'python3 -u ./XSStrike/xsstrike.py ' . $domArg . ' --threads 10 -u ' . $url .' --headers ' . $c;
}

// Debug: echo $command;
if (filter_var($target, FILTER_VALIDATE_URL)) {
  echo "<h3 align='center'>Scan Report for " . $target ."</h3>";
  echo "<pre>";
  $result = liveExecuteCommand($command);
  if($result['exit_status'] === 0){
           // do something if command execution succeeds
    echo "</pre>";
    echo '<footer><h2 align="center">Scan Completed!</h2>';

  } else {
          // do something on failure
    echo '<footer><h2>Scan Failed!</h2>';

  }
  echo "</pre>";
  echo '<svg height="20" width="100%"><line x1="100%" y1="0" x2="0" y2="0" style="stroke:rgb(47,79,79);stroke-width:8" /> </svg>';
  echo '<div class="footer"></br></br> </div></footer>';
}
else {
  echo "<h2 align='center'>Invalid URL!</h2>";
}

function liveExecuteCommand($cmd)
{

    while (@ ob_end_flush()); // end all output buffers if any

    $proc = popen("$cmd 2>&1", 'r');

    $live_output     = "";
    $complete_output = "";

    while (!feof($proc))
    {
        $live_output     = fread($proc, 4096);
        $complete_output = $complete_output . $live_output;
        echo "$live_output";
        @ flush();
    }

    pclose($proc);

    // get exit status
    preg_match('/[0-9]+$/', $complete_output, $matches);

    // return exit status and intended output
    return array (
                    'exit_status'  => intval($matches[0]),
                    'output'       => str_replace("Exit status : " . $matches[0], '', $complete_output)
                 );
}


?>

</body>
</html>
