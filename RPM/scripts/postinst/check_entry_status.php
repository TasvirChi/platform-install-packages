<?php
if (count($argv)<3){
        echo 'Usage:' .__FILE__ .' <service_url> <partner_id> <secret> <entry_id>'."\n";
        exit (1); 
}

require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$secret = $argv[3];
$type = BorhanSessionType::USER;
$partnerId=$argv[2];
$config = new BorhanConfiguration($partnerId);
$config->serviceUrl = $argv[1];
$entryId = $argv[4];
$client = new BorhanClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
$version = null;
$result = $client->baseEntry->get($entryId, $version);
exit($result->status);
?>
