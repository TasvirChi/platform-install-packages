<?php
if (count($argv)<4){
        echo 'Usage:' .__FILE__ .' <service_url> <partner_id> <secret> <player_ver> </path/to/xml>'."\n";
        exit (1); 
}

require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$secret = $argv[3];
$type = BorhanSessionType::ADMIN;
$partnerId=$argv[2];
$config = new BorhanConfiguration($partnerId);
$config->serviceUrl = $argv[1];
$player_ver=$argv[4];
$client = new BorhanClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
$uiConf = new BorhanUiConf();
$uiConf->name = 'Sanity player';
$uiConf->description = "Test player creation via API";
$uiConf->objType = 1; 
$uiConf->width = 533; 
$uiConf->height = 300; 
$uiConf->htmlParams = '';
$uiConf->swfUrl = "/flash/bdp3/v$player_ver/bdp3.swf";
$uiConf->confFile = file_get_contents($argv[5]);
$uiConf->creationMode=3;
$uiConf->useCdn = '1';
$uiConf->swfUrlVersion = $player_ver;
$results = $client->uiConf->add($uiConf);
echo "Generated UI conf id : ".$results->id ."\n";
?>
