    #!/usr/bin/tclsh
    
    # create workspace
	setws ./fsbl_workspace
    # create project
    createhw -name hw0 -hwspec ../../zed_example/zed_example.sdk/zed_bd_wrapper.hdf
    createapp -name fsbl -app {Zynq FSBL} -proc ps7_cortexa9_0 -hwproject hw0 -os standalone
    configapp -app fsbl 

    # build project 
    projects -build
    
   
    exit
