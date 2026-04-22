## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           scapy
Version:        2.7.0
Release:        %autorelease
Summary:        Interactive packet manipulation tool and network scanner

%global         gituser         secdev
%global         gitname         scapy
%global         gitdate         20251225
%global         commit          40fc5ecf9e69e9bd76664d63ae133d4973fcf81b
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         giturl          https://github.com/%{gituser}/%{gitname}

License:        GPL-2.0-only
URL:            https://scapy.net/
#was            http://www.secdev.org/projects/scapy/
VCS:            git:%{giturl}
#               https://github.com/secdev/scapy/releases
#               https://bitbucket.org/secdev/scapy/pull-request/80
#               https://scapy.readthedocs.io/en/latest/introduction.html
Source0:        %{giturl}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Allow build with older setuptools for EPEL9
Patch0:         scapy-2.7.0-rhel9.patch

%global         common_desc %{expand:
Scapy is a powerful interactive packet manipulation program built on top
of the Python interpreter. It can be used to forge or decode packets of
a wide number of protocols, send them over the wire, capture them, match
requests and replies, and much more.}

# By default do not build documentation because of not allowed cc-by-nc-sa license
%bcond_with        doc


BuildArch:      noarch

BuildRequires:  make
BuildRequires:  sed
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with doc}
BuildRequires:  python%{python3_pkgversion}-tox
%endif

%if ( 0%{?rhel} && 0%{?rhel} == 8 )
# RHEL8 - deps bellow are for RHEL8
# This should be added by generate_buildrequires on newer platforms
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  pyproject-rpm-macros
%endif

# Check Tests
BuildRequires:  python%{python3_pkgversion}-cryptography
BuildRequires:  python%{python3_pkgversion}-tkinter


Recommends:     tcpdump
# Using database of manufactures /usr/share/wireshark/manuf
Recommends:     wireshark-cli

%description %{common_desc}


%package -n python%{python3_pkgversion}-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Provides:       %{name} = %{version}-%{release}

Recommends:     PyX
Recommends:     python%{python3_pkgversion}-matplotlib
Recommends:     ipython3

%description -n python%{python3_pkgversion}-%{name}
%{common_desc}


%if %{with doc}
%package doc
Summary:        Interactive packet manipulation tool and network scanner
License:        CC-BY-NC-SA-2.5

BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

%description doc
%{common_desc}
%endif


%prep
%autosetup -p 1 -n %{name}-%{version}

# Remove shebang
# https://github.com/secdev/scapy/pull/2332
SHEBANGS=$(find ./scapy -name '*.py' -print | xargs grep -l -e '^#!.*env python')
for FILE in $SHEBANGS ; do
    sed -i.orig -e 1d "${FILE}"
    touch -r "${FILE}.orig" "${FILE}"
    rm "${FILE}.orig"
done



%if (0%{?fedora} && 0%{?fedora} > 33 ) || ( 0%{?rhel} && 0%{?rhel} > 8 ) || 0%{?flatpak}
%generate_buildrequires
%pyproject_buildrequires
%endif


%build
%pyproject_wheel

%if %{with doc}
make -C doc/scapy html BUILDDIR=_build_doc SPHINXBUILD=sphinx-build-%python3_version

rm -f doc/scapy/_build_doc/html/.buildinfo
rm -f doc/scapy/_build_doc/html/_static/_dummy
%endif



%install
install -dp -m0755 %{buildroot}%{_mandir}/man1
install -Dp -m0644 doc/scapy.1* %{buildroot}%{_mandir}/man1/

%pyproject_install
%pyproject_save_files scapy

# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy3

# Link the default to the python3 version of executables
ln -s scapy3 %{buildroot}%{_bindir}/scapy



%check
%global         check_exclude %{expand:
    -e 'scapy.arch.bpf.core' -e 'scapy.arch.bpf.supersocket' \
    -e 'scapy.arch.windows' -e 'scapy.arch.windows.native' -e 'scapy.arch.windows.structures' \
    -e 'scapy.contrib.cansocket_python_can' -e 'scapy.tools.generate_bluetooth' \
    -e 'scapy.tools.generate_ethertypes' -e 'scapy.tools.generate_manuf' -e 'scapy.tools.scapy_pyannotate' \
    -e 'scapy.libs.winpcapy'
}

%pyproject_check_import %{check_exclude}

# TODO: Need to fix/remove slow/failed test
# cd test/
# ./run_tests_py2 || true
# ./run_tests_py3 || true



%files -n python%{python3_pkgversion}-%{name} -f %{pyproject_files}
%license LICENSE
%doc %{_mandir}/man1/scapy.1*
%{_bindir}/scapy
%{_bindir}/scapy3


%if %{with doc}
%files doc
%doc doc/scapy/_build_doc/html
%endif


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.7.0-3
- Latest state for scapy

* Mon Jan 05 2026 Michal Ambroz <rebus@seznam.cz> - 2.7.0-2
- scapy build for epel9

* Mon Jan 05 2026 Michal Ambroz <rebus@seznam.cz> - 2.7.0-1
- bump to 2.7.0

* Sun Nov 16 2025 Michal Ambroz <rebus@seznam.cz> - 2.6.1-1
- scapy bump to 2.6.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.6.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.6.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.6.0-4
- Rebuilt for Python 3.14

* Thu May 15 2025 Miroslav Suchý <msuchy@redhat.com> - 2.6.0-3
- do not build documentation subpackage

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Michal Ambroz <rebus@seznam.cz> - 2.6.0-1
- bump to 2.6.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.5.0-8
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.5.0-7
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.12

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Jonathan Wright <jonathan@almalinux.org> - 2.5.0-1
- Update to 2.5.0 rhbz#2156396

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.4.5-5
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.4.5-2
- Rebuilt for Python 3.10

* Tue Apr 20 2021 Michal Ambroz <rebus _AT seznam.cz> - 2.4.5-1
- bump to 2.4.5 release

* Fri Mar 12 2021 Michal Ambroz <rebus _AT seznam.cz> - 2.4.4-1
- bump to 2.4.4 release

* Thu Mar 11 2021 W. Michael Petullo <mike@flyn.org> - 2.4.3-8
- Patch to fix loading libc.a; see https://bugs.python.org/issue42580

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.4.3-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Michal Ambroz <rebus _AT seznam.cz> - 2.4.3-3
- remove colliding manpage from python2 package
- add license files
- add doc subpackage
- remove shebangs

* Sun Oct 06 2019 Michal Ambroz <rebus _AT seznam.cz> - 2.4.3-2
- change to recommended python build dependencies for EPEL7 - thanks Miro Hroncok

* Thu Sep 26 2019 Michal Ambroz <rebus _AT seznam.cz> - 2.4.3-1
- bump to 2.4.3 release
- change the python2 to conditional build to be able to keep one spec for all
- add Recommends for dependencies, except for EPEL7

* Fri Sep 20 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-8
- Subpackage python2-scapy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-3
- Rebuilt for Python 3.7

* Mon Apr 30 2018 Michal Ambroz <rebus _AT seznam.cz> - 2.4.0-2
- disable the test for now - there is too many failing (network) tests

* Mon Apr 30 2018 Michal Ambroz <rebus _AT seznam.cz> - 2.4.0-1
- bump to 2.4.0 release

* Fri Mar 9 2018 Michal Ambroz <rebus _AT seznam.cz> - 2.4.0-0.rc5.1
- bump to upstream 2.4.0 release candidate 5
- enable separate python3 and python2 build

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.3.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Michal Ambroz <rebus _AT seznam.cz> - 2.3.3-1
- bump to upstream 2.3.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Sven Lankes <athmane@fedoraproject.org> - 2.3.1-1
- update to latest upstream release (2.3.1)
- Update to 2.3.1
- Remove upstreamed patch
- Some spec fixes
- Thanks to Athmane Madjoudj for the patch

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 02 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.2.0-5
- Fix psdump()/pdfdump()

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Sven Lankes <sven@lank.es> - 2.2.0-1
- Update to Scapy 2.2.0
- Fixes rhbz #788659 - thanks to Thiébaud Weksteen

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Devan Goodwin <dgoodwin@dangerouslyinc.com> 2.0.0.10-1
- Update to Scapy 2.0.0.10.

* Sun Dec 07 2008 Devan Goodwin <dgoodwin@dangerouslyinc.com> 2.0.0.9-2
- Update for Scapy 2.0.0.9.

* Tue Jan 22 2008 Devan Goodwin <dgoodwin@dangerouslyinc.com> 1.1.1-4
- Switch to using rm macro.

* Mon Jan 21 2008 Devan Goodwin <dgoodwin@dangerouslyinc.com> 1.1.1-2
- Spec file cleanup.

* Fri Jan 18 2008 Devan Goodwin <dgoodwin@dangerouslyinc.com> 1.1.1-1
- Initial packaging for Fedora.


## END: Generated by rpmautospec
