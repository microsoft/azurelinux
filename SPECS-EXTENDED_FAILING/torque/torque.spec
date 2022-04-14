# The following options are supported:
#   --with server_name=hostname
#   --with homedir=directory
#   --with[out] rcp
#   --with[out] gui
#   --with[out] tcl

# Hrm, should we default to the name of the buildhost?  That seems only
# slightly better than picking a hostname at random.  This is exactly the kind
# of compile-time default that doesn't work well with distributable packages.
# Let's force the issue with the non-sensical "localhost".
# 
# Note that "localhost" doesn't actually work.  You must either define the
# correct hostname here, pass '--with server_name=foo' to rpmbuild, or be sure
# that $PBS_SERVER_HOME/server_name contains the correct hostname.
%global server_name localhost

%bcond_with docs

# Build doxygen docs
%global doxydoc 0

%global use_rcp 0
%global use_tcl 1
%global build_gui 1

# these are non-defaults, but fit better into most RPM-based systems
%global torquehomedir %{_localstatedir}/lib/torque

# --with/--without processing
# first, error if conflicting options are used
%{?_with_rcp: %{?_without_rcp: %{error: both _with_rcp and _without_rcp}}}
%{?_with_tcl: %{?_without_tcl: %{error: both _with_tcl and _without_tcl}}}
%{?_with_gui: %{?_without_gui: %{error: both _with_gui and _without_gui}}}

# did we find any --with options?
%{?_with_rcp: %global use_rcp 1}
%{?_with_tcl: %global use_tcl 1}
%{?_with_gui: %global build_gui 1}

%{?_with_server_name:%global server_name %(set -- %{_with_server_name}; echo $1 | grep -v with | sed 's/=//')}
%{?_with_homedir:%global torquehomedir %(set -- %{_with_homedir}; echo $1 | grep -v with | sed 's/=//')}

# did we find any --without options?
%{?_without_rcp: %global use_rcp 0}
%{?_without_tcl: %global use_tcl 0}
%{?_without_gui: %global build_gui 0}

# Set up all options as disabled
%global rcpflags    --with-rcp=/usr/bin/scp
%global tclflags    --without-tcl
%global guiflags    --disable-gui

# Enable options that we want
%if %{use_rcp}
%global rcpflags    --with-rcp=mom_rcp
%endif

%if %{build_gui}
%global guiflags   --enable-gui
%endif

%if %{use_tcl}
%if %{build_gui}
%global tclflags    --with-tcl --with-tk
%else
%global tclflags    --with-tcl --without-tk
%endif
%endif

# finish up the configs...
%global server_nameflags --with-default-server=%{server_name}

Name:        torque
Version:     4.2.10
Release:     27%{?dist}
Summary:     Tera-scale Open-source Resource and QUEue manager
Source0:     http://www.adaptivecomputing.com/download/%{name}/%{name}-%{version}.tar.gz
Source2:     xpbs.desktop
Source3:     xpbsmon.desktop
Source4:     xpbs.png
Source5:     xpbsmon.png
Source6:     README.Fedora
Source8:     config
Source20:    pbs_mom.service
Source21:    pbs_sched.service
Source22:    pbs_server.service
Source23:    trqauthd.service
Source24:    mom.layout
# Feb 3rd 2011, I've sent a mail upstream to request the re-inclusion
# of the OpenPBS license file in distribution.
# I'll announce to fedora-devel once this is resolved either way.
# Fedora approval of TORQUEv1.1
# http://lists.fedoraproject.org/pipermail/legal/2011-February/001530.html
# This is a wrapper for multilib
Source100:   pbs-config

# https://bugzilla.redhat.com/show_bug.cgi?id=713996
Patch1:      torque-munge-size.patch
Patch2:      torque-%{version}-port-args.patch
# Fixes https://bugzilla.redhat.com/show_bug.cgi?id=1424149
Patch3:      torque-%{version}-fix-bad-crypto-check.patch
# From https://github.com/adaptivecomputing/torque/pull/148
Patch4:      torque-%{version}-remove-unused-header.patch

License:     OpenPBS and TORQUEv1.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:         http://www.adaptivecomputing.com/products/open-source/torque/
BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: pam-devel
BuildRequires: xauth
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gperf
BuildRequires: openssl-devel
BuildRequires: hwloc-devel
BuildRequires: libxml2-devel
BuildRequires: munge-devel
%if %{use_tcl}
BuildRequires: tcl-devel
%endif
%if %{build_gui}
BuildRequires: tk-devel
%endif


%{?systemd_requires}
BuildRequires: systemd

%if %{with docs}
%if 0%{?doxydoc}
BuildRequires:  graphviz
BuildRequires:  doxygen
%if 0%{?rhel} == 5
BuildRequires: graphviz-gd
%endif # end rhel5 check
BuildRequires:  texlive-tabu
BuildRequires:  tex(latex)
BuildRequires:  tex-xtab
BuildRequires:  tex-sectsty
BuildRequires:  tex-tocloft
BuildRequires:  tex-multirow
BuildRequires:  tex-adjustbox
%endif # end doxydoc check
BuildRequires:  tex(etoc.sty)
BuildRequires:  tex(hanging.sty)
BuildRequires:  tex(listofitems.sty)
BuildRequires:  tex(newunicodechar.sty)
BuildRequires:  tex(stackengine.sty)
BuildRequires:  tex(ulem.sty)
%endif # end docs check

Requires:        munge
Requires(post): /bin/grep /bin/cat /etc/services

%description
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds just a few shared files and directories.

%package         client
Summary:         Client part of TORQUE
Requires:        torque-libs%{_isa} = %{version}-%{release}
Requires(posttrans):  %{_sbindir}/alternatives
Requires(preun):      %{_sbindir}/alternatives

%description client
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the command-line client programs.

%if %{with docs}
%package docs
Summary:        Documentation files for TORQUE
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description docs
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the documentation files.
%endif

%package gui
Summary:      Graphical clients for TORQUE
Requires:     torque-client = %{version}-%{release}
Requires:     torque-libs%{_isa} = %{version}-%{release}

%description gui
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the graphical clients.

%package libs
Summary:      Run-time libs for programs which will use the %{name} library
Requires:     munge
Obsoletes:    libtorque  < 2.4.8-2
Provides:     libtorque = %{version}-%{release}
Requires:     munge

%description libs
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package includes the shared libraries necessary for running TORQUE 
programs.

%package devel
Summary:     Development tools for programs which will use the %{name} library
Requires:    torque-libs%{_isa} = %{version}-%{release}
Obsoletes:   libtorque-devel < 2.4.8-2
Provides:    libtorque-devel = %{version}-%{release}

%description devel
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package includes the header files and static libraries
necessary for developing programs which will use %{name}.

%package mom
Summary:        Node execution daemon for TORQUE
Requires:       torque-libs%{_isa} = %{version}-%{release}
Requires:       munge
%if ! %{use_rcp}
Requires:       openssh-clients
%endif

Requires(posttrans):  systemd
Requires(preun):      systemd








%description mom
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the execute daemon required on every node.

%package pam
Summary:    PAM module for TORQUE MOM nodes

%description pam
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

A simple PAM module to authorize users on PBS MOM nodes with a running job.

%package scheduler
Summary:         Simple fifo scheduler for TORQUE
Requires:        torque-libs%{_isa} = %{version}-%{release}

Requires(posttrans):  systemd
Requires(preun):      systemd






%description scheduler
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the fifo C scheduler.

%package server
Summary:           The main part of TORQUE
Requires:          torque-libs%{_isa} = %{version}-%{release}
Requires:          munge
%if ! %{use_rcp}
Requires:          openssh-server
%endif

Requires(posttrans):  systemd
Requires(preun):      systemd






%description server
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

This package holds the server.

%package drmaa
Summary:           Run time files for the drmaa interface
Requires:          torque-libs%{_isa} = %{version}-%{release}

%description drmaa
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

Run time files for working the DRMAA interface to torque.
DRMAA is "Distributed Resource Management Application API"


%package drmaa-devel
Summary:           Development files for the drmaa interface.
Requires:          torque-drmaa = %{version}-%{release}
Requires:          torque-devel = %{version}-%{release}

%description drmaa-devel
TORQUE (Tera-scale Open-source Resource and QUEue manager) is a resource 
manager providing control over batch jobs and distributed compute nodes.
TORQUE is based on OpenPBS version 2.3.12 and incorporates scalability,
fault tolerance, and feature extension patches provided by USC, NCSA, OSC,
the U.S. Dept of Energy, Sandia, PNNL, U of Buffalo, TeraGrid, and many
other leading edge HPC organizations.

Developement files for working the DRMAA interface to torque.
DRMAA is "Distributed Resource Management Application API"


%prep
%setup -q -n torque-%{version}
%patch1 -p 1
%patch2 -p 1
%patch3 -p 0
%patch4 -p 1
sed -i '/LATEX_BATCHMODE/d' src/drmaa/Doxyfile.in
install -pm 644 %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} \
   %{SOURCE6} %{SOURCE8} .
# rm x bit on some documentation.
chmod 644 torque.setup

%build
# -fpermissive added to downgrade numerous 'invalid conversion' errors to warnings
CFLAGS="%{optflags} -DUSE_INTERP_RESULT -DUSE_INTERP_ERRORLINE -fpermissive"
%configure --includedir=%{_includedir}/torque \
  --with-server-home=%{torquehomedir} --with-pam=/%{_lib}/security \
  --with-sendmail=%{_sbindir}/sendmail --disable-static \
  --with-tcp-retry-limit=2 --without-debug \
  --enable-drmaa --enable-munge-auth --with-munge \
  --enable-cpuset --enable-numa-support \
  %{server_nameflags} %{guiflags} %{tclflags} %{rcpflags}

make %{?_smp_mflags}

for daemon in pbs_mom pbs_sched pbs_server trqauthd
do
sed -i -e 's|^PBS_HOME=.*|PBS_HOME=%{torquehomedir}|' \
       -e 's|^PBS_DAEMON=.*|PBS_DAEMON=%{_sbindir}/'$daemon'|' \
       -e 's|chkconfig: 345|chkconfig: -|' \
       contrib/init.d/$daemon
done

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install

# remove files we don't need
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*/buildindex
rm -f %{buildroot}/%{_lib}/security/pam_pbssimpleauth.{a,la}
mkdir -p %{buildroot}%{_bindir}


# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/
install -p -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/
install -p -m 644 %{SOURCE22} %{buildroot}%{_unitdir}/
install -p -m 644 %{SOURCE23} %{buildroot}%{_unitdir}/









%if %{build_gui}
# This is really trivial, but cleans up an rpmlint warning
sed -i -e 's|%{_lib}/../||' %{buildroot}%{_bindir}/xpbs

desktop-file-install --dir %{buildroot}%{_datadir}/applications --vendor=adaptivecomputing.com xpbs.desktop
desktop-file-install --dir %{buildroot}%{_datadir}/applications --vendor=adaptivecomputing.com xpbsmon.desktop
install -d %{buildroot}%{_datadir}/pixmaps
install -p -m0644 xpbs.png xpbsmon.png %{buildroot}%{_datadir}/pixmaps
%endif

# alternatives stuff
for bin in qalter qdel qhold qrls qselect qstat qsub
do
    mv %{buildroot}%{_bindir}/$bin %{buildroot}%{_bindir}/${bin}-torque
    mv %{buildroot}%{_mandir}/man1/${bin}.1 \
       %{buildroot}%{_mandir}/man1/${bin}-torque.1
done

# Remove nodes file database since we don't want it in
# the package.
rm %{buildroot}/%{torquehomedir}/server_priv/nodes

# Relocate configuration files.
mkdir -p %{buildroot}%{_sysconfdir}/torque
pushd %{buildroot}%{torquehomedir}
mv pbs_environment %{buildroot}%{_sysconfdir}/torque
mv server_name %{buildroot}%{_sysconfdir}/torque
ln -s %{_sysconfdir}/torque/pbs_environment .
ln -s %{_sysconfdir}/torque/server_name .
popd

# Relocate mom_logs to /var/log
mkdir -p %{buildroot}%{_var}/log/torque
pushd %{buildroot}%{torquehomedir}
mv mom_logs %{buildroot}%{_var}/log/torque
ln -s %{_var}/log/torque/mom_logs .
popd

# Install mom_priv/config file to /etc/torque/mom
mkdir -p %{buildroot}%{_sysconfdir}/torque/mom
install -p -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/torque/mom/config
install -p -m 644 %{SOURCE24} %{buildroot}%{_sysconfdir}/torque/mom/mom.layout
pushd %{buildroot}%{torquehomedir}/mom_priv
ln -s %{_sysconfdir}/torque/mom/config .
ln -s %{_sysconfdir}/torque/mom/mom.layout .
popd

# Install sched_config files to /etc/torque/sched
mkdir -p %{buildroot}%{_sysconfdir}/torque/sched
pushd %{buildroot}%{torquehomedir}/sched_priv
for CONFIG in dedicated_time holidays resource_group sched_config ; do
  mv $CONFIG %{buildroot}%{_sysconfdir}/torque/sched/.
  ln -s %{_sysconfdir}/torque/sched/$CONFIG .
done
popd

# Relocate sched_logs to /var/log
pushd %{buildroot}%{torquehomedir}
mv sched_logs %{buildroot}%{_var}/log/torque
ln -s %{_var}/log/torque/sched_logs .
popd

# Relocate server_logs to /var/log
pushd %{buildroot}%{torquehomedir}
mv server_logs %{buildroot}%{_var}/log/torque
ln -s %{_var}/log/torque/server_logs .
popd


# Move drmaa man pages to correct place 
# and delete the three copies of the same documentation.

%if 0%{?doxydoc}
rm -f %{buildroot}%{_defaultdocdir}/torque-drmaa/man/man3/*_src_drmaa_src_.3
mv %{buildroot}%{_defaultdocdir}/torque-drmaa/man/man3/* %{buildroot}%{_mandir}/man3/.
rm -rf %{buildroot}%{_defaultdocdir}/torque-drmaa/html/*
rm -rf %{buildroot}%{_defaultdocdir}/torque-drmaa/latex/*
# Include drmaa.pdf later from the src tree.
rm %{buildroot}%{_defaultdocdir}/torque-drmaa/drmaa.pdf
%endif

#Remove man page for binary that is not included.
rm %{buildroot}%{_mandir}/man1/basl2c.1

# fix permissions for some directories in /var/lib/torque
chmod 755 `find %{buildroot}/var/lib/torque -type d`

# Use wrapper script for pbs-config and rename original script to include architecture name
mv %{buildroot}%{_bindir}/pbs-config %{buildroot}%{_bindir}/pbs-config-%{_arch}
install -m0755 -p %{SOURCE100} %{buildroot}%{_bindir}/pbs-config

%post
# fix mistake in previous release
sed -i '/pbs_mon/D' /etc/services
for srvs in pbs:15001 pbs_mom:15002 pbs_resmom:15003 pbs_sched:15004 ; do
  port=${srvs/*:/}
  srvs=${srvs/:*/}
  for proto in tcp udp ; do
    if ! grep -q $srvs'\W\W*'$port'/'$proto /etc/services;then
      cat<<__EOF__>>/etc/services
$srvs        $port/$proto
__EOF__
    fi
  done
done

%systemd_post trqauthd.service




%preun

%systemd_preun trqauthd.service







%posttrans client
/usr/sbin/alternatives --install %{_bindir}/qsub qsub %{_bindir}/qsub-torque 10 \
        --slave %{_mandir}/man1/qsub.1.gz qsub-man \
                %{_mandir}/man1/qsub-torque.1.gz \
        --slave %{_bindir}/qalter qalter %{_bindir}/qalter-torque \
        --slave %{_mandir}/man1/qalter.1.gz qalter-man \
                %{_mandir}/man1/qalter-torque.1.gz \
        --slave %{_bindir}/qdel qdel %{_bindir}/qdel-torque \
        --slave %{_mandir}/man1/qdel.1.gz qdel-man \
                %{_mandir}/man1/qdel-torque.1.gz \
        --slave %{_bindir}/qhold qhold %{_bindir}/qhold-torque \
        --slave %{_mandir}/man1/qhold.1.gz qhold-man \
                %{_mandir}/man1/qhold-torque.1.gz \
        --slave %{_bindir}/qrls qrls %{_bindir}/qrls-torque \
        --slave %{_mandir}/man1/qrls.1.gz qrls-man \
                %{_mandir}/man1/qrls-torque.1.gz \
        --slave %{_bindir}/qselect qselect %{_bindir}/qselect-torque \
        --slave %{_mandir}/man1/qselect.1.gz qselect-man \
                %{_mandir}/man1/qselect-torque.1.gz \
        --slave %{_bindir}/qstat qstat %{_bindir}/qstat-torque \
        --slave %{_mandir}/man1/qstat.1.gz qstat-man \
                %{_mandir}/man1/qstat-torque.1.gz

%preun client
if [ $1 -eq 0 ]; then
  /usr/sbin/alternatives --remove qsub %{_bindir}/qsub-torque
fi

%ldconfig_scriptlets   libs
%ldconfig_scriptlets   drmaa

%pre mom
if test -f %{torquehomedir}/mom_priv/mom.layout ; then
  if ! test -h %{torquehomedir}/mom_priv/mom.layout ; then
    mkdir -p %{_sysconfdir}/torque/mom
    cp -p %{torquehomedir}/mom_priv/mom.layout %{_sysconfdir}/torque/mom/
  fi
fi

%post mom

%systemd_post pbs_mom.service




%preun mom

%systemd_preun pbs_mom.service







%post scheduler

%systemd_post pbs_sched.service




%preun scheduler

%systemd_preun pbs_sched.service







%post server

%systemd_post pbs_server.service




%preun server

%systemd_preun pbs_server.service







%files
%doc               README.torque torque.setup Release_Notes 
%doc               CHANGELOG PBS_License.txt README.Fedora contrib/PBS_License_2.3.txt
%dir %{torquehomedir} 
%dir %{torquehomedir}/aux
%attr (1777,root,root) %{torquehomedir}/spool
%attr (1777,root,root) %{torquehomedir}/undelivered
%attr (1777,root,root) %{torquehomedir}/checkpoint
%dir %{torquehomedir}/spool
%dir %{torquehomedir}/undelivered
%{torquehomedir}/checkpoint
%{torquehomedir}/pbs_environment
%{torquehomedir}/server_name
%config(noreplace) %{_sysconfdir}/torque/pbs_environment
%config(noreplace) %{_sysconfdir}/torque/server_name
%{_mandir}/man1/pbs.1.*
%attr(0755, root, root) %{_sbindir}/trqauthd

%{_unitdir}/trqauthd.service




%files client
%{_bindir}/q*
%{_bindir}/chk_tree
%{_bindir}/hostn
%{_bindir}/nqs2pbs
%{_bindir}/pbsdsh
%{_bindir}/pbsnodes
%{_bindir}/printjob
%{_bindir}/printserverdb
%{_bindir}/printtracking
%{_bindir}/tracejob
%{_sbindir}/pbs_demux
%if %{use_tcl}
%{_bindir}/pbs_tclsh
%endif
%{_mandir}/man1/nqs2pbs.1.*
%{_mandir}/man1/pbsdsh.1.*
%{_mandir}/man1/qchkpt.1.*
%{_mandir}/man1/qmgr.1.*
%{_mandir}/man1/qmove.1.*
%{_mandir}/man1/qmsg.1.*
%{_mandir}/man1/qorder.1.*
%{_mandir}/man1/qrerun.1.*
%{_mandir}/man1/qsig.1.*
%{_mandir}/man1/qgpumode.1.gz
%{_mandir}/man1/qgpureset.1.gz
%{_mandir}/man8/pbsnodes.8.*
%{_mandir}/man8/qdisable.8.*
%{_mandir}/man8/qenable.8.*
%{_mandir}/man8/qrun.8.*
%{_mandir}/man8/qstart.8.*
%{_mandir}/man8/qstop.8.*
%{_mandir}/man8/qterm.8.*
%{_mandir}/man7/pbs_job_attributes.7.*
%{_mandir}/man7/pbs_queue_attributes.7.*
%{_mandir}/man7/pbs_resources.7.*
%{_mandir}/man7/pbs_resources_aix4.7.*
%{_mandir}/man7/pbs_resources_aix5.7.*
%{_mandir}/man7/pbs_resources_darwin.7.*
%{_mandir}/man7/pbs_resources_digitalunix.7.*
%{_mandir}/man7/pbs_resources_freebsd.7.*
%{_mandir}/man7/pbs_resources_fujitsu.7.*
%{_mandir}/man7/pbs_resources_hpux10.7.*
%{_mandir}/man7/pbs_resources_hpux11.7.*
%{_mandir}/man7/pbs_resources_irix5.7.*
%{_mandir}/man7/pbs_resources_irix6.7.*
%{_mandir}/man7/pbs_resources_irix6array.7.*
%{_mandir}/man7/pbs_resources_linux.7.*
%{_mandir}/man7/pbs_resources_netbsd.7.*
%{_mandir}/man7/pbs_resources_solaris5.7.*
%{_mandir}/man7/pbs_resources_solaris7.7.*
%{_mandir}/man7/pbs_resources_sp2.7.*
%{_mandir}/man7/pbs_resources_sunos4.7.*
%{_mandir}/man7/pbs_resources_unicos8.7.*
%{_mandir}/man7/pbs_resources_unicosmk2.7.*
%{_mandir}/man7/pbs_server_attributes.7.*

# And the following are alternative managed ones.
%{_mandir}/man1/qsub-torque.1.*
%{_mandir}/man1/qalter-torque.1.*
%{_mandir}/man1/qdel-torque.1.*
%{_mandir}/man1/qhold-torque.1.*
%{_mandir}/man1/qrls-torque.1.*
%{_mandir}/man1/qselect-torque.1.*
%{_mandir}/man1/qstat-torque.1.*

%if %{with docs}
%files docs
%doc doc/admin_guide.ps
%if 0%{?doxydoc}
%doc src/drmaa/drmaa.pdf
%endif
%endif

%if %{build_gui}
%files gui
%{_bindir}/pbs_wish
%{_bindir}/xpbs
%{_bindir}/xpbsmon
%{_libdir}/xpbs
%{_libdir}/xpbsmon
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/xpbs.1.*
%{_mandir}/man1/xpbsmon.1.*
%endif

%files libs
%{_libdir}/libtorque.so.*

%files devel
%{_libdir}/libtorque.so
%{_includedir}/torque
%exclude %{_includedir}/torque/drmaa.h
%{_bindir}/pbs-config
%{_bindir}/pbs-config-%{_arch}
%{_mandir}/man3/pbs_alterjob.3.*
%{_mandir}/man3/pbs_connect.3.*
%{_mandir}/man3/pbs_default.3.*
%{_mandir}/man3/pbs_deljob.3.*
%{_mandir}/man3/pbs_disconnect.3.*
%{_mandir}/man3/pbs_geterrmsg.3.*
%{_mandir}/man3/pbs_holdjob.3.*
%{_mandir}/man3/pbs_locate.3.*
%{_mandir}/man3/pbs_manager.3.*
%{_mandir}/man3/pbs_movejob.3.*
%{_mandir}/man3/pbs_msgjob.3.*
%{_mandir}/man3/pbs_orderjob.3.*
%{_mandir}/man3/pbs_rerunjob.3.*
%{_mandir}/man3/pbs_rescquery.3.*
%{_mandir}/man3/pbs_rescreserve.3.*
%{_mandir}/man3/pbs_rlsjob.3.*
%{_mandir}/man3/pbs_runjob.3.*
%{_mandir}/man3/pbs_selectjob.3.*
%{_mandir}/man3/pbs_selstat.3.*
%{_mandir}/man3/pbs_sigjob.3.*
%{_mandir}/man3/pbs_stagein.3.*
%{_mandir}/man3/pbs_statjob.3.*
%{_mandir}/man3/pbs_statnode.3.*
%{_mandir}/man3/pbs_statque.3.*
%{_mandir}/man3/pbs_statserver.3.*
%{_mandir}/man3/pbs_submit.3.*
%{_mandir}/man3/pbs_terminate.3.*
%{_mandir}/man3/pbs_checkpointjob.3.gz
%{_mandir}/man3/pbs_fbserver.3.gz
%{_mandir}/man3/pbs_get_server_list.3.gz
%{_mandir}/man3/pbs_gpumode.3.gz
%{_mandir}/man3/pbs_gpureset.3.gz
%{_mandir}/man3/tm.3.*

%files mom
%{_sbindir}/momctl
%{_sbindir}/pbs_mom
%{_sbindir}/qnoded
%{_sbindir}/pbs_demux
%{_bindir}/pbs_track

%{_unitdir}/pbs_mom.service



%if %{use_rcp}
%attr(4755, root, root) %{_sbindir}/pbs_rcp
%endif
%{torquehomedir}/mom_priv
%{torquehomedir}/mom_logs
%dir %{_var}/log/torque
%dir %{_var}/log/torque/mom_logs
%dir %{_sysconfdir}/torque/mom
%{_mandir}/man8/pbs_mom.8.*
%config(noreplace) %{_sysconfdir}/torque/mom/config
%config(noreplace) %{_sysconfdir}/torque/mom/mom.layout

%files pam
%doc src/pam/README.pam
/%{_lib}/security/pam_pbssimpleauth.so

%files scheduler
%attr(0755, root, root) %{_sbindir}/pbs_sched
%{_sbindir}/qschedd

%{_unitdir}/pbs_sched.service



%dir %{torquehomedir}/sched_priv
%config(noreplace) %{torquehomedir}/sched_priv/*
%{torquehomedir}/sched_logs
%dir %{_var}/log/torque/sched_logs
%dir %{_sysconfdir}/torque/sched
%{_mandir}/man8/pbs_sched.8.*
%{_mandir}/man8/pbs_sched_basl.8.*
%{_mandir}/man8/pbs_sched_cc.8.*
%{_mandir}/man8/pbs_sched_tcl.8.*
%config(noreplace) %{_sysconfdir}/torque/sched/dedicated_time 
%config(noreplace) %{_sysconfdir}/torque/sched/holidays 
%config(noreplace) %{_sysconfdir}/torque/sched/resource_group 
%config(noreplace) %{_sysconfdir}/torque/sched/sched_config 

%files server
%attr(0755, root, root) %{_sbindir}/pbs_server
%{_sbindir}/qserverd

%{_unitdir}/pbs_server.service



%dir %{_var}/log/torque/server_logs
%{torquehomedir}/server_logs
%{torquehomedir}/server_priv
%{_mandir}/man8/pbs_server.8.*

%files drmaa
%{_libdir}/libdrmaa.so.*

%files drmaa-devel
%{_libdir}/libdrmaa.so
%{_includedir}/torque/drmaa.h
%if 0%{?doxydoc}
%{_mandir}/man3/compat.h.3.*
%{_mandir}/man3/drmaa.3.*
%{_mandir}/man3/drmaa.h.3.*
%{_mandir}/man3/drmaa_attr_names_s.3.*
%{_mandir}/man3/drmaa_attr_values_s.3.*
%{_mandir}/man3/drmaa_attrib.3.*
%{_mandir}/man3/drmaa_attrib_info_s.3.*
%{_mandir}/man3/drmaa_submission_context_s.3.*
%{_mandir}/man3/drmaa_job_ids_s.3.*
%{_mandir}/man3/drmaa_def_attr_s.3.*
%{_mandir}/man3/pbs_attrib.3.*
%{_mandir}/man3/drmaa_viter.3.*
%{_mandir}/man3/drmaa_job_iter_s.3.*
%{_mandir}/man3/drmaa_job_s.3.*
%{_mandir}/man3/drmaa_job_template_s.3.*
%{_mandir}/man3/drmaa_jobt.3.*
%{_mandir}/man3/drmaa_session.3.*
%{_mandir}/man3/drmaa_session_s.3.*
%{_mandir}/man3/error.h.3.*
%{_mandir}/man3/jobs.3.*
%{_mandir}/man3/jobs.h.3.*
%{_mandir}/man3/lookup3.h.3.*
%endif

%changelog
* Mon Jun 14 2021 Thomas Crain <thcrain@microsoft.com> - 4.2.10-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Conditionally build documentation
- Correct the location of grep, cat in requirements

* Thu Jul  9 2020 Tom Callaway <spot@fedoraproject.org> - 4.2.10-26
- improve -libs Requires

* Thu Jul  2 2020 Tom Callaway <spot@fedoraproject.org> - 4.2.10-25
- resolve multilib conflict on pbs-config script

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep  3 2019 Tom Callaway <spot@fedoraproject.org> - 4.2.10-23
- revive

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.2.10-21
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.10-19
- Adjust dependencies for install requirements, few cleanups

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.2.10-17
- Remove old Requires

* Thu Jan 11 2018 Merlin Mathesius <mmathesi@redhat.com> - 4.2.10-16
- Cleanup spec file conditionals
- Fix FTBFS (BZ#1424149)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.2.10-12
- Rebuild for readline 7.x

* Thu Oct 20 2016 Orion Poplawski <orion@cora.nwra.com> - 4.2.10-11
- Make libs sub-package not require main package (bug #1333489)

* Fri Apr 8 2016 David Brown <david.brown@pnnl.gov> - 4.2.10-10
- Resolve systemd requires for bug #1319195
- add sample mom.layout file as an example

* Fri Feb 19 2016 David Brown <david.brown@pnnl.gov> - 4.2.10-9
- Resolve dependencies for rawhide (#1308192)
- Fix port and args environment variables for el5/6 (#1254301)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 06 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-8
- Resolve momctl into the right package

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 4.2.10-7
- Remove AppStream metadata file as it's no longer used.

* Mon Aug 17 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-6
- enable numa support bug #1231148

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 6 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-4
- Bugfix - #1227003 test system in cluster environment
- Bugfix - #1216049 add --enable-cpuset and hwloc
- Bugfix - #1176080 this maybe a duplicate of #1216037

* Tue May 19 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-3
- Bugfix - #1215207 create/install service files for these
- Bugfix - #1117263 qmgr aborts in some instances
- Bugfix - #1144396 Hey! Version Bump!
- Bugfix - #1215992 more service scripts
- Bugfix - #1216037 fixed permissions on directories
- Bugfix - #1149045 hopefully these are all fixed now
- Bugfix - #965513 calling this one fixed...

* Fri Apr 24 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-2
- Bugfix - #1154413 make manipulating services better.

* Mon Apr 6 2015 David Brown <david.brown@pnnl.gov> - 4.2.10-1
- Updated upstream version

* Thu Apr 2 2015 David Brown <david.brown@pnnl.gov> - 4.2.8-3
- Version bump to merge from previous version

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 4.2.8-2
- Add an AppData file for the software center

* Tue Oct 14 2014 David Brown <david.brown@pnnl.gov> - 4.2.8-2
- merged fedora latest into epel
- This breaks old configs and should be treated carefully

* Wed Oct 01 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 3.0.4-6
- Fix CVE-2013-4319 (RHBZ #1005918, #1005919)

* Fri Sep 05 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 3.0.4-5
- Fix CVE-2013-4495 (RHBZ #1029752)

* Mon Sep 01 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 4.2.8-1
- upstream 4.2.8

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.2.6.1-5
- Reflect upstream URL and Source0 having changed.

* Thu Jul 17 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.2.6.1-4
- Append -DUSE_INTERP_RESULT -DUSE_INTERP_ERRORLINE to CFLAGS to work-around
  Tcl/Tk-8.6 incompatibilities (FTFFS RHBZ#1107455).
- Pass --without-debug to %%configure to let configure pass through
  %%optflags (RHBZ#1074571).
- Fix twice listed files in *-devel.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sun Jan 12 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 4.2.6.1-1
- upstream 4.2.6.1

* Wed Nov 13 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 4.2.6-1
- upstream 4.2.6

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> - 3.0.4-4
- Add missing BRs for latex docs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 5 2012 Steve Traylen <steve.traylen@cern.ch> - 3.0.4-1
- New upstream.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 3 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-9
- Add torque-2.5.7-rhbz#759141-r5167-pbs_server-crash.patch

* Mon Nov 21 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-8
- Add torque-rhbz#758740-r5258-dis-close.patch and
  torque-rhbz#758740-r5270-dis-array.patch

* Mon Nov 21 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-7
- Add torque-fix-munge-rhbz#752079-PTII.patch

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.3-2
- Empty release for release mistake.

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.3-1
- New upstream.

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-6
- Empty release for release mistake.

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-5
- Add patch torque-fix-munge-rhbz#752079.patch

* Sun Oct  9 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.2-4
- Add patch torque-initd-hangs-rhbz-744138.patch

* Sun Oct  9 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-4
- Add patch torque-initd-hangs-rhbz-744138.patch

* Mon Sep 19 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.2-3
- Add --with-tcp-retry-limit=2 to build, rhbz#738576.

* Mon Sep 19 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-3
- Add --with-tcp-retry-limit=2 to build, rhbz#738576.

* Wed Aug 31 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-2
- Move checkpoint directory from torque-mom to torque package.
  rhbz#734878.

* Tue Aug 30 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.2-2
- Move checkpoint directory from torque-mom to torque package.
  rhbz#734878.

* Tue Jul 26 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.7-1
- Update to 2.5.7, drop torque-buffer-overrun-2.5.5.patch,
  Add man pages for: qgpumod, qgpureset, pbs_gpumode and 
  pbs_gpureset.
- Add or rather force munge support, Add torque-munge-size.patch.

* Mon Jun 27 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.2-1
- Update to 3.0.2.
- Remove torque-buffer-overrun since upstream now.

* Sun Jun 26 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.1-4
- Removes nodes database file from package rhbz#716659

* Sun Jun 26 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-3
- Removes nodes database file from package rhbz#716659

* Fri Jun 17 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.1-3
- Add torque-munge-size.patch, rhbz#713996, Alex Chernyakhovsky

* Wed Jun 8 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-2
- Add torque-buffer-overrun.patch rhbz#711463

* Wed Jun 8 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.1-2
- Add torque-buffer-overrun.patch patch, rhbz#711463

* Thu Apr 21 2011 Steve Traylen <steve.traylen@cern.ch> - 3.0.1-1
- Update to 3.0.1.
  License file name change.
- Renable doxygen documentation for drmaa.

* Tue Mar 8 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.5-1
- New upstream 2.5.5
  Drop torque-create-request.patch since fixed upstream.
- Torque License change, 
    PBS_License.txt now contrib/PBS_License2.3.txt 
    New additional license file PBS_License_2.5.txt
  License field changed from OpenPBS to "OpenPBS and TORQUEv1.1"

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0_snap.201102011355-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 9 2011 Steve Traylen <steve.traylen@cern.ch> - 2.5.4-1
- New upstream 2.5.4
  Drop patches: torque-cond-touch.patch rhbz#528060 and
  torque-start-start.patch rhbz#643194 since both upstream.

* Fri Dec 10 2010 Steve Traylen <steve.traylen@cern.ch> - 3.0.0-snap.201102011355-1
- Update to 3.0.0-snap.201102011355-1.
- Drop torque-create-request.patch since upstream.
- License change to "OpenPBS and TORQUEv1.1" from OpenPBS.

* Fri Dec 10 2010 Steve Traylen <steve.traylen@cern.ch> - 3.0.0-2
- Enable or rather force munge support.

* Thu Dec 9 2010 Steve Traylen <steve.traylen@cern.ch> - 3.0.0-1
- New upstream 3.0.0. Drop patches torque-cond-touch.patch and
  torque-start-start.patch since both upstream now.

* Wed Dec 8 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.3-3
- Remove own copy of pbs-config. #657027
- Move man pages from doc subpackage to relavent sub package.
- Enable drmaa support and add drmaa sub packages.

* Wed Dec 8 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.3-2
- Only build noarch doc package on RHEL6 or Fedora10. #659723

* Thu Nov 18 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.3-1
- Upstream to 2.5.3.

* Thu Oct 14 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.2-4
- rhbz#643194, stop a stoped service, start a start service 
  return codes now fixed.

* Thu Oct 14 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.2-3
- rhbz#631256 Only create db if asked to.

* Thu Oct 14 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.2-2
- rhbz#58060, add torque-cond-touch.spec to only touch files
  when service actually starts.

* Tue Sep 7 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.2-1
- New upstream 2.5.2
- Three new man pages added to file listing.

* Tue Aug 10 2010 Steve Traylen <steve.traylen@cern.ch> - 2.5.1-1
- New upstream 2.5.1

* Wed Jul 14 2010 Steve Traylen <steve.traylen@cern.ch> - 2.4.8-3
- Rebuild for cvs mistake.

* Thu Jul 1 2010 Steve Traylen <steve.traylen@cern.ch> - 2.4.8-2
- Set torquehome to /var/lib/torque rather than /var/torque
- Drop provides and obsoletes since never present in Fedora/EPEL.
- Don't use a variable for the description.
- Split install of init.d scripts to build and install sections
  as appropriate.
- Mark docs subpackage as noarch.
- Rename libtorque package to more normal torque-libs package.
- Rename libtorque-devel package to more normal torque-devel package.
- Remove the unused epoch and snapshot variables.
- Have mom requires openssh-clients and server openssh-server
- Have mom, sched and server log to /var/log/torque and symlinks
- Move configurtion files to /etc/torque and symlink in expected.
- Be more explicit about man page in the files section.
- Rename README-localhost to README.Fedora to make it more obvious
  it's related to this package.

* Wed Jun  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.4.8-1
- update to 2.4.8
- drop static libs
- cleanup spec file

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 16 2008 Garrick Staples <garrick@usc.edu> 2.1.10-6
- add alternatives system

* Thu Feb 14 2008 Garrick Staples <garrick@usc.edu> 2.1.10-5
- fix missing NI_MAXSERV on fedora9

* Thu Jan  3 2008 Garrick Staples <garrick@usc.edu> 2.1.10-4
- correct pbs-config build typo

* Thu Jan  3 2008 Garrick Staples <garrick@usc.edu> 2.1.10-3
- rebuild because tcl was bumped

* Thu Dec 13 2007 Garrick Staples <garrick@usc.edu> 2.1.10-2
- fix multilib conflicts

* Wed Dec 12 2007 Garrick Staples <garrick@usc.edu> 2.1.10-1
- bump to 2.1.10

* Wed Oct  3 2007 Garrick Staples <garrick@usc.edu> 2.1.9-1
- bump to 2.1.9

* Fri Aug 31 2007 Garrick Staples <garrick@usc.edu> 2.1.8-3
- correct License tag

* Wed Aug 15 2007 Garrick Staples <garrick@usc.edu> 2.1.8-2
- correct errors in desktop entry files

* Tue Mar 13 2007 Garrick Staples <garrick@usc.edu> 2.1.8-1
- bump to 2.1.8
- ensure daemons have the correct path to sendmail
- don't need rpath configure patch anymore

* Wed Feb 14 2007 Garrick Staples <garrick@usc.edu> 2.1.6-5
- rebuilding because tcl8.5 was downgraded to tcl8.4

* Tue Feb  6 2007 Garrick Staples <garrick@usc.edu> 2.1.6-4
- rebuilding with new tcl

* Sat Feb  3 2007 Garrick Staples <garrick@usc.edu> 2.1.6-3
- trying to resolve tcl8.5 buildindex issue

* Fri Feb  2 2007 Garrick Staples <garrick@usc.edu> 2.1.6-2
- rebuild for tcl8.5

* Tue Oct 24 2006 Garrick Staples <garrick@usc.edu> 2.1.6-1
- fixes more regressions from Friday

* Sat Oct 21 2006 Garrick Staples <garrick@usc.edu> 2.1.5-1
- fixes "qsub -o /dev/null" regression

* Fri Oct 20 2006 Garrick Staples <garrick@usc.edu> 2.1.4-1
- bump to fix "Spool Job Race condition" on bugtraq

* Mon Oct 16 2006 Garrick Staples <garrick@usc.edu> 2.1.3-3
- correct unowned directories

* Thu Oct 12 2006 Garrick Staples <garrick@usc.edu> 2.1.3-2
- missing BR ncurses-devel and readline-devel

* Thu Oct 12 2006 Garrick Staples <garrick@usc.edu> 2.1.3-1
- bump to 2.1.3

* Sun Aug 27 2006 Garrick Staples <garrick@usc.edu> 2.1.2-3
- FC6 mass rebuild

* Wed Aug  2 2006 Garrick Staples <garrick@usc.edu> 2.1.2-2
- fix incorrect _pam_getpwnam_r usage in pam module

* Tue Aug  1 2006 Garrick Staples <garrick@usc.edu> 2.1.2-1
- bump to 2.1.2
- fix bz #200830
- enable new pam module

* Thu Jun 22 2006 Garrick Staples <garrick@usc.edu> 2.1.1-3
- rebuild

* Thu Jun 22 2006 Garrick Staples <garrick@usc.edu> 2.1.1-2
- rebuild with added README-localhost

* Thu Jun 22 2006 Garrick Staples <garrick@usc.edu> 2.1.1-1
- bump to 2.1.1

* Mon May 15 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-3
- get rid of the annoying "localhost only" package

* Fri May 12 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-2
- fix pbs_server segfault when mom_job_sync is enabled

* Thu May 11 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-1
- bump to final release

* Tue Apr 25 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.11.200604251602cvs
- bump to fix "mem" job resources for non-serial jobs
- rm.h is now installed

* Fri Apr 21 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.10.200604211036cvs
- bump

* Fri Apr 21 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.9.200604171430cvs
- fix qsub write return check

* Thu Apr 20 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.8.200604171430cvs
- fix pbs_sched error opening lockfile and immediately exiting

* Mon Apr 17 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.7.200604171430cvs
- importing to fedora extras

* Mon Apr 17 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.6.200604171430cvs
- add %%{dist} tag
- cleanup the cleanups in spec
- bump to matching upstream
- move headers to /usr/include/torque/

* Wed Apr 12 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.5.200604071240cvs
- remove rpath

* Tue Apr 11 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.4.200604071240cvs
- fix release string to match fedora guidelines

* Fri Apr  7 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.3.200604071240
- spec and initscript cleanups

* Wed Apr  5 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.2.200604051756
- add .desktop files

* Wed Apr  5 2006 Garrick Staples <garrick@usc.edu> 2.1.0p0-0.1.200604051756
- Initial package for Fedora Extras


