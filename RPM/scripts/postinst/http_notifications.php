<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url>'."\n");
}
require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = BorhanSessionType::ADMIN;
$config = new BorhanConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$client = new BorhanClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

// list available HTTP templates:
$filter = new BorhanEventNotificationTemplateFilter();
$filter->systemNameEqual = 'HTTP_ENTRY_STATUS_CHANGED';
$pager = null;
$eventNotificationTemplate = new BorhanHttpNotificationTemplate();
$eventnotificationPlugin = BorhanEventnotificationClientPlugin::get($client);
$notification_templates = $eventnotificationPlugin->eventNotificationTemplate->listTemplates($filter, $pager);
// id for entry change:
if (isset($notification_templates->objects[0]->id)){
	$template_id=$notification_templates->objects[0]->id;
}else{
	die("\nNo HTTP templates exist.\n Try running:\nphp /opt/borhan/app/tests/standAloneClient/exec.php /opt/borhan/app/tests/standAloneClient/httpNotificationsTemplate.xml /tmp/out.xml\nPassing -2 as partner ID");
}

// clone the template to partner:
$result = $eventnotificationPlugin->eventNotificationTemplate->cloneAction($template_id, $eventNotificationTemplate);
$notification_id = $result->id;

// activate template
$status = BorhanEventNotificationTemplateStatus::ACTIVE;
$eventnotificationPlugin = BorhanEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->updateStatus($notification_id, $status);

// update url:
$eventNotificationTemplate->type = BorhanEventNotificationTemplateType::HTTP;
$eventNotificationTemplate->eventType = BorhanEventNotificationEventType::BATCH_JOB_STATUS;
$eventNotificationTemplate->eventObjectType = BorhanEventNotificationEventObjectType::ENTRY;
$eventNotificationTemplate->contentParameters = array();
$eventNotificationTemplate->contentParameters[0] = new BorhanEventNotificationParameter();
$eventNotificationTemplate->contentParameters[1] = new BorhanEventNotificationParameter();
$eventNotificationTemplate->contentParameters[2] = null;
$eventNotificationTemplate->contentParameters[3] = null;
$eventNotificationTemplate->url = 'http://localhost/1.php';
$BorhanHttpNotificationDataFields=new BorhanHttpNotificationDataFields();
$eventNotificationTemplate->data = $BorhanHttpNotificationDataFields;
$eventnotificationPlugin = BorhanEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->update($notification_id, $eventNotificationTemplate);
$eventnotificationPlugin->eventNotificationTemplate->delete($notification_id);
echo('ID: '. $result->id. ', URL: '.$result->url);
?>
