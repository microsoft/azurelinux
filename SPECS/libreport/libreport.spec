# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
  %bcond_with bugzilla

  %define dbus_devel dbus-1-devel
  %define libjson_devel libjson-devel
%else
  %bcond_without bugzilla

  %define dbus_devel dbus-devel
  %define libjson_devel json-c-devel
%endif

%define glib_ver 2.43.4

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.17.15
Release: 9%{?dist}
License: GPL-2.0-or-later
URL: https://abrt.readthedocs.org/
Source: https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires: %{dbus_devel}
BuildRequires: gtk3-devel
BuildRequires: curl-devel
BuildRequires: desktop-file-utils
BuildRequires: python3-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: make
BuildRequires: texinfo
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: newt-devel
BuildRequires: satyr-devel >= 0.38
BuildRequires: glib2-devel >= %{glib_ver}
BuildRequires: git-core

%if 0%{?fedora} >= 24 || 0%{?rhel} > 7
# A test case uses zh_CN locale to verify XML event translations
BuildRequires: glibc-all-langpacks
%endif

%if %{with bugzilla}
BuildRequires: xmlrpc-c-devel
%endif
BuildRequires: doxygen
BuildRequires: systemd-devel
BuildRequires: augeas-devel
BuildRequires: augeas
BuildRequires: libarchive-devel
Requires: libreport-filesystem = %{version}-%{release}
Requires: satyr%{?_isa} >= 0.38
Requires: glib2%{?_isa} >= %{glib_ver}
Requires: libarchive%{?_isa}

# Required for the temporary modularity hack, see below
%if 0%{?_module_build}
BuildRequires: sed
%endif

Obsoletes: %{name}-compat < 2.13.2
Obsoletes: %{name}-plugin-rhtsupport < 2.13.2
Obsoletes: %{name}-rhel < 2.13.2

%description
Libraries providing API for reporting different problems in applications
to different bug targets like Bugzilla, ftp, trac, etc...

%package filesystem
Summary: Filesystem layout for libreport
BuildArch: noarch

%description filesystem
Filesystem layout for libreport

%package devel
Summary: Development libraries and headers for libreport
Requires: libreport = %{version}-%{release}

%description devel
Development libraries and headers for libreport

%package web
Summary: Library providing network API for libreport
Requires: libreport = %{version}-%{release}

%description web
Library providing network API for libreport

%package web-devel
Summary: Development headers for libreport-web
Requires: libreport-web = %{version}-%{release}

%description web-devel
Development headers for libreport-web

%package -n python3-libreport
Summary: Python 3 bindings for report-libs
%if 0%{?_module_build}
# This is required for F26 Boltron (the modular release)
# Different parts of libreport are shipped with different
# modules with different dist tags; we need to weaken the
# strict NVR dependency to make it work.  Temporary and
# limited to F26 Boltron.
%global distfreerelease %(echo %{release}|sed 's/%{?dist}$//'||echo 0)
Requires: libreport >= %{version}-%{distfreerelease}
%else
Requires: libreport = %{version}-%{release}
%endif
Requires: python3-dnf
Requires: python3-requests
Requires: python3-urllib3
%{?python_provide:%python_provide python3-libreport}

%description -n python3-libreport
Python 3 bindings for report-libs.

%package cli
Summary: %{name}'s command line interface
Requires: %{name} = %{version}-%{release}

%description cli
This package contains simple command line tool for working
with problem dump reports

%package newt
Summary: %{name}'s newt interface
Requires: %{name} = %{version}-%{release}
Provides: report-newt = 0:0.23-1
Obsoletes: report-newt < 0:0.23-1

%description newt
This package contains a simple newt application for reporting
bugs

%package gtk
Summary: GTK front-end for libreport
Requires: libreport = %{version}-%{release}
Requires: libreport-plugin-reportuploader = %{version}-%{release}
Provides: report-gtk = 0:0.23-1
Obsoletes: report-gtk < 0:0.23-1

%description gtk
Applications for reporting bugs using libreport backend

%package gtk-devel
Summary: Development libraries and headers for libreport
Requires: libreport-gtk = %{version}-%{release}

%description gtk-devel
Development libraries and headers for libreport-gtk

%package plugin-kerneloops
Summary: %{name}'s kerneloops reporter plugin
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-kerneloops
This package contains plugin which sends kernel crash information to specified
server, usually to kerneloops.org.

%package plugin-logger
Summary: %{name}'s logger reporter plugin
Requires: %{name} = %{version}-%{release}

%description plugin-logger
The simple reporter plugin which writes a report to a specified file.

%package plugin-systemd-journal
Summary: %{name}'s systemd journal reporter plugin
Requires: %{name} = %{version}-%{release}

%description plugin-systemd-journal
The simple reporter plugin which writes a report to the systemd journal.

%package plugin-mailx
Summary: %{name}'s mailx reporter plugin
Requires: %{name} = %{version}-%{release}
Requires: /usr/bin/mailx

%description plugin-mailx
The simple reporter plugin which sends a report via mailx to a specified
email address.

%if %{with bugzilla}
%package plugin-bugzilla
Summary: %{name}'s bugzilla plugin
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}
Requires: python3-libreport = %{version}-%{release}
%if 0%{?fedora} >= 38
Requires: python3-satyr
Suggests: python3-pytest
Suggests: python3-vcrpy
%endif



%description plugin-bugzilla
Plugin to report bugs into the bugzilla.
%endif

%package plugin-mantisbt
Summary: %{name}'s mantisbt plugin
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-mantisbt
Plugin to report bugs into the mantisbt.

%package centos
Summary: %{name}'s CentOS Bug Tracker workflow
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}
Requires: libreport-plugin-mantisbt = %{version}-%{release}

%description centos
Workflows to report issues into the CentOS Bug Tracker.

%package plugin-ureport
Summary: %{name}'s micro report plugin
BuildRequires: %{libjson_devel}
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-ureport
Uploads micro-report to abrt server

%package plugin-reportuploader
Summary: %{name}'s reportuploader plugin
Requires: %{name} = %{version}-%{release}
Requires: libreport-web = %{version}-%{release}

%description plugin-reportuploader
Plugin to report bugs into anonymous FTP site associated with ticketing system.

%if 0%{?fedora} || 0%{?eln}
%package fedora
Summary: Default configuration for reporting bugs via Fedora infrastructure
Requires: %{name} = %{version}-%{release}

%description fedora
Default configuration for reporting bugs via Fedora infrastructure
used to easily configure the reporting process for Fedora systems. Just
install this package and you're done.
%endif

%if 0%{?rhel} && ! 0%{?eln}
%package rhel-bugzilla
Summary: Default configuration for reporting bugs to Red Hat Bugzilla
Requires: %{name} = %{version}-%{release}
Requires: libreport-plugin-bugzilla = %{version}-%{release}
Requires: libreport-plugin-ureport = %{version}-%{release}

%description rhel-bugzilla
Default configuration for reporting bugs to Red Hat Bugzilla used to easily
configure the reporting process for Red Hat systems. Just install this package
and you're done.

%package rhel-anaconda-bugzilla
Summary: Default configuration for reporting anaconda bugs to Red Hat Bugzilla
Requires: %{name} = %{version}-%{release}
Requires: libreport-plugin-bugzilla = %{version}-%{release}

%description rhel-anaconda-bugzilla
Default configuration for reporting Anaconda problems to Red Hat Bugzilla used
to easily configure the reporting process for Red Hat systems. Just install this
package and you're done.
%endif

%if %{with bugzilla}
%package anaconda
Summary: Default configuration for reporting anaconda bugs
Requires: %{name} = %{version}-%{release}
Requires: libreport-plugin-reportuploader = %{version}-%{release}
%if ! 0%{?rhel} || 0%{?eln}
Requires: libreport-plugin-bugzilla = %{version}-%{release}
%endif

%description anaconda
Default configuration for reporting Anaconda problems or uploading the gathered
data over ftp/scp...
%endif

%prep
%autosetup

%build
./autogen.sh

%configure \
%if %{without bugzilla}
        --without-bugzilla \
%endif
        --enable-doxygen-docs \
        --disable-silent-rules

%make_build

%install
%make_install \
%if %{with python3}
             PYTHON=%{__python3} \
%endif
             mandir=%{_mandir}

%find_lang %{name}

# Remove byte-compiled python files generated by automake.
# automake uses system's python for all *.py files, even
# for those which needs to be byte-compiled with different
# version (python2/python3).
# rpm can do this work and use the appropriate python version.
find %{buildroot} -name "*.py[co]" -delete

# remove all .la and .a files
find %{buildroot} -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events.d/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/events/
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/workflows.d/
mkdir -p %{buildroot}/%{_datadir}/%{name}/events/
mkdir -p %{buildroot}/%{_datadir}/%{name}/workflows/

# After everything is installed, remove info dir
rm -f %{buildroot}/%{_infodir}/dir

# Remove unwanted Fedora specific workflow configuration files
%if ! 0%{?fedora} && ! 0%{?eln}
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraPython3.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraVmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraXorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_FedoraJavaScript.xml
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_fedora.conf
rm -f %{buildroot}%{_mandir}/man5/report_fedora.conf.5
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaFedora.xml
%endif

# Remove unwanted RHEL specific workflow configuration files
%if ! 0%{?rhel} || 0%{?eln}
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_uReport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaRHELBugzilla.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaVmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaXorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELBugzillaJavaScript.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDatavmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataxorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELAddDataJavaScript.xml
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_uReport.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel_bugzilla.conf
rm -f %{buildroot}%{_mandir}/man5/report_uReport.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_rhel_bugzilla.conf.5
%endif

%if 0%{?fedora} >= 38
    mv %{buildroot}/%{_bindir}/reporter-bugzilla-python %{buildroot}/%{_bindir}/reporter-bugzilla
%endif

%check
make check|| {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}

%ldconfig_scriptlets
%ldconfig_scriptlets web
%if 0%{?rhel} && 0%{?rhel} <= 7
%post gtk
%{?ldconfig}
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gtk
%{?ldconfig}
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gtk
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%endif

%files -f %{name}.lang
%doc README.md
%license COPYING
%config(noreplace) %{_sysconfdir}/%{name}/libreport.conf
%config(noreplace) %{_sysconfdir}/%{name}/report_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/forbidden_words.conf
%config(noreplace) %{_sysconfdir}/%{name}/ignored_words.conf
%config(noreplace) %{_sysconfdir}/%{name}/ignored_elements.conf
%{_datadir}/%{name}/conf.d/libreport.conf
%{_libdir}/libreport.so.*
%{_mandir}/man5/libreport.conf.5*
%{_mandir}/man5/report_event.conf.5*
%{_mandir}/man5/forbidden_words.conf.5*
%{_mandir}/man5/ignored_words.conf.5*
%{_mandir}/man5/ignored_elements.conf.5*
# filesystem package owns /usr/share/augeas/lenses directory
%{_datadir}/augeas/lenses/libreport.aug

%files filesystem
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/events.d/
%dir %{_sysconfdir}/%{name}/events/
%dir %{_sysconfdir}/%{name}/workflows.d/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/conf.d/
%dir %{_datadir}/%{name}/conf.d/plugins/
%dir %{_datadir}/%{name}/events/
%dir %{_datadir}/%{name}/workflows/
%dir %{_sysconfdir}/%{name}/plugins/

%files devel
# Public api headers:
%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/libreport/libreport_types.h
%{_includedir}/libreport/client.h
%{_includedir}/libreport/dump_dir.h
%{_includedir}/libreport/event_config.h
%{_includedir}/libreport/problem_data.h
%{_includedir}/libreport/problem_report.h
%{_includedir}/libreport/report.h
%{_includedir}/libreport/report_result.h
%{_includedir}/libreport/run_event.h
%{_includedir}/libreport/file_obj.h
%{_includedir}/libreport/config_item_info.h
%{_includedir}/libreport/workflow.h
%{_includedir}/libreport/problem_details_widget.h
%{_includedir}/libreport/problem_details_dialog.h
%{_includedir}/libreport/problem_utils.h
%{_includedir}/libreport/ureport.h
%{_includedir}/libreport/reporters.h
%{_includedir}/libreport/global_configuration.h
# Private api headers:
%{_includedir}/libreport/internal_libreport.h
%{_includedir}/libreport/xml_parser.h
%{_includedir}/libreport/helpers
%{_libdir}/libreport.so
%{_libdir}/pkgconfig/libreport.pc
%dir %{_includedir}/libreport

%files web
%{_libdir}/libreport-web.so.*

%files web-devel
%{_libdir}/libreport-web.so
%{_includedir}/libreport/libreport_curl.h
%{_libdir}/pkgconfig/libreport-web.pc

%files -n python3-libreport
%{python3_sitearch}/report/
%{python3_sitearch}/reportclient/

%files cli
%{_bindir}/report-cli
%{_mandir}/man1/report-cli.1.gz

%files newt
%{_bindir}/report-newt
%{_mandir}/man1/report-newt.1.gz

%files gtk
%{_bindir}/report-gtk
%{_libdir}/libreport-gtk.so.*
%{_mandir}/man1/report-gtk.1.gz

%files gtk-devel
%{_libdir}/libreport-gtk.so
%{_includedir}/libreport/internal_libreport_gtk.h
%{_libdir}/pkgconfig/libreport-gtk.pc

%files plugin-kerneloops
%{_datadir}/%{name}/events/report_Kerneloops.xml
%{_mandir}/man*/reporter-kerneloops.*
%{_bindir}/reporter-kerneloops

%files plugin-logger
%config(noreplace) %{_sysconfdir}/libreport/events/report_Logger.conf
%{_mandir}/man5/report_Logger.conf.5.*
%{_datadir}/%{name}/events/report_Logger.xml
%{_datadir}/%{name}/workflows/workflow_Logger.xml
%{_datadir}/%{name}/workflows/workflow_LoggerCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/print_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_logger.conf
%{_mandir}/man5/print_event.conf.5.*
%{_mandir}/man5/report_logger.conf.5.*
%{_bindir}/reporter-print
%{_mandir}/man*/reporter-print.*

%files plugin-systemd-journal
%{_bindir}/reporter-systemd-journal
%{_mandir}/man*/reporter-systemd-journal.*

%files plugin-mailx
%config(noreplace) %{_sysconfdir}/libreport/plugins/mailx.conf
%{_datadir}/%{name}/conf.d/plugins/mailx.conf
%{_datadir}/%{name}/events/report_Mailx.xml
%{_datadir}/%{name}/workflows/workflow_Mailx.xml
%{_datadir}/%{name}/workflows/workflow_MailxCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/mailx_event.conf
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_mailx.conf
%{_mandir}/man5/mailx.conf.5.*
%{_mandir}/man5/mailx_event.conf.5.*
%{_mandir}/man5/report_mailx.conf.5.*
%{_mandir}/man*/reporter-mailx.*
%{_bindir}/reporter-mailx

%files plugin-ureport
%config(noreplace) %{_sysconfdir}/libreport/plugins/ureport.conf
%{_datadir}/%{name}/conf.d/plugins/ureport.conf
%{_bindir}/reporter-ureport
%{_mandir}/man1/reporter-ureport.1.gz
%{_mandir}/man5/ureport.conf.5.gz
%{_datadir}/%{name}/events/report_uReport.xml
%if 0%{?rhel} && ! 0%{?eln}
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_uReport.conf
%{_datadir}/%{name}/workflows/workflow_uReport.xml
%{_mandir}/man5/report_uReport.conf.5.*
%endif

%if %{with bugzilla}
%files plugin-bugzilla
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla.conf
%{_datadir}/%{name}/conf.d/plugins/bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_kernel.conf
%{_datadir}/%{name}/events/report_Bugzilla.xml
%{_datadir}/%{name}/events/watch_Bugzilla.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_Bugzilla.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_event.conf
# FIXME: remove with the old gui
%{_mandir}/man1/reporter-bugzilla.1.gz
%{_mandir}/man5/report_Bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_event.conf.5.*
%{_mandir}/man5/bugzilla.conf.5.*
%{_mandir}/man5/bugzilla_format.conf.5.*
%{_mandir}/man5/bugzilla_formatdup.conf.5.*
%{_mandir}/man5/bugzilla_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/bugzilla_formatdup_analyzer_libreport.conf.5.*
%{_mandir}/man5/bugzilla_format_kernel.conf.5.*
%{_bindir}/reporter-bugzilla
%if 0%{?fedora} < 38
%{_bindir}/reporter-bugzilla-python
%endif

%endif

%files plugin-mantisbt
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt.conf
%{_datadir}/%{name}/conf.d/plugins/mantisbt.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_format_analyzer_libreport.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/mantisbt_formatdup_analyzer_libreport.conf
%{_bindir}/reporter-mantisbt
%{_mandir}/man1/reporter-mantisbt.1.gz
%{_mandir}/man5/mantisbt.conf.5.*
%{_mandir}/man5/mantisbt_format.conf.5.*
%{_mandir}/man5/mantisbt_formatdup.conf.5.*
%{_mandir}/man5/mantisbt_format_analyzer_libreport.conf.5.*
%{_mandir}/man5/mantisbt_formatdup_analyzer_libreport.conf.5.*

%files centos
%{_datadir}/%{name}/workflows/workflow_CentOSCCpp.xml
%{_datadir}/%{name}/workflows/workflow_CentOSKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_CentOSPython.xml
%{_datadir}/%{name}/workflows/workflow_CentOSPython3.xml
%{_datadir}/%{name}/workflows/workflow_CentOSVmcore.xml
%{_datadir}/%{name}/workflows/workflow_CentOSXorg.xml
%{_datadir}/%{name}/workflows/workflow_CentOSLibreport.xml
%{_datadir}/%{name}/workflows/workflow_CentOSJava.xml
%{_datadir}/%{name}/workflows/workflow_CentOSJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_centos.conf
%{_mandir}/man5/report_centos.conf.5.*
%{_datadir}/%{name}/events/report_CentOSBugTracker.xml
%config(noreplace) %{_sysconfdir}/libreport/events/report_CentOSBugTracker.conf
%{_mandir}/man5/report_CentOSBugTracker.conf.5.*
# report_CentOSBugTracker events are shipped by libreport package
%config(noreplace) %{_sysconfdir}/libreport/events.d/centos_report_event.conf
%{_mandir}/man5/centos_report_event.conf.5.gz

%files plugin-reportuploader
%{_mandir}/man*/reporter-upload.*
%{_mandir}/man5/uploader_event.conf.5.*
%{_bindir}/reporter-upload
%{_datadir}/%{name}/events/report_Uploader.xml
%config(noreplace) %{_sysconfdir}/libreport/events.d/uploader_event.conf
%{_datadir}/%{name}/workflows/workflow_Upload.xml
%{_datadir}/%{name}/workflows/workflow_UploadCCpp.xml
%config(noreplace) %{_sysconfdir}/libreport/plugins/upload.conf
%{_datadir}/%{name}/conf.d/plugins/upload.conf
%{_mandir}/man5/upload.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_uploader.conf
%{_mandir}/man5/report_uploader.conf.5.*
%config(noreplace) %{_sysconfdir}/libreport/events/report_Uploader.conf
%{_mandir}/man5/report_Uploader.conf.5.*

%if 0%{?fedora} || 0%{?eln}
%files fedora
%{_datadir}/%{name}/workflows/workflow_FedoraCCpp.xml
%{_datadir}/%{name}/workflows/workflow_FedoraKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_FedoraPython.xml
%{_datadir}/%{name}/workflows/workflow_FedoraPython3.xml
%{_datadir}/%{name}/workflows/workflow_FedoraVmcore.xml
%{_datadir}/%{name}/workflows/workflow_FedoraXorg.xml
%{_datadir}/%{name}/workflows/workflow_FedoraLibreport.xml
%{_datadir}/%{name}/workflows/workflow_FedoraJava.xml
%{_datadir}/%{name}/workflows/workflow_FedoraJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_fedora.conf
%{_mandir}/man5/report_fedora.conf.5.*
%endif

%if %{with bugzilla}
%if 0%{?rhel} && ! 0%{?eln}
%files rhel-bugzilla
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaCCpp.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaKerneloops.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaPython.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaVmcore.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaXorg.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaLibreport.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaJava.xml
%{_datadir}/%{name}/workflows/workflow_RHELBugzillaJavaScript.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/report_rhel_bugzilla.conf
%{_mandir}/man5/report_rhel_bugzilla.conf.5.*

%files rhel-anaconda-bugzilla
%{_datadir}/%{name}/workflows/workflow_AnacondaRHELBugzilla.xml
%endif

%files anaconda
%if 0%{?fedora} || 0%{?eln}
%{_datadir}/%{name}/workflows/workflow_AnacondaFedora.xml
%endif
%{_datadir}/%{name}/workflows/workflow_AnacondaUpload.xml
%config(noreplace) %{_sysconfdir}/libreport/workflows.d/anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/bugzilla_anaconda_event.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_format_anaconda.conf
%config(noreplace) %{_sysconfdir}/libreport/plugins/bugzilla_formatdup_anaconda.conf
%{_mandir}/man5/anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_anaconda_event.conf.5.*
%{_mandir}/man5/bugzilla_format_anaconda.conf.5.*
%{_mandir}/man5/bugzilla_formatdup_anaconda.conf.5.*
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.17.15-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.17.15-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.17.15-6
- Rebuilt for Python 3.14

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.17.15-2
- Rebuilt for Python 3.13

* Sun Feb 18 2024 Packit <hello@packit.dev> - 2.17.15-1
- Release version 2.17.15 (Michal Srb)
- reporter-bugzilla: Make the supplementary bugs easily identifiable (Michal Srb)
- reporter-bugzilla: Fix formatting in the supplementary bugs (Michal Srb)
- reporter-bugzilla: Fix code comment (Michal Srb)

* Mon Feb 12 2024 Packit <hello@packit.dev> - 2.17.14-1
- Release version 2.17.14 (Michal Srb)
- reporter-bugzilla: Reduce number of duplicate bug reports (Michal Srb)
- reporter-bugzilla: Fix config loading (Michal Srb)
- reporter-bugzilla: API key must consist of latin-1 characters (Michal Srb)
- reporter-bugzilla: Fix typo (Michal Srb)
- reporter-bugzilla: Fix creating binary attachments (Michal Srb)
- Update translations (mgrabovsky)

* Sun Feb 04 2024 Packit <hello@packit.dev> - 2.17.13-1
- Release version 2.17.13 (Michal Srb)
- Exclude coredump archives when creating a bug (Michal Srb)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Florian Weimer <fweimer@redhat.com> - 2.17.11-5
- Fix C compatibility issues in tests

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 2.17.11-2
- Rebuilt for Python 3.12

* Fri Jun 30 2023 Packit <hello@packit.dev> - 2.17.11-1
- Release version 2.17.11 (Michal Srb)
- spec: Add missing requires for python3-libreport (Michal Srb)
- Build URL with urllib.parse.urljoin() (Michal Srb)
- Add XDG_ACTIVATION_TOKEN to the list of ignored words (Michal Srb)
- Attachments are minor updates in Bugzilla (Michal Srb)
- Retry Bugzilla search queries with delays (Michal Srb)
- Fix "NameError: name 'ticket' is not defined" exception (Michal Srb)
- Update translations (mgrabovsky)

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.17.10-2
- Rebuilt for Python 3.12

* Thu May 11 2023 Packit <hello@packit.dev> - 2.17.10-1
- Release version 2.17.10 (Matěj Grabovský)
- reporter-upload: Fix a use-after-free error in string handling (Matěj Grabovský)
- Update translations (mgrabovsky)
- Update translations (mgrabovsky)

* Fri Mar 24 2023 Packit <hello@packit.dev> - 2.17.9-1
- Release version 2.17.9 (Michal Srb)
- reporter-bugzilla: Fix string interpolation (Matěj Grabovský)
- reporter-bugzilla: Replace flags with just keyword arg (Michal Srb)
- reporter-bugzilla: Make sure that the creator of a bug is always in CC (Michal Srb)
- reporter-bugzilla: Don't fail if reported_to file doesn't exist (Michal Srb)
- reporter-bugzilla: Fix reporting when the bug already exists (Michal Srb)
- use $XDG_CONFIG_HOME to access user's configuration files (Yann Droneaud)
- Update translations (mgrabovsky)

* Fri Mar 03 2023 Packit <hello@packit.dev> - 2.17.8-1
- Release version 2.17.8 (Michal Srb)
- Update changelog (Michal Srb)
- reporter-bugzilla: Fix KeyError when HOME env var is not set (Michal Srb)
- Update changelog (Michal Srb)
- reporter-bugzilla: Fix password prompt in client/server mode (Michal Srb)

* Mon Feb 20 2023 Packit <hello@packit.dev> - 2.17.7-1
- Release version 2.17.7 (Michal Srb)
- spec: Add disttag (Michal Srb)
- Update changelog (Michal Srb)
- Fix rpm -V issue with missing reporter-bugzilla-python in f38 (Michal Srb)
- Fix TypeError (Michal Srb)
- Update pot file (Matěj Grabovský)
- readme: Add diagram of related projects (Matěj Grabovský)
- Update translations (mgrabovsky)
- Use SPDX format for license field (Matěj Grabovský)
- ignored_words: Add KeyboardInterrupt (Michal Fabik)
- packit: Add dependencies for SRPM build (Matěj Grabovský)
- Update translations (mgrabovsky)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 06 2022 Packit <hello@packit.dev> - 2.17.6-1
- Release version 2.17.6 (Michal Srb)
- Update translations (mgrabovsky)
- Update changelog (Michal Srb)
- reporter-bugzilla: Fix TypeError (Michal Srb)

* Mon Oct 24 2022 Michal Srb <michal@redhat.com> - 2.17.5-2
- Fix dist-tag

* Mon Oct 24 2022 Packit <hello@packit.dev> - 2.17.5-1
- Release version 2.17.5 (Michal Srb)
- Update changelog (Michal Srb)
- dump_dir.py: check that the filename doesn't start with "/" (Michal Srb)
- dump_dir.py: Don't pass libreport flags to open() (Michal Srb)
- reporter-bugzilla: Fix exceptions (Michal Srb)
- Update translations (mgrabovsky)

* Wed Sep 14 2022 Packit <hello@packit.dev> - 2.17.4-1
- Release version 2.17.4 (Michal Fabik)
- Update changelog (Michal Fabik)
- reporter_bugzilla.py: Don't ask for API key if we already have it (Michal Srb)
- internal/bz_connection.py: Fix "TypeError: 'builtin_function_or_method' object is not subscriptable" (Michal Srb)
- reporter_bugzilla.py: Fix condition (Michal Srb)
- internal/reported_to.py: Prevent possible ValueError if the line is for example empty (Michal Srb)
- reporter_bugzilla.py: Prevent possible KeyError exception (Michal Srb)
- reporter_bugzilla.py: Default value for `b_create_private` is False (Michal Srb)
- reporter_bugzilla.py: Prevent possible KeyError exception (Michal Srb)

* Mon Sep 12 2022 Packit <hello@packit.dev> - 2.17.3-1
- Release version 2.17.3 (Michal Fabik)
- Update changelog (Michal Fabik)
- Run autoupdate to get rid of obsolete/deprecated macros (Michal Fabik)
- Makefile: Move README.md to EXTRA_DIST (Michal Fabik)
- Don't build rhel-bugzilla --without-bugzilla (Michal Fabik)
- doc: Make anaconda_event.conf depend on BZ (Michal Fabik)
- Fix build --without-bugzilla (Michal Fabik)
- spec: Don't list files twice (Michal Fabik)
- Update translations (mgrabovsky)

* Thu Aug 18 2022 Packit <hello@packit.dev> - 2.17.2-1
- Release version 2.17.2 (Michal Fabik)
- reporter_bugzilla.py: Build, install (Michal Fabik)
- reporter_bugzilla.py: Add tests (Michal Fabik)
- reporter_bugzilla.py: Initial commit (Michal Fabik)
- Update translations (mgrabovsky)
- abrt_xmlrpc: Don't warn about discarded const (Michal Fabik)
- Update translations (mgrabovsky)
- Update translations (mgrabovsky)
- Use conventional lseek arg order (Michal Fabik)
- Update translations (mgrabovsky)
- ignored_words: Ignore more debuginfod URLs (Matěj Grabovský)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.17.1-2
- Rebuilt for Python 3.11

* Thu Mar 10 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 2.17.1-1
- Release version 2.17.1 (Michal Srb)
- reporter-bugzilla: send API key in HTTP header (Michal Srb)
- tito: Use custom tagger that updates changelog (Matěj Grabovský)
- changelog: Fix link to release diff (Matěj Grabovský)
- reporter-bugzilla: Fix APIKey name (Michal Fabik)
- Update translations (mgrabovsky)
- Add missing va_end (Michal Židek)

* Mon Feb 21 2022 Michal Srb <michal@redhat.com> - 2.17.0-1
- [reporter-bugzilla] Use API key for authentication

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.16.0-2
- Rebuild for testing

* Mon Jan 17 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.16.0-1
- Bump satyr dependency to 0.38
- Bump libreport library revision to 2:1:0
- Drop build-time dependency on libproxy-devel
- Drop last reference to global_uuid file
- Don't use deprecated assertEquals() in tests
- Add DEBUGINFOD_URLS environment variable to ignored_words
- rhbz: Retry XML-RPC calls when uploading attachments
- rhbz: Be a little bit more defensive when working with subcomponents
- Update translations

* Thu Jan 13 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.15.2-11
- Backport patch for building with Python 3.11
  (https://bugzilla.redhat.com/show_bug.cgi?id=2019402)

* Wed Jan 12 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.15.2-10
- Bump for rebuild

* Thu Jan 06 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.15.2-9
- Bump release for rebuild

* Thu Jan 06 2022 Matěj Grabovský <mgrabovs@redhat.com> - 2.15.2-8
- Bump release for rebuild

* Wed Dec 22 2021 Matěj Grabovský <mgrabovs@redhat.com> - 2.15.2-7
- Rebuild for satyr 0.39

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 2.15.2-5
- Rebuild for versioned symbols in json-c

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 2.15.2-4
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.15.2-2
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 2.15.2-1
- Release version 2.15.2-1 (Michal Fabik)
- binhex: Remove unused API (Matěj Grabovský)
- lib: Use GLib for computing SHA-1 digests (Matěj Grabovský)
- run_event: Improve memory management (Matěj Grabovský)
- gtk: Fix segfault (Matěj Grabovský)

* Tue May 04 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 2.15.1-1
- Release version 2.15.1-1 (Michal Fabik)
- ureport: Strange usage of tmp variable (Michal Židek)
- steal_directory: Silence a warning (Michal Židek)
- dump_dir: Use g_free and re-init to NULL (Michal Židek)
- dump_dir: Use g_free instead of free (Michal Židek)
- dirsize: No need to check for NULL (Michal Židek)
- dirsize: Bad checks for NULL (Michal Židek)
- gui-wizard-gtk: Possible double free (Michal Židek)
- gui-wizard-gtk: Check if EXCLUDE_FROM_REPORT is set (Michal Židek)
- gui-wizard-gtk: Improve docs and add missing free (Michal Židek)
- cli: Address of local auto-variable assigned to a function parameter (Michal Židek)
- gtk-helpers: Add missing g_strfreev() (Michal Židek)
- cli: Add missing g_free call (Michal Židek)
- gitignore: Drop misleading comment (Michal Fabik)
- spec: Sync upstream with distgit (Michal Fabik)
- changelog: Add missing link to changes in 2.15.0 (Matěj Grabovský)
- spec: Make plugin-mailx depend on /usr/bin/mailx (Matěj Grabovský)
- Add support for excluding whole elements from search for sensitive words (Michal Srb)
- ignored_words: add more "key" variations (Michal Srb)

* Fri Jan 29 2021 Michal Srb <michal@redhat.com> - 2.14.0-17
- Drop AnacondaRHEL workflow reference

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.14.0-15
- Bump rev for upgrades

* Fri Dec 11 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-13
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1906405

* Tue Nov 03 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-12
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1893595

* Fri Oct 09 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-11
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1882328

* Tue Sep 29 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-10
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1883337
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1883410

* Sun Sep 27 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-9
- Add upstream fixes for memory management

* Sun Sep 27 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-8
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1882950

* Fri Sep 25 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.14.0-7
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1882319

* Wed Aug 19 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.14.0-6
- Updates so ELN builds in a Fedora-like reporting configuration, even though
  the %%{rhel} macro is set.

* Thu Aug 13 2020 Michal Fabik <mfabik@redhat.com> 2.14.0-3
- forbidden_words: Add potentially sensitive env vars
- lib: Add version script for libreport
- lib: compress: Use libarchive
- Replace various utility functions with stock GLib ones
- gtk,lib: Update symbol list
- dd: Update dd_get_owner to handle error return values
- dirsize: Don't pick .lock'd dirs for deletion
- setgid instead of setuid the abrt-action-install-debuginfo-to-abrt-cache
- Various coding style improvements
- Various memory management fixes
- lib: Check for errors when opening files
- gtk-helpers: Check return value
- doc: Exclude more files with --without-bugzilla
- lib: Don’t use external executables for decompression
- lib: Decommission libreport_list_free_with_free
- Drop Red Hat Customer Portal reporter
- ureport: Drop Strata integration
- lib: Remove creates-items tag parsing in event definitions

* Fri Aug 07 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2.13.1-4
- Bump to fix upgrade path

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.13.1-2
- Rebuilt for Python 3.9

* Mon May 11 2020 Michal Fabik <mfabik@redhat.com> 2.13.1-1
- Fix broken abrt-vmcore.service due to bad namespacing

* Fri Apr 24 2020 Michal Fabik <mfabik@redhat.com> 2.13.0-2
- Support new "time" and "time_for_children" kernel namespaces
- Remove preprocessor namespacing in favor of function name prefixes
- client-python: Accomodate for multiple debug directories
- gui-wizard-gtk: Wrap event log messages
- lib: Drop D-Bus code 
- plugins: reporter-rhtsupport: Drop unused debugging code 
- Update translations

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 2.12.0-4
- Rebuild (json-c)

* Fri Mar 20 2020 Ernestas Kulik <ekulik@redhat.com> - 2.12.0-3
- Add patch for https://bugzilla.redhat.com/show_bug.cgi?id=1815544

* Fri Feb 07 2020 Ernestas Kulik <ekulik@redhat.com> - 2.12.0-2
- Bump release for side tag rebuild

* Thu Feb 06 2020 Michal Fabik <mfabik@redhat.com> 2.12.0-1
- ureport: Allow printf-like data attaching
- plugins: reporter-rhtsupport: Avoid runtime warning
- Update translations
- lib: Don't include Nettle in a public interface
- ureport: Drop HTTP header table
- glib_support: Use g_strsplit
- glib_support: Drop type initialization
- client-python: Drop yumdebuginfo
- lib: Use Nettle for computing SHA-1 digests
- Move augeas lenses to new subdirectory

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Matěj Grabovský <mgrabovs@redhat.com> 2.11.3-1
- Remove unused scripts
- gtk: Fix infinite loop crashing the reporting
- gtk: Improve logging
- gtk: Remove page number from page struct
- gtk: Code style adjustments
- Make notebook tabs invisible again
- gui-wizard-gtk: Remove expert mode
- gui-wizard-gtk: Stop allowing overriding UI definitions
- pull-trans: Suggest zanata install
- shellcheck: Iterating over ls output is fragile. Use globs.
- shellcheck: Double quote to prevent globbing and word splitting
- zanata: Use python3 zanata client to pull translations
- gtk: Fix another possible double-free

* Mon Nov 11 2019 Ernestas Kulik <ekulik@redhat.com> - 2.11.2-2
- Add patch to fix a double-free

* Wed Oct 23 2019 Matěj Grabovský <mgrabovs@redhat.com> 2.11.2-1
- gtk: Improve memory management
- gtk: Prevent memory leak
- lib: Eliminate GLib inefficiency
- gtk,style: Minor style consistency fixes
- workflows: Correct name of post_report event

* Wed Oct 16 2019 Matěj Grabovský <mgrabovs@redhat.com> 2.11.1-1
- gtk: Fix a double-free condition

* Fri Oct 11 2019 Matěj Grabovský <mgrabovs@redhat.com> 2.11.0-1
- Remove option for emergency analysis/reporting
- tests: proc_helpers: Fix call to errx()
- plugins: bugzilla: Add format file for libreport duplicates
- dbus: Remove interface introspection files
- lib: Don't warn if a configuration key is missing
- gtk: Handle event wildcards in command line options
- gtk: Better handling of workflows with wildcarded events
- lib: Remove unused arguments of prepare_commands
- lib: Reintroduce error logging in event XML parser
- cli: Continue running even if some events have no commands
- cli: Expand event name wildcards
- lib: Expand wildcards in workflow XML parser
- lib: Add a function to expand wildcards in event names
- style: Simplify code; fix typos in comments
- gitignore: Update with missing and renamed generated files
- dirsize: Skip dirs in which sosreport is being generated
- tests: Fix Python tests being skipped unconditionally
- Remove Python 2 support

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Martin Kutlak <mkutlak@redhat.com> 2.10.1-1
- doc: Makefile.am: Use correct path for --conf-file
- lib: copy_file_recursive: Use GLib abstractions
- gui-wizard-gtk: Fix fix
- cli: run-command: Replace use of vfork() with fork()
- plugins: rhbz: Don’t call strlen() on attachment data
- Check for empty fmt_file name when printing error msgs
- cli: Unpack command-line argument parsing logic
- lib: event_config: Remove pointless assignment
- gui-wizard-gtk: Fix never-read assignment
- lib: xatonum: Check string parameters
- Rework and refine composition of error messages
- Add clearer warnings about missing report elements specified in format files
- Move uReport workflow to plugin-ureport subpackage
- lib: ureport: Export workflow when saving server response
- lib: dump_dir: Clean up on failure in dd_delete()
- Use #ifdef to check whether macros are defined
- autogen.sh: Use autoreconf
- autogen.sh: Allow skipping running configure
- tests: forbidden_words: Don’t hardcode sysconfdir
- Makefile.am: Use correct locale when getting date

* Tue Apr 23 2019 Ernestas Kulik <ekulik@redhat.com> - 2.10.0-3
- Add patch to fix workflow fields not being added to reported_to when μReport response comes with a Bugzilla URL

* Mon Feb 04 2019 Ernestas Kulik <ekulik@redhat.com> - 2.10.0-2
- Remove unused patch

* Sat Feb 02 2019 Ernestas Kulik <ekulik@redhat.com> - 2.10.0-1
- Update to 2.10.0
- Bump GLib dependency
- Add patch to work around issue with test
