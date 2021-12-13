Red Hat Specific mod_auth_mellon Information
============================================

This README contains information specific to Red Hat's distribution of
``mod_auth_mellon``.

Diagnostic Logging
------------------

Diagnostic logging can be used to collect run time information to help
diagnose problems with your ``mod_auth_mellon`` deployment. Please see
the "Mellon Diagnostics" section in the Mellon User Guide for more
details.

How to enable diagnostic logging on Red Hat systems
```````````````````````````````````````````````````

Diagnostic logging adds overhead to the execution of
``mod_auth_mellon``. The code to emit diagnostic logging must be
compiled into ``mod_auth_mellon`` at build time. In addition the
diagnostic log file may contain security sensitive information which
should not normally be written to a log file. If you have a
version of ``mod_auth_mellon`` which was built with diagnostics you
can disable diagnostic logging via the ``MellonDiagnosticsEnable``
configuration directive. However given human nature the potential to
enable diagnostic logging while resolving a problem and then forget to
disable it is not a situation that should exist by default. Therefore
given the overhead consideration and the desire to avoid enabling
diagnostic logging by mistake the Red Hat ``mod_auth_mellon`` RPM's
ship with two versions of the ``mod_auth_mellon`` Apache module.

1. The ``mod_auth_mellon`` RPM contains the normal Apache module
   ``/usr/lib*/httpd/modules/mod_auth_mellon.so`` 

2. The ``mod_auth_mellon-diagnostics`` RPM contains the diagnostic
   version of the Apache module
   ``/usr/lib*/httpd/modules/mod_auth_mellon-diagnostics.so``

Because each version of the module has a different name both the
normal and diagnostic modules can be installed simultaneously without
conflict. But Apache will only load one of the two modules. Which
module is loaded is controlled by the
``/etc/httpd/conf.modules.d/10-auth_mellon.conf`` config file which
has a line in it which looks like this::

    LoadModule auth_mellon_module modules/mod_auth_mellon.so

To load the diagnostics version of the module you need to change the
module name so it looks like this::

    LoadModule auth_mellon_module modules/mod_auth_mellon-diagnostics.so

**Don't forget to change it back again when you're done debugging.**

You'll also need to enable the collection of diagnostic information,
do this by adding this directive at the top of your Mellon conf.d
config file or inside your virtual host config (diagnostics are per
server instance)::

    MellonDiagnosticsEnable On

.. NOTE::
   Some versions of the Mellon User Guide have a typo in the name of
   this directive, it incorrectly uses ``MellonDiagnosticEnable``
   instead of ``MellonDiagnosticsEnable``. The difference is
   Diagnostics is plural.

The Apache ``error_log`` will contain a message indicating how it
processed the ``MellonDiagnosticsEnable`` directive. If you loaded the
standard module without diagnostics you'll see a message like this::

    MellonDiagnosticsEnable has no effect because Mellon was not
    compiled with diagnostics enabled, use
    ./configure --enable-diagnostics at build time to turn this
    feature on.

If you've loaded the diagnostics version of the module you'll see a
message in the ``error_log`` like this::

    mellon diagnostics enabled for virtual server *:443
    (/etc/httpd/conf.d/my_server.conf:7)
    ServerName=https://my_server.example.com:443, diagnostics
    filename=logs/mellon_diagnostics
