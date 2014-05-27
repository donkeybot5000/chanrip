chanrip
=======

chanrip is a simple-to-use script that downloads all the images off a single board on 4chan. It follows all API rules, and can be easily automated. chanrip depends on python.

The syntax is pretty simple:

    chmod +x chanrip.py
    ./chanrip.py a
    
Where 'a' can be any 4chan board short name.

automation
==========

chanrip can be easily automated, since it is entirely operated through the command line. In case of an emergency, you can stop the script from downloading in the future by creating a file called ```stopcron.txt``` in the same directory.
