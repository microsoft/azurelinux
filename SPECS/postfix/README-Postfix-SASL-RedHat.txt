Quick Start to Authenticate with SASL and PAM:
----------------------------------------------

If you don't need the details and are an experienced system
administrator you can just do this, otherwise read on.

1) Edit /etc/postfix/main.cf and set this:

smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
broken_sasl_auth_clients = yes

smtpd_recipient_restrictions = 
  permit_sasl_authenticated,
  permit_mynetworks,
  reject_unauth_destination

2) Turn on saslauthd:

   /sbin/chkconfig --level 345 saslauthd on
   /sbin/service saslauthd start

3) Edit /etc/sysconfig/saslauthd and set this:

   MECH=pam

4) Restart Postfix:

   /sbin/service postfix restart

A crash course in using SASL with Postfix:
------------------------------------------

Red Hat's Postfix RPMs include support for both SASL and TLS.  SASL, the
Simple Authentication and Security Layer, allows Postfix to implement RFC
2554, which defines an extension to ESMTP, SMTP AUTH, which compliant
ESMTP clients can use to authenticate themselves to ESMTP servers.
Typically, this is used to allow roaming users to relay mail through a
server safely without configuring the SMTP server to be an open relay.
Inclusion of TLS support allows Postfix to implement RFC 2487, which
defines an extension to ESMTP, SMTP STARTTLS, which compliant ESMTP
clients and servers can use to encrypt the SMTP session.  This is a
security enhancement -- normally SMTP is transmitted as cleartext over the
wire, making it vulnerable to both passive sniffing and active alteration
via monkey-in-the-middle attacks.  In addition, STARTTLS can also be
used by either or both server and client to verify the identity of the
other end, making it useful for the same sorts of purposes as SMTP AUTH.
The two can even be combined.  Typically, this is done by first starting
TLS, to encrypt the SMTP session, and then issuing the SMTP AUTH command,
to authenticate the client; this combination ensures that the username
and password transferred as part of the SMTP AUTH are protected by the
TLS encrypted session.

SMTP AUTH is implemented using SASL, an abstraction layer which can
authenticate against a variety of sources.  On Red Hat, SASL can use
the /etc/shadow file, or it can use PAM libraries, or it can use its own
password database (/etc/sasldb), or it can do various more exotic things.

Authentication raises a number of security concerns for obvious
reasons. As a consequence authentication services on Red Hat systems
are restricted to processes running with root privileges. However for
security reasons it is also essential that a mail server such as
Postfix run without root privileges so that mail operations cannot
compromise the host system. This means that Postfix cannot directly
use authentication services because it does not execute with root
privileges. The answer to this this problem is to introduce an
intermediary process that runs with root privileges which Postfix can
communicate with and will perform authentication on behalf of
Postfix. The SASL package includes an authentication daemon called
saslauthd which provided this service, think of it as an
authentication proxy.

Using Saslauthd:
---------------- 

To use saslauthd there are several things you must assure are
configured. 

Selecting an Authentication Method:
-----------------------------------

Recall that it is saslauthd which is authenticating, not
Postfix. To start with you must tell Postfix to use saslauthd, in
main.cf edit this configuration parameter:

   smtpd_sasl_auth_enable = yes

It is also recommended that you disable anonymous logins otherwise
you've left your system open, so also add this configuration
parameter. 

   smtpd_sasl_security_options = noanonymous

Now you must tell saslauthd which authentication method to use. To
determine the authentication methods currently supported by saslauthd
invoke saslauthd with the -v parameter, it will print its version and
its list of methods and then exit, for example:

   /usr/sbin/saslauthd -v
   saslauthd 2.1.10
   authentication mechanisms: getpwent kerberos5 pam rimap shadow 

When saslauthd starts up it reads its configuration options from the
file /etc/sysconfig/saslauthd. Currently there are two parameters
which can be set in this file, MECH and FLAGS. MECH is the
authentication mechanism and FLAGS is any command line flags you may
wish to pass to saslauthd. To tell saslauthd to use a specific
mechanism edit /etc/sysconfig/saslauthd and set the MECH parameter,
for example to use PAM it would look like this:

   MECH=pam

Of course you may use any of the other authentication mechanisms that
saslauthd reported it supports. PAM is an excellent choice as PAM
supports many of the same authentication methods that saslauthd does,
but by using PAM you will have centralized all of your authentication
configuration under PAM which is one of PAM's greatest assets.

How Postfix Interacts with SASL to Name its Authentication Services:
--------------------------------------------------------------------

It can be very helpful to understand how Postfix communicates with
SASL to name its authentication services. Knowing this will let you
identify the configuration files the various components will access.

When Postfix invokes SASL it must give SASL an application name that
SASL will use among other things to locate a configuration file for
the application. The application name Postfix identifies itself as is
"smtpd". SASL will append ".conf" to the application name and look for
a config file in its library and config directories. Thus SASL will
read Postfix's configuration from

   /etc/sasl2/smtpd.conf

This file names the authentication method SASL will use for Postfix
(actually for smtpd, other MTA's such as sendmail may use the same
file). Because we want to use the saslauthd authentication proxy
daemon the contents of this file is:

   pwcheck_method: saslauthd

This tells SASL when being invoked to authentication for Postfix that
it should use saslauthd. Saslauthd's mechanism is set in
/etc/sysconfig/saslauthd (see below).

When Postfix calls on SASL to authenticate it passes to SASL a service
name. This service name is used in authentication method specific
way. The service name Postfix passes to SASL is "smtp" (note this is
not the same as the application name which is "smtpd"). To understand
this better consider the case of using PAM authentication. When SASL,
or in our case saslauthd, invokes PAM it passes the service name of
"smtp" to PAM which means that when PAM wants to read configuration
information for this client it will find it under the name of "smtp". 

Turning on the Authentication Daemon:
-------------------------------------

Red Hat security policy is not to automatically enable services
belonging to a package when the package is installed. The system
administrator must explicitly enable the service. To enable saslauthd
do the following:

1) Tell the init process to launch saslauthd when entering various run
   levels. Assuming you want saslauthd to run at run levels 3,4,5
   invoke chkconfig.

   /sbin/chkconfig --level 345 saslauthd on

2) You will probably want to start saslauthd now without having to
   reboot, to do this:

   /sbin/service saslauthd start

Trouble Shooting Authentication:
--------------------------------

The best way to debug authentication problems is to examine log
messages from the authentication components. However, normally these
log messages are suppressed. There are two principle reasons the
messages are suppressed. The first is that they are typically logged
at the DEBUG logging priority level which is the lowest priority and
the syslog configuration typically logs only higher priority
messages. The second reason is that for security reasons authentication
logging is considered a risk. Authentication logging has been divided
into two different facilities, auth and authpriv. authpriv is private
and is typically shunted off to a different log file with higher
protection. You will want to be able to see both auth and authpriv
messages at all priorities. To do this as root edit /etc/syslog.conf
file, find the following line

authpriv.*					/var/log/secure

edit the line to:

authpriv.*;auth.*				/var/log/secure

Then restart syslogd so the syslog configuration changes will be
picked up:

       /sbin/service syslog restart

Now all authentication messages at all priorities will log to
/var/log/secure. 

Using PAM to Authenticate:
--------------------------

Edit /etc/sysconfig/saslauthd and set MECH to PAM like this:

   MECH=pam

When PAM is invoked via SASL it is passed a service name of
"smtp". This means that PAM will read its configuration parameters for
Postfix from the file: /etc/pam.d/smtp. By default this file is set to
refer to the global system PAM authentication policy, thus by default
you'll get whatever PAM authentication your system is configured for
and virtually all applications use. Configuring PAM authentication is
beyond the scope of this document, please refer to the PAM
documentation if you which to modify PAM.

Trouble Shooting PAM Authentication:
------------------------------------

1) One possible reason PAM may fail to authenticate even if the user
is known to the system is if PAM fails to find the service
configuration file in /etc/pam.d. Service configuration files are not
required by PAM, if it does not find a service configuration file it
will default to "other". Since PAM does not consider the absence of a
service configuration file a problem it does not log anything nor does
it return an error to the calling application. In other words it is
completely silent about the fact it did not find a service
configuration file. On Red Hat system the default implementation of
"other" for PAM is to deny access. This means on Red Hat systems the
absence of a PAM service configuration file will mean PAM will
silently fail authentication. The PAM service configuration file for
postfix is /etc/pam.d/smtp and is intalled by the Red Hat Postfix rpm
and put under control of "alternatives" with name mta. Alternatives
allows one to select between the sendmail and postfix MTA's and
manages symbolic links for files the two MTA's share. /etc/pam.d/smtp
is one such file, if you have not selected Postfix as your prefered
MTA the link to this file will not be present. To select Postfix as
your MTA do this: "/usr/sbin/alternatives --config mta" and follow the
prompt to select postfix.

2) Is SASL appending a realm or domain to a username? PAM
   authentication requires a bare username and password, other
   authentication methods require the username to be qualified with a
   realm. Typically the username will be rewritten as user@realm
   (e.g. user@foo.com) PAM does not understand a username with
   "@realm" appended to it and will fail the authentication with the
   message that the user is unknown. If the log files shows saslauthd
   usernames with "@realm" appended to it then the
   smtpd_sasl_local_domain configuration parameter is likely set in
   /etc/postfix/main.cf file, make sure its either not set or set it
   to an empty string. Restart postfix and test authtentication again,
   the log file should show only a bare username.



Using saslpasswd to Authenticate:
---------------------------------

SASL can maintain its own password database independent of the host
system's authentication setup, it is called saslpasswd. You may wish
to use saslpasswd if you want to isolate who can smtp authenticate
from general system users. However, it does add another password
database that a system administrator must maintain.

To authenticate against sasldb, you'll first have to create accounts.
These accounts are entirely separate from system accounts, and are used
only by connecting SMTP clients to authenticate themselves.  Use the
saslpassword command:

saslpasswd -u `postconf -h myhostname` -c user

to create an account named user which can log into realm.  For the
realm, make absolutely certain that you use the same value as is set for
myhostname in /etc/postfix/main.cf.  If you don't, it likely won't work.

Also, be aware that saslpasswd is somewhat buggy.  The first time you
run it, it may generate an error message while initializing the sasldb.
If it does, just add that user a second time.

You'll need to set permissions on the SASL password database so that
the Postfix daemons can read it:

   chgrp postfix /etc/sasldb
   chmod g+r /etc/sasldb

Now, you'll need to modify /etc/postfix/main.cf to tell it to
support SASL.  The complete options you might want to use are in the
sample-auth.cf file in the Postfix documentation directory.  An option
you will definitely need is:

# enable SASL support
smtpd_sasl_auth_enable = yes

You might also need to set the SASL authentication realm to whatever
realm you used when you created your sasldb; by default, this is set to
$myhostname, but you instead might need something like:

# set SASL realm to domain instead
smtpd_sasl_local_domain = $mydomain

Other Postfix Authentication Parameters:
----------------------------------------

If you want to allow your already configured users to still use your SMTP
server, and to allow users authenticated via SMTP AUTH to use your server
as well, then modify your existing smtpd_recipient_restrictions line to;

# also allow authenticated (RFC 2554) users
smtpd_recipient_restrictions = permit_sasl_authenticated ...

If you want to restrict use of your server to just authenticated clients
(Note: this is a bad idea for public mail servers), then instead use:

# restrict server access to authenticated (RFC 2554) clients
smtpd_delay_reject = yes
smtpd_client_restrictions = permit_sasl_authenticated ...

SASL supports several password types which have differing security
properties.  Different SMTP clients may support some or all of these
password types.  When the client issues an EHLO command, the server
tells it which types it supports:

$ telnet station6 25
Trying 10.100.0.6...
Connected to station6.example.com.
Escape character is '^]'.
220 station6.example.com ESMTP Postfix
ehlo station7
250-station6.example.com
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-AUTH PLAIN LOGIN DIGEST-MD5 CRAM-MD5
250-XVERP
250 8BITMIME

Here, the server supports PLAIN, LOGIN, DIGEST-MD5, and CRAM-MD5 password
methods.

The client then chooses the first of these listed methods which it also
supports, and issues an SMTP AUTH request.

For security, PLAIN and LOGIN methods are typically disabled.  These two
methods use trivially decryptable encryption, making the username and
password issued by the client vulnerable to interception via a sniffer
in between the server and client.  Unfortunately, they can't always
be disabled.  Some popular SMTP clients, including MS Outlook 5.x,
only support PLAIN authentication, for example.

To limit the login methods offered by the server:

# disable unsafe password methods
smtpd_sasl_security_options = noplaintext noanonymous

Available options are:

noplaintext, which disables LOGIN and PLAIN
noanonymous, which disables disables ANON
nodictionary, which disables methods vulnerable to dictionary attacks
noactive, which disables methods vulnerable to active attacks

The last two are rarely used, since almost all supported methods are
vulnerable to those attacks ;-).

Also be aware that some broken clients mis-implement the SMTP AUTH
protocol, and send commands using incorrect syntax (AUTH=foo instead of
the correct AUTH foo).  MS Outlook 4.x clients have this bug, among
a legion of others....  If you need to support these clients, use:

# support braindead MS products
broken_sasl_auth_clients = yes

To help prevent spoofing, you can also create a map file of SASL login
names which are allowed to use specific envelope sender (MAIL FROM)
addresses.  If you choose to do this, you also have to tell Postfix to
reject addresses which don't match login names:

# prevent spoofing by authenticated users
reject_sender_login_mismatch
smtpd_sender_login_maps=type:/path/to/file

Configuration of SASL clients is much simpler.  Postfix itself can be
made a SASL client; this is typically useful when roaming users run Linux
on their laptop and need to relay mail back through the organization's
main server.

To enable Postfix to act as an SMTP AUTH client, simply add to
/etc/postfix/main.cf:

# support authentication (RFC 2557) when relaying through a server
smtp_sasl_auth_enable = yes

and tell Postfix where to find the usernames and passwords it should
use to authenticate:

# location of passwords for authentication client
smtp_sasl_password_maps = type:/path/to/file

The file itself should have the format:

destination     username:password

where destination is the name of the server, and username:password are
the username and password which should be presented to that server to
authenticate when connecting to it as a client.

Optionally, the authentication methods to be used can be specified for
the Postfix client, just as they can be for the Postfix server:

# disable plaintext and anonymous
smtp_sasl_security_options = noplaintext noanonymous

Many popular end-user MUAs can also be configured as SMTP AUTH clients.
Clients capable of this supplied with Red Hat include pine, Netscape,
and Mozilla.

Other Sources of Documentation:
-------------------------------

/usr/share/doc/postfix-<version>/README_FILES/SASL_README

Local configuration examples:

/usr/share/doc/postfix-*/samples

Postfix Howtos, Guides and Tips by Ralf Hildebrandt and Patrick
Koetter can be found at: http://postfix.state-of-mind.de

------------------------------------------------------------------------------

Please send any comments / corrections to Chris Ricker
<kaboom@gatech.edu>.  This material can be freely modified and
redistributed. Additional material provided by John Dennis
<jdennis@redhat.com> and Dax Kelson <dax@gurulabs.com>.
