@ECHO OFF

IF EXIST train.o           DEL /Q train.o          
IF EXIST test.o            DEL /Q test.o           
IF EXIST compile.log.train DEL /Q compile.log.train
IF EXIST compile.log.test  DEL /Q compile.log.test 
IF EXIST train             DEL /Q train            
IF EXIST test              DEL /Q test             
IF EXIST xor_net           DEL /Q xor_net          
IF EXIST xor_net_json      DEL /Q xor_net_json     
