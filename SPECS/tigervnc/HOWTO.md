# What has changed
The previous Tigervnc versions had a wrapper script called `vncserver` which 
could be run as a user manually to start *Xvnc* process. The usage was quite 
simple as you just run
```
$ vncserver :x [vncserver options] [Xvnc options]
```
and that was it. While this was working just fine, there were issues when users
wanted to start a Tigervnc server using *systemd*. For these reasons things were 
completely changed and there is now a new way how this all is supposed to work.

 # How to start Tigervnc server
 
## Add a user mapping
With this you can map a user to a particular port. The mapping should be done in 
`/etc/tigervnc/vncserver.users` configuration file. It should be pretty 
straightforward once you open the file as there are some examples, but basically
the mapping is in form
```
:x=user
```
For example you can have
```
:1=test
:2=vncuser
```

## Configure Xvnc options
To configure Xvnc parameters, you need to go to the same directory where you did
the user mapping and open `vncserver-config-defaults` configuration file. This 
file is for the default Xvnc configuration and will be applied to every user 
unless any of the following applies:
* The user has its own configuration in `$HOME/.vnc/config`
* The same option with different value is configured in 
  `vncserver-config-mandatory` configuration file, which replaces the default 
  configuration and has even a higher priority than the per-user configuration.
  This option is for system administrators when they want to force particular 
  *Xvnc* options.

Format of the configuration file is also quite simple as the configuration is
in form of
```
option=value
option
```
for example
```
session=gnome
securitytypes=vncauth,tlsvnc
desktop=sandbox
geometry=2000x1200
localhost
alwaysshared
```
### Note:
There is one important option you need to set and that option is the session you
want to start. E.g when you want to start GNOME desktop, then you have to use
```
session=gnome
```
which should match the name of a session desktop file from `/usr/share/xsessions`
directory.

## Set VNC password
You need to set a password for each user in order to be able to start the 
Tigervnc server. In order to create a password, you just run
```
$ vncpasswd
```
as the user you will be starting the server for. 
### Note:
If you were using Tigervnc before for your user and you already created a 
password, then you will have to make sure the `$HOME/.vnc` folder created by 
`vncpasswd` will have the correct *SELinux* context. You either can delete this 
folder and recreate it again by creating the password one more time, or 
alternatively you can run
```
$ restorecon -RFv /home/<USER>/.vnc
```

## Start the Tigervnc server
Finally you can start the server using systemd service. To do so just run
```
$ systemctl start vncserver@:x
```
as root or
```
$ sudo systemctl start vncserver@:x
```
as a regular user in case it has permissions to run `sudo`. Don't forget to 
replace the `:x` by the actual number you configured in the user mapping file. 
Following our example by running
```
$ systemctl start vncserver@:1
```
you will start a Tigervnc server for user `test` with a GNOME session.

### Note:
If you were previously using Tigervnc and you were used to start it using 
*systemd* then you will need to remove previous *systemd* configuration files,
those you most likely copied to `/etc/systemd/system/vncserver@.service`, 
otherwise this service file will be preferred over the new one installed with
latest Tigervnc.

# Limitations
You will not be able to start a Tigervnc server for a user who is already
logged into a graphical session. Avoid running the server as the `root` user as
it's not a safe thing to do. While running the server as the `root` should work 
in general, it's not recommended to do so and there might be some things which
are not working properly.
