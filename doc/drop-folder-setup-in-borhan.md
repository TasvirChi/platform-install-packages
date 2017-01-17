Setting up a Drop folder in Borhan
====================================

######After Creating a Publisher in Borhan 

* Creat a Transcoding Profile ( I have created in my name as blackyboy transcoding 

* Then Configure DropBox for Publisher by choosing configure in Drop menu

* And Tick the check box, Content Ingestion - **Drop Folder/s (config)**

* Then Click on configure and change the settings.
  
  Note your Publisher ID from user's list ( My Publisher ID 102) and Create using Type : Local

  Drop Folder Name: our Wish ( Here i have used blackyboy)

  Description: As our Wish (This is blackyboy's Drop)

* Conversion Profile ID: Choose your created name Here from Drop list

* Drop Folder Storage Path: /opt/borhan/web/content/blackyboy (or) any folder name

  Check file size every (seconds): 10

* Choose Manual Deletion if you Don't want to delete the Source.

  Save it ... that't it in BMC side..

-------------------------------------------------------------------------

### Then in Terminal 

* Create a directory named as you have mentioned here (Drop Folder Storage Path: /opt/borhan/web/content/blackyboy)

```
Eg : mkdir /opt/borhan/web/content/blackyboy
```

* Then add a user for FTP

```
# useradd -d /opt/borhan/web/content/blackyboy blackyboy  ( home Dir of this blackyboy user is /opt/borhan/web/content/blackyboy )
```
(skel file error will be display, we don't need a bash profile so don't mind the error)

Create a password for the user which we have created for Drop

```
# passwd blackyboy

New passwd: ********
Con Passwd: ********
```

* Add the user blackyboy to apache & borhan Group
   Only borhan Group is Enough

```
# usermod -a -G apache,borhan blackyboy

```

* Navigate to directory 

```
# cd /opt/borhan/web/content
```

* Change the Ownership of blackyboy

```
# chown blackyboy:borhan blackyboy/

```
  Note : Here i have setuped for sftp because ftp is not secured one, If we need ftp just 2 more step to be added in above steps, those are 

```
# usermod -a -G ftp,borhan blackyboy

```

  And at last we need to restart the vsftpd Service 

```
# /etc/init.d/vsftpd restart
```

* Login the sftp from filezilla 

  And upload a video file, it will be uploaded to **/opt/borhan/web/content/blackyboy**

  After Completing upload it wait's for 10 seconds and it will move to BMC Content TAB and Start to convert it Using      Transcoding profile Which we have created.

  We can see the Progress of uploading from (Drop folder) Under Content TAB 

  That's it ..

  
