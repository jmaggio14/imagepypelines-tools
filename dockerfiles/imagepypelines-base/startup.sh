echo -e "
################################################################################
##############################Ndyo/:.        .-/+shN############################
##########################my/.                       :sd########################
#######################mo-                               /h#####################
#####################h\033[38;5;208mo/+o+/.\e[39m\e[49m                              .oN##################
###################s\033[38;5;208m-oooooooo/\e[39m\e[49m                                +N################
#################d. \033[38;5;208m:ooooooooo \e[39m\e[49m                                o################
################+   \033[38;5;208m.oooooooo+ \e[39m\e[49m                                  -m#############
##############N-     \033[38;5;208m./oooo+:\e[39m\e[49m                                      h############
#############N.     \033[38;5;208m.---::--.           .:::::::-../////////::.\e[39m\e[49m     h###########
#############-      \033[38;5;208m+ooooooooo.         :oooooooooossssssssssss+\e[39m\e[49m     m##########
############o       \033[38;5;208m+ooooooooo.         :ooooooooossssssssssssss+\e[39m\e[49m    -##########
###########N        \033[38;5;208m+ooooooooo.         :ooooooooossssssssssssss+\e[39m\e[49m     y#########
###########s        \033[38;5;208m+ooooooooo.         :ooooooooossssssssssssss+\e[39m\e[49m     -#########
###########:        \033[38;5;208m+ooooooooo.         :ooooooooo:    :sssssssss+\e[39m\e[49m     N########
###########.        \033[38;5;208m+ooooooooo.         :ooooooooo:   -sssssssss+\e[39m\e[49m      d########
###########.        \033[38;5;208m+ooooooooo.         :ooooooooo:   -sssssssss+\e[39m\e[49m      d########
###########:        \033[38;5;208m+ooooooooo.         :ooooooooo:   -sssssssss+\e[39m\e[49m      N########
###########s        \033[38;5;208m+ooooooooo.         :ooooooooo:   -sssssssss+\e[39m\e[49m     -#########
###########N        \033[38;5;208m/ooooooooo:---------/ooooooooo/---/sssssssss+\e[39m\e[49m     y#########
############o        \033[38;5;208m./ooooooossssssss/ :ossssssssssssssssssssss+\e[39m\e[49m    .##########
#############-          \033[38;5;208m:ooooossssso:   :ooossssssssssssssssssss+\e[39m\e[49m    d##########
#############N.           \033[38;5;208m-+oosss+-     :oooooosssssssssssssssss/\e[39m\e[49m   h###########
##############N-            \033[38;5;208m./s/.       :oooooooossssssssssssso:\e[39m\e[49m   h############
################+                       \033[38;5;208m:ooooooooo: \e[39m\e[49m             -m#############
#################h.                     \033[38;5;208m:ooooooooo:\e[39m\e[49m             o###############
###################s.                   \033[38;5;208m:ooooooooo:\e[39m\e[49m           +N################
#####################y-                 \033[38;5;208m:ooooooooo:\e[39m\e[49m         oN##################
#######################mo-              \033[38;5;208m:ooooooooo-\e[39m\e[49m      /h#####################
##########################my/.          \033[38;5;208m:oooooooo/\e[39m\e[49m   :od########################
##############################Ndyo/:. -///+ossoshm##############################
################################################################################"
echo -e "
Welcome to the imagepypelines virtual container! This docker image contains all dependencies you need to run vanilla imagepypelines apps. The source for this dockerfile can be found here: https://github.com/jmaggio14/imagepypelines-tools

ENV VARIABLES:
	IP_GPU_ENABLED: $IP_GPU_ENABLED
	IP_ABORT_NESTED_SHELLS: $IP_ABORT_NESTED_SHELLS

the following folders have been mounted to this container:
$MOUNTED_VOLUMES
you can mount additional folders with the following
	imagepypelines shell -v /path/to/folder/on/host:/where/you/want/to/mount/it

GPU support (Nvidia Only):
    On Linux host systems:
        > install nvidia-docker: https://github.com/NVIDIA/nvidia-docker
        > add the flag --with-gpu when you launch this shell

    On Windows or MacOSX host systems:
        > GPU access from this container is not possible

some things to note:
	> as of now, graphics are not supported from this container
	> any changes made to folders not listed above will NOT be persistent
	> you are root. so no need to use sudo :p
	> you may exit this shell by typing 'exit'
"
