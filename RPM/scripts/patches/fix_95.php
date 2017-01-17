<?php
if (count($argv)<4){
        echo 'Usage:' .__FILE__ .' <service_url> <partner_id> <secret> </path/to/xml>'."\n";
	echo "for getting your partner ID admin_secret run:\nselect admin_secret,status from borhan.partner where id=\$YOUR_ID;\n\n";
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
$client = new BorhanClient($config);
$uiConf = null;
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
$uiConf = new BorhanUiConf();
$uiConf->name = 'Share target';
$uiConf->description = "Share target";
$uiConf->objType = 8; 
$uiConf->width = 533; 
$uiConf->height = 300; 
$uiConf->htmlParams = '';
$uiConf->swfUrl = '/flash/bdp3/v3.9.8/bdp3.swf';
$uiConf->confFile = file_get_contents($argv[4]);
$uiConf->creationMode=3;
$uiConf->useCdn = '1';
$uiConf->swfUrlVersion = '3.9.8';
$results = $client->uiConf->add($uiConf);
echo "Your new UI conf ID is ".$results->id."\nConnect to your DB and run: update borhan.ui_conf set id=8700151 where id=".$results->id." limit 1;\n";
