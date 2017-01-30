<?php
if($argc<6){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url> <start date i.e "01 Jul 2015"> <end date i.e "10 Jul 2015">'."\n");
}
require_once('/opt/borhan/web/content/clientlibs/php5/BorhanClient.php');

// generate a KS
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = BorhanSessionType::ADMIN;
$config = new BorhanConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$start_date=date_format(date_create($argv[4]), 'U');
$end_date=date_format(date_create($argv[5]), 'U');
$client = new BorhanClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

// set type to TOP_CONTENT
// reportType can be any of there:
// https://github.com/bordar/server/blob/master/api_v3/lib/types/enums/BorhanReportType.php
$report_type_string='TOP_CONTENT';
$reportType = constant('BorhanReportType::'.$report_type_string);
$reportInputFilter = new BorhanReportInputFilter();
// epoch representation of the start and end dates
$reportInputFilter->fromDate = $start_date;
$reportInputFilter->toDate = $end_date;
// interval can also be BorhanReportInterval::MONTHS;
$reportInputFilter->interval = BorhanReportInterval::DAYS;
$dimension = null;
// objectIds: comma separated string of entry ids
$objectIds = null;
echo "Getting $report_type_string total info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->gettotal($reportType, $reportInputFilter, $objectIds);
var_dump($result);

echo "Getting $report_type_string graph info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->getgraphs($reportType, $reportInputFilter, $dimension, $objectIds);
var_dump($result);


// set type to OPERATION_SYSTEM
$report_type_string='OPERATION_SYSTEM';
$reportType = constant('BorhanReportType::'.$report_type_string);
$reportInputFilter = new BorhanReportInputFilter();
$reportInputFilter->fromDate = $start_date;
$reportInputFilter->toDate = $end_date;
$reportInputFilter->interval = BorhanReportInterval::DAYS;
$dimension = null;
$objectIds = null;
echo "Getting $report_type_string total info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->gettotal($reportType, $reportInputFilter, $objectIds);
var_dump($result);

echo "Getting $report_type_string graph info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->getgraphs($reportType, $reportInputFilter, $dimension, $objectIds);
var_dump($result);
?>
