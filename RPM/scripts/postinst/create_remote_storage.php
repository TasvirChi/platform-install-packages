<?php

if (count($argv)<11){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <minus_2_admin_secret> <profile name> <delivery url> <storage host> <storage basedir> <remote storage username> <remote storage passwd> 
 <remote storage proto: FTP|SFTP|SCP|S3>
 <playback proto: APPLE_HTTP|HDS|RTMP|HTTP|AKAMAI_HD|AKAMAI_HDS>
 <delivery proto: APPLE_HTTP|HDS|HTTP|RTMP|AKAMAI_HD|AKAMAI_HDS|AKAMAI_HLS_DIRECT|AKAMAI_HLS_MANIFEST>'."\n";
    exit (1);
}
require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');

$protocols['FTP'] = BorhanStorageProfileProtocol::FTP;
$protocols['SFTP'] = BorhanStorageProfileProtocol::SFTP;
$protocols['SCP'] = BorhanStorageProfileProtocol::SCP;
$protocols['S3'] = BorhanStorageProfileProtocol::S3;


$deliveries['APPLE_HTTP'] = BorhanDeliveryProfileType::APPLE_HTTP; 
$deliveries['HDS'] = BorhanDeliveryProfileType::HDS;
$deliveries['HTTP'] = BorhanDeliveryProfileType::HTTP;
$deliveries['RTMP'] = BorhanDeliveryProfileType::RTMP;
$deliveries['AKAMAI_HD'] = BorhanDeliveryProfileType::AKAMAI_HD;
$deliveries['AKAMAI_HDS'] = BorhanDeliveryProfileType::AKAMAI_HDS;
$deliveries['AKAMAI_HLS_DIRECT'] = BorhanDeliveryProfileType::AKAMAI_HLS_DIRECT;
$deliveries['AKAMAI_HLS_MANIFEST'] = BorhanDeliveryProfileType::AKAMAI_HLS_MANIFEST;
$deliveries['AKAMAI_HLS_DIRECT'] = BorhanDeliveryProfileType::AKAMAI_HLS_DIRECT;
$deliveries['AKAMAI_HLS_MANIFEST'] = BorhanDeliveryProfileType::AKAMAI_HLS_MANIFEST;
$deliveries['AKAMAI_HD'] = BorhanDeliveryProfileType::AKAMAI_HD;
$deliveries['AKAMAI_HDS'] = BorhanDeliveryProfileType::AKAMAI_HDS;
$deliveries['AKAMAI_HTTP'] = BorhanDeliveryProfileType::AKAMAI_HTTP;
$deliveries['AKAMAI_RTMP'] = BorhanDeliveryProfileType::AKAMAI_RTMP;

$playbacks['APPLE_HTTP'] = BorhanPlaybackProtocol::APPLE_HTTP;
$playbacks['HDS'] = BorhanPlaybackProtocol::HDS;
$playbacks['RTMP'] = BorhanPlaybackProtocol::RTMP;
$playbacks['HTTP'] = BorhanPlaybackProtocol::HTTP;
$playbacks['AKAMAI_HD'] = BorhanPlaybackProtocol::AKAMAI_HD;
$playbacks['AKAMAI_HDS'] = BorhanPlaybackProtocol::AKAMAI_HDS;
         
$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$profile_name=$argv[4];
$delivery_url=$argv[5];
$storage_host=$argv[6];
$storage_basedir=$argv[7];
$storage_user=$argv[8];
$storage_passwd=$argv[9];
$basedir=dirname(__FILE__);
$storage_protocol=$argv[10];
$playback_protocol=$argv[11];

try{
	$config = new BorhanConfiguration($partnerId);
	$config->serviceUrl = $service_url;  
	$client = new BorhanClient($config);
	$ks = $client->session->start($secret, null, BorhanSessionType::ADMIN, -2, null,null);
	$client->setKs($ks);
	$config->partnerId=$partnerId;
	$client->setPartnerId($partnerId);
	$delivery = new BorhanDeliveryProfile();
	$delivery->name = $profile_name;
	$delivery->status = BorhanDeliveryStatus::ACTIVE;
	$delivery->type = BorhanDeliveryProfileType::HTTP;
	$delivery->streamerType = BorhanPlaybackProtocol::HTTP;
	$delivery->systemName = $profile_name;
	$delivery->url = $delivery_url;
	//$delivery->isDefault = BorhanNullableBoolean::FALSE_VALUE;
	$delivery_obj=$client->deliveryProfile->add($delivery);
	if ($protocols[$storage_protocol] === 'S3'){
		$storageProfile = new BorhanAmazonS3StorageProfile();
		$storageProfile->filesPermissionInS3 = BorhanAmazonS3StorageProfileFilesPermissionLevel::ACL_PUBLIC_READ;
	}else{
		$storageProfile = new BorhanStorageProfile();
	}

	$storageProfile->name = $profile_name;
	$storageProfile->systemName = $profile_name;
	$storageProfile->status = BorhanStorageProfileStatus::AUTOMATIC;
	$storageProfile->protocol = $protocols[$storage_protocol];
	$storageProfile->storageUrl = $storage_host;
	$storageProfile->storageBaseDir = $storage_basedir;
	$storageProfile->storageUsername = $storage_user;
	$storageProfile->storagePassword = $storage_passwd;
	$storageProfile->deliveryProfileIds = array();
	$storageProfile->deliveryProfileIds[0] = new BorhanKeyValue();
	$storageProfile->deliveryProfileIds[0]->key = $playback_protocol;
	$storageProfile->deliveryProfileIds[0]->value = $delivery_obj->id;
	$result = $client->storageProfile->add($storageProfile);
	return($result);
}catch(exception $e){
	var_dump($e);
}
