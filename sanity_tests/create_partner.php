<?php
if (count($argv)<4){
    echo __FILE__ . ' <admin_secret> <partner email> <partner passwd> <service_url> '."\n";
    exit (1);
}
require_once('create_session.php');
$admin_partner_id = -2;
$config = new BorhanConfiguration($admin_partner_id);
$config->serviceUrl = $argv[4];
$client = new BorhanClient($config);
$expiry = null;
$privileges = null;
$email=$argv[2];
$name='Linux Rules';
$cmsPassword=$argv[3];
$secret = $argv[1];
        $userId = null;
        $type = BorhanSessionType::ADMIN;
        $ks = $client->session->start($secret, $userId, $type, $admin_partner_id, $expiry, $privileges);
        $client->setKs($ks);
        $partner = new BorhanPartner();
        $partner->website="http://www.borhan.com";
        $partner->adminName=$name;
        $partner->name=$name;
        $partner->description=" "; //cannot be empty or null
        $partner->adminEmail=$email;
        $results = $client->partner->register($partner, $cmsPassword);
	echo($results->id);
?>
