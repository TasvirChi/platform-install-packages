<?php

if (count($argv)<4){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <-2 secret> <dropfolder path>'."\n";
    exit (1);
}

function enable_dropbox_permission($client,$config,$partner_id)
{

        $config->partnerId=$partner_id;
        //$client->setConfig($config);
        $client->setPartnerId($partner_id);
        $permission = new BorhanPermission();
        $permission->name = 'DROPFOLDER_PLUGIN_PERMISSION';

        $filter = new BorhanPermissionFilter();
        $filter->nameEqual = $permission->name;
        $pager = null;
        $result = $client->permission->listAction($filter, $pager);
        if (!isset($result->objects[0]->status)|| $result->objects[0]->status!==1){
                $result = $client->permission->add($permission);
        }
}



function create_dropbox($client,$partnerId, $droppath)
{

	try{
		$dropFolder = new BorhanDropFolder();
		$dropFolder->partnerId = $partnerId;
		$dropFolder->name = 'sanity_drop';
		$dropFolder->description = 'done by '.__FILE__;
		$dropFolder->status = BorhanDropFolderStatus::ENABLED;
		$dropfolderPlugin = BorhanDropfolderClientPlugin::get($client);
		$dropFolder->type = BorhanDropFolderType::LOCAL;
		$dropFolder->dc = 0;
		$dropFolder->fileHandlerType = BorhanDropFolderFileHandlerType::CONTENT;
		$dropFolder->fileHandlerConfig = new BorhanDropFolderContentFileHandlerConfig();
		$dropFolder->fileHandlerConfig->contentMatchPolicy=BorhanDropFolderContentFileHandlerMatchPolicy::MATCH_EXISTING_OR_ADD_AS_NEW;
	
		$dropFolder->path=$droppath;
		mkdir($dropFolder->path);
		chown($dropFolder->path,'borhan');
		chgrp($dropFolder->path,'apache');
		chmod($dropFolder->path,0775);
		$drop_obj = $dropfolderPlugin->dropFolder->add($dropFolder);
		$drop_id=$drop_obj->id;
		$status_msg="'".$drop_obj->name.' successfully created for partner:' .$drop_obj->partnerId;
		$dropfolderPlugin->dropFolder->delete($drop_id);
		return $status_msg;
		
	}catch(exception $e){
		throw $e;
	}
	 

}
$service_url = $argv[1];
$partnerId=$argv[2];
$minus_2_secret=$argv[3];
$droppath=$argv[4];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
//$client=generate_ks($service_url,-2,$minus_2_secret,$type=BorhanSessionType::ADMIN,$userId=null);


    $config = new BorhanConfiguration(-2);
    $config->serviceUrl = $service_url;  
    $client = new BorhanClient($config);
    $ks = $client->session->start($minus_2_secret, null, BorhanSessionType::ADMIN, -2, null,null);
    $client->setKs($ks);
enable_dropbox_permission($client,$config,$partnerId);
//die();
/*$filter = new BorhanPermissionFilter();

$filter->typeEqual = BorhanPermissionType::NORMAL;
$filter->name = 'dropFolder.SYSTEM_ADMIN_DROP_FOLDER_BASE';
$pager = null;
$result = $client->permission->listAction($filter, $pager);
var_dump($result) ;exit(0);*/

$out=create_dropbox($client,$partnerId,$droppath);
echo $out;
