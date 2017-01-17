<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <user secret> <service_url> <search string> '."\n");
}
require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = BorhanSessionType::USER;
$config = new BorhanConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$search_string=$argv[4];
$client = new BorhanClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

$filter = new BorhanBaseEntryFilter();
$filter->searchTextMatchOr = $search_string;
$pager = null;
$result = $client->baseEntry->listAction($filter, $pager);
echo "The string '$search_string' was found in the tags of these entries:
===================================================================================================================================
";
foreach($result->objects as $entry){
	echo "Entry ID: " . $entry->id."\nName: ". $entry->name."\nDescription: ".$entry->description."\nTags: ".$entry->tags."\n\n\n";
}

$entryFilter = new BorhanBaseEntryFilter();
$entryFilter->advancedSearch = new BorhanCategoryEntryAdvancedFilter();
$captionAssetItemFilter = new BorhanCaptionAssetItemFilter();
$captionAssetItemFilter->contentMultiLikeOr = $search_string;
$captionAssetItemPager = null;
$captionsearchPlugin = BorhanCaptionsearchClientPlugin::get($client);
$result = $captionsearchPlugin->captionAssetItem->searchEntries($entryFilter, $captionAssetItemFilter, $captionAssetItemPager);
echo "The string '$search_string' was also found is caption assets of these entries:
==============================================================================================================================
";
foreach($result->objects as $entry){
	$filter = new BorhanAssetFilter();
	$filter->advancedSearch = new BorhanEntryCaptionAssetSearchItem();
	$filter->entryIdEqual = $entry->id;
	$pager = null;
	$captionPlugin = BorhanCaptionClientPlugin::get($client);
	$result = $captionPlugin->captionAsset->listAction($filter, $pager);
	$storageId = null;
	$url = $captionPlugin->captionAsset->geturl($result->objects[0]->id, $storageId);
	echo "Entry ID: " . $entry->id."\nName: ". $entry->name."\nDescription: ".$entry->description."\nCaption file URL: $url\n\n\n";
}
?>
