%bcond_without bugzilla

%define dbus_devel dbus-devel
%define libjson_devel json-c-devel

%define glib_ver 2.43.4

Summary: Generic library for reporting various problems
Name: libreport
Version: 2.17.15
Release: 1%{?dist}
License: GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://abrt.readthedocs.org/
Source: https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch1: 0001-skip-unwanted-tests.patch
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
%autosetup -p1

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

# Remove unwanted RHEL specific workflow configuration files
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELCCpp.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELKerneloops.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELPython.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELvmcore.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELxorg.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELLibreport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELJava.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_RHELJavaScript.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_uReport.xml
rm -f %{buildroot}/%{_datadir}/libreport/workflows/workflow_AnacondaRHEL.xml
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
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel_add_data.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_uReport.conf
rm -f %{buildroot}/%{_sysconfdir}/libreport/workflows.d/report_rhel_bugzilla.conf
rm -f %{buildroot}%{_mandir}/man5/report_rhel.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_uReport.conf.5
rm -f %{buildroot}%{_mandir}/man5/report_rhel_bugzilla.conf.5

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
%{_bindir}/reporter-bugzilla-python

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


%if %{with bugzilla}

%files anaconda
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
* Thu Nov 28 2024 Sumit Jena <v-sumitjena@microsoft.com> - 2.17.15-1
- Update to version 2.17.15
- License verified.

* Tue Dec 20 2022 Muhammad Falak <mwani@microsoft.com> - 2.13.1-9
- License verified

* Thu Dec 09 2021 Muhammad Falak <mwani@microsoft.com> - 2.13.1-8
- Introduce macro '%{mariner_failing_tests}' to gate `--run-check` failures
- Remove non 0 exit from check to avoid build break

* Wed Aug 11 2021 Thomas Crain <thcrain@microsoft.com> - 2.13.1-7
- Only require testing requirements during check builds
- Only build Fedora subpackage on Fedora

* Tue Jan 12 2021 Joe Schmitt <joschmit@microsoft.com> - 2.13.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove gtk3 dependency and features. ignored_words and forbidden_words are built only when gtk support is on.

* Wed Oct 07 2020 Matěj Grabovský <mgrabovs@redhat.com> - 2.13.1-5
- Add fix for https://bugzilla.redhat.com/show_bug.cgi?id=1883337

* Mon May 11 2020 Michal Fabik <mfabik@redhat.com> 2.13.1-2
- Fix broken abrt-vmcore.service due to bad namespacing

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
