echo -e "
Welcome to the imagepypelines virtual container!

This docker image contains all dependencies you need to run vanilla imagepypelines apps. The source for this dockerfile can be found here: https://github.com/jmaggio14/imagepypelines-tools/blob/master/dockerfiles/imagepypelines-base/dockerfile

the following folders have been mounted to this container:
$MOUNTED_VOLUMES

you can mount additional folders with the following
	imagepypelines shell -v /path/to/folder/on/host:/where/you/want/to/mount/it

some things to note:
	> as of now, graphics are not supported in this container
	> any changes made to folders not listed above will NOT be persistent
	> you are root. so no need to use sudo :p
	> you may exit this shell by typing 'exit'
"
