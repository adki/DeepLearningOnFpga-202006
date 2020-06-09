@ECHO OFF

IF EXIST train.o           DEL /Q train.o          
IF EXIST test.o            DEL /Q test.o           
IF EXIST compile.log.train DEL /Q compile.log.train
IF EXIST compile.log.test  DEL /Q compile.log.test 
IF EXIST train             DEL /Q train            
IF EXIST test              DEL /Q test             
IF EXIST pixel_net         DEL /Q pixel_net          
IF EXIST pixel_net_json    DEL /Q pixel_net_json     
