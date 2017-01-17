<?php
$config = null;
$clientConfig = null;
/* @var $clientConfig BorhanConfiguration */
$client = null;
/* @var $client BorhanClient */

require_once __DIR__ . '/init.php';


/**
 * Start a new session
 */
$adminSecretForSigning = $config['adminConsoleSession']['adminConsoleSecret'];
$client->setKs($client->generateSessionV2($adminSecretForSigning, null, BorhanSessionType::ADMIN, -2, 86400, ''));


$partnerId = $config['session']['partnerId'];
/**
 * Delete the partner
 */
$systemPartnerClient = BorhanSystemPartnerClientPlugin::get($client);
$systemPartnerClient->systemPartner->updateStatus($partnerId, BorhanPartnerStatus::FULL_BLOCK,'Test partner');
//if ($systemPartnerClient->systemPartner->updateStatus($partnerId, BorhanPartnerStatus::FULL_BLOCK,'Test partner')){
echo "Partner [$partnerId] deleted\n";

