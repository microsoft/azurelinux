%{?filter_setup:
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       2.0.4
Release:       4%{?dist}
# older URL, but still with useful information about pycups
#URL:           http://cyberelk.net/tim/software/pycups/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:           https://github.com/OpenPrinting/pycups/
Source:        https://github.com/OpenPrinting/pycups/releases/download/v%{version}/pycups-%{version}.tar.gz
License:       GPL-2.0-or-later

# all taken from upstream


# gcc is no longer in buildroot by default
BuildRequires: gcc
# for autosetup
BuildRequires: git-core
# uses make
BuildRequires: make
BuildRequires: python3-pytest
BuildRequires: python3-pytest-runner
BuildRequires: cups-devel
BuildRequires: python3-devel
# distutils are removed from python3 project, use the one
# from setuptools
BuildRequires: python3-setuptools
Provides: python3-cups

%description
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package -n python3-cups
Summary:       Python3 bindings for CUPS API, known as pycups.
%{?python_provide:%python_provide python3-cups}

%description -n python3-cups
This package provides Python 3 bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package doc
Summary:       Documentation for python-cups

%description doc
Documentation for python-cups.

%prep
%autosetup -S git -n pycups-%{version}

%build
%py3_build

%install
make install-rpmhook DESTDIR="%{buildroot}"
%py3_install
export PYTHONPATH=%{buildroot}%{python3_sitearch}
%{__python3} -m pydoc -w cups
%{_bindir}/mkdir html
%{_bindir}/mv cups.html html

%check
python3 test.py

%files -n python3-cups
%doc README NEWS TODO
%license COPYING
%{python3_sitearch}/cups.cpython-3*.so
%{python3_sitearch}/pycups*.egg-info
%{_rpmconfigdir}/fileattrs/psdriver.attr
%{_rpmconfigdir}/postscriptdriver.prov

%files doc
%doc examples html

%changelog
* Wed Dec 18 2024 Sumit Jena <v-sumitjena@microsoft.com> - 2.0.4-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.4-2
- Rebuilt for Python 3.13

* Thu Apr 18 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.4-1
- 2275527,2275779 - 2.0.4, fix python-cups installation

* Wed Apr 17 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.3-1
- rebase to 2.0.3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-19
- SPDX migration

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.1-17
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 19 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-15
- distutils will be removed in Python3.12, use setuptools instead

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.1-13
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-10
- IPPRequest.writeIO() tracebacks because PY_SSIZE_T_CLEAN is not defined

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.1-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-7
- fix invalid delete (upstream ticket #11)

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-6
- make is no longer in buildroot by default
- use smaller git-core instead of git

* Fri Aug 28 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-5
- 1873385 - ignore driverless utilities during tags creation

* Wed Jul 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-4
- use %%python3_sitearch in filter_provides_in, otherwise the package fails to build

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-2
- Rebuilt for Python 3.9

* Fri Apr 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-1
- 2.0.1, fixes #1816107

* Mon Mar 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.74-7
- use __python macro for calling pydoc

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.74-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.74-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.74-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.74-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.74-2
- 1578356 - Remove python2 subpackage

* Wed Sep 26 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.74-1
- 1.9.74

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.72-21
- Rebuilt for Python 3.7

* Fri Apr 20 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.72-20
- adding docs back

* Thu Apr 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.72-19
- fixing statement

* Thu Apr 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.72-18
- make building python2 subpackage optional

* Wed Apr 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.72-17
- remove python2 subpackage

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.9.72-16
- gcc is no longer in buildroot by default

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.9.72-12
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.9.72-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.72-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.72-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Jiri Popelka <jpopelka@redhat.com> - 1.9.72-7
- Remove shebang from examples/cupstree.py (bug #1288830).

* Mon Nov 23 2015 Jiri Popelka <jpopelka@redhat.com> - 1.9.72-6
- python2 subpackage

* Fri Nov 20 2015 Jiri Popelka <jpopelka@redhat.com> - 1.9.72-5
- do not use py3dir
- use python_provide macro

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.9.72-4
- Rebuilt for Python3.5 rebuild

* Tue Aug 11 2015 Jiri Popelka <jpopelka@redhat.com> - 1.9.72-3
- %%py3_build && %%py3_install

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 10 2015 Tim Waugh <twaugh@redhat.com> - 1.9.72-1
- Latest upstream release.

* Thu Jan 15 2015 Tim Waugh <twaugh@redhat.com> - 1.9.70-3
- Only ship the postscriptdriver rpm-provides script in python3-cups
  as it is a python3 script.

* Mon Jan 12 2015 Tim Waugh <twaugh@redhat.com> - 1.9.70-2
- Fixes for IPP constants (bug #1181043, bug #1181055).

* Tue Dec 23 2014 Tim Waugh <twaugh@redhat.com> - 1.9.70-1
- 1.9.70.

* Sat Dec 13 2014 Tim Waugh <twaugh@redhat.com> - 1.9.69-2
- Fixed password_callback so it obtains UTF-8 password correctly
  (bug #1155469).

* Thu Dec  4 2014 Tim Waugh <twaugh@redhat.com> - 1.9.69-1
- 1.9.69.

* Mon Oct  6 2014 Tim Waugh <twaugh@redhat.com> - 1.9.68-1
- 1.9.68.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Tim Waugh <twaugh@redhat.com> - 1.9.67-1
- 1.9.67, fixing a Connection.getFile crash.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.66-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.9.66-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Nov 27 2013 Jiri Popelka <jpopelka@redhat.com> - 1.9.66-1
- 1.9.66 - Python 3 support.

* Wed Nov 27 2013 Tim Waugh <twaugh@redhat.com> - 1.9.65-1
- 1.9.65.

* Wed Jul 31 2013 Jiri Popelka <jpopelka@redhat.com> - 1.9.63-4
- Fix getting of booleans.

* Fri Apr 12 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-3
- Propagate UTF-8 decoding errors.

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-2
- Encode generated URIs correctly (bug #950162).

* Wed Mar 20 2013 Tim Waugh <twaugh@redhat.com> - 1.9.63-1
- 1.9.63.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 27 2012 Jiri Popelka <jpopelka@redhat.com> - 1.9.62-2
- Remove unused statements.

* Wed Aug  1 2012 Tim Waugh <twaugh@redhat.com> - 1.9.62-1
- 1.9.62, including fixes for building against newer versions of CUPS.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Tim Waugh <twaugh@redhat.com> - 1.9.61-2
- Apply upstream patch to fix crash on loading invalid PPDs (bug #811159).

* Tue Mar  6 2012 Tim Waugh <twaugh@redhat.com> - 1.9.61-1
- 1.9.61, fixing ref-counting bugs (bug #800143).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Tim Waugh <twaugh@redhat.com> - 1.9.60-1
- 1.9.60.  Constants from CUPS 1.5.0.

* Mon Oct  3 2011 Tim Waugh <twaugh@redhat.com> - 1.9.59-1
- 1.9.59.  Fixes auth loops with CUPS 1.5.0 (bug #734247).

* Thu Jun  9 2011 Tim Waugh <twaugh@redhat.com> - 1.9.57-1
- 1.9.57.  Fixes rpm provides script (bug #712027).

* Sun Mar 20 2011 Tim Waugh <twaugh@redhat.com> - 1.9.55-1
- 1.9.55.  Support for IPP "resolution" type.

* Wed Feb 23 2011 Tim Waugh <twaugh@redhat.com> - 1.9.54-1
- 1.9.54.  The rpm hook is now upstream.

* Wed Feb 23 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-5
- Use rpmconfigdir macro throughout.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-3
- Fixed typo in psdriver.attr that prevented PPD files from being
  scanned when generating postscriptdriver tags.

* Thu Jan 20 2011 Tim Waugh <twaugh@redhat.com> - 1.9.53-2
- Moved postscriptdriver RPM tagging machinery here.  Fixed
  leading/trailing whitespace in tags as well.

* Wed Dec 15 2010 Tim Waugh <twaugh@redhat.com> - 1.9.53-1
- 1.9.53 fixing a thread-local storage issue (bug #662805).

* Wed Nov 17 2010 Jiri Popelka <jpopelka@redhat.com> - 1.9.52-2
- Fixed rpmlint errors/warnings (#648986)
- doc subpackage

* Mon Nov 01 2010 Jiri Popelka <jpopelka@redhat.com> - 1.9.52-1
- Initial RPM spec file
