<?php
require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');
function generate_ks($service_url,$partnerId,$secret,$type=BorhanSessionType::ADMIN,$userId=null,$expiry = null,$privileges = null)
{
    $config = new BorhanConfiguration($partnerId);
    $config->serviceUrl = $service_url;  
    $client = new BorhanClient($config);
    $ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
    $client->setKs($ks);
    return ($client);
}
?>
