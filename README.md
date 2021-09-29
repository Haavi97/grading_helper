Module main
===========
This module does following things:
* Extract projects from zipfile in directory specified in configuration.
* Execute catkin_make in catkin_ws
* Execute rospack command in catkin_ws

Functions
---------

    
`catkin_make()`
:   Execute catkin_make command in catkin_ws.
    :return: success

    
`extract_projects(zipfilename)`
:   Extract zipped projects from zipfile to catkin_ws. If the directory has files already then skip.
    :param zipfilename:
    :return:

    
`main()`
:   

    
`rename_files_to_latin(files_path)`
:   

    
`rospack()`
:   Execute rospack profile command in caktin_ws,
    :return: success


Module exec
===========
This module does traverse projects in catkin_ws and executes command from configuration in them.
Project execution can be terminated using ctr-c hotkey.

Functions
---------

    
`main()`
:   Traverse the "catkin_src" directory from config file for projects and execute 'launch_command' in them.
    While process is running it is safe to terminate it with CTR-C hotkey. The script intercepts it and terminates project.
    :return:
