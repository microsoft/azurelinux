%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       2.0.1
Release:       2%{?dist}
# older URL, but still with useful information about pycups
#URL:           https://cyberelk.net/tim/software/pycups/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:           https://github.com/OpenPrinting/pycups/
Source:        https://github.com/OpenPrinting/pycups/releases/download/v%{version}/pycups-%{version}.tar.gz
License:       GPLv2+

# gcc is no longer in buildroot by default
BuildRequires: gcc

BuildRequires: cups-devel
BuildRequires: python3-devel

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
%setup -n pycups-%{version}

sed -i '/^#!\/usr\/bin\/python/d' examples/cupstree.py

%build
%py3_build

%install
make install-rpmhook DESTDIR="%{buildroot}"
%py3_install
export PYTHONPATH=%{buildroot}%{python3_sitearch}
%{__python3} -m pydoc -w cups
%{_bindir}/mkdir html
%{_bindir}/mv cups.html html

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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
