Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname oauth2client
%global sum Python client library for OAuth 2.0
# Share doc between python- and python3-
%global _docdir_fmt %{name}

Name:           python-%{srcname}
Version:        4.1.3
Release:        11%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://github.com/google/%{srcname}
Source0:        https://github.com/google/%{srcname}/archive/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
Patch0:         docs-build-fix.patch
Patch1:         doc-fix.patch
Patch2:         keyring-remove.patch

BuildArch:      noarch
#BuildRequires:  %{_bindir}/tox
BuildRequires:  python3-devel

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-fasteners
BuildRequires:  python3-mock
BuildRequires:  python3-pyasn1 >= 0.1.7
BuildRequires:  python3-pyasn1-modules >= 0.0.5
BuildRequires:  python3-pytest

%description
This is a python client module for accessing resources protected by OAuth 2.0

%package -n python3-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

Requires:       python3-pyOpenSSL
Requires:       python3-fasteners

%description -n python3-%{srcname}
This is a python client module for accessing resources protected by OAuth 2.0

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .doc
%patch1 -p1 -b .doc2
%patch2 -p1 -b .keyring

# Remove the version constraint on httplib2.  From reading upstream's git log,
# it seems the only reason they require a new version is to force python3
# support.  That doesn't affect us on EPEL7, so we can loosen the constraint.
sed -i 's/httplib2>=0.9.1/httplib2/' setup.py

# We do not have the package for google.appengine support
# This is removed because it breaks the docs build otherwise
rm -f docs/source/oauth2client.contrib.appengine.rst oauth2client/appengine.py

# Remove keyring support
rm oauth2client/contrib/keyring_storage.py tests/contrib/test_keyring_storage.py docs/source/oauth2client.contrib.keyring_storage.rst

%build
%py3_build

%install
%py3_install

%check
#tox -v --sitepackages -e py%%{python3_version_nodots}

# We remove tests currently, we will ship them eventually
# This is a bit of a hack until I package the test scripts in a separate package
rm -r $(find %{_buildrootdir} -type d -name 'tests') || /bin/true


%files -n python3-%{srcname}
%license LICENSE 
%doc CHANGELOG.md CONTRIBUTING.md README.md 
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1.3-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 4.1.3-9
- Don't BR tox if we don't run tests.

* Sat Oct 26 2019 Orion Poplawski <orion@nwra.com> - 4.1.3-8
- Drop py3dir
- Drop obsolete dependency on python-gflags

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 24 2019 Gwyn Ciesla <gwync@protonmail.com> - 4.1.3-6
- Drop Python 2.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1.3-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 30 2019 Miro Hrončok <mhroncok@redhat.com> - 4.1.3-3
- Don't ship docs, use python2 names to declare Python 2 dependencies

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Michele Baldessari <michele@acksyn.org> - 4.1.3-1
- New upstream
- Disable keyring requires as python-keyring is gone

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.2-6
- Rebuilt for Python 3.7

* Tue May 08 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.2-5
- Fix BuildRequires to require the tox command and not the python2 module

* Wed Mar 21 2018 Michele Baldessari <michele@acksyn.org> - 4.1.2-4
- Fix FTBFS due to missing python-django (rhbz#1556223)
- Set right version in the docs

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Michele Baldessari <michele@acksyn.org> - 4.1.2-1
- New upstream

* Sat May 13 2017 Michele Baldessari <michele@acksyn.org> - 4.1.0-1
- New upstream

* Thu Mar 30 2017 Ralph Bean <rbean@redhat.com> - 4.0.0-2
- Compat for EPEL7.

* Wed Mar 29 2017 Ralph Bean <rbean@redhat.com> - 4.0.0-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 27 2016 Michele Baldessari <michele@acksyn.org> - 3.0.0-3
- Fix python 3.6 breakage

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-2
- Rebuild for Python 3.6

* Thu Nov 10 2016 Michele Baldessari <michele@acksyn.org> - 3.0.0-1
- New upstream

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun May 22 2016 Michele Baldessari <michele@acksyn.org> - 2.1.0-1
- New upstream
* Tue Mar 08 2016 Michele Baldessari <michele@acksyn.org> - 2.0.1-1
- New upstream (NB: for now I am not shipping the tests, to be revised later)
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Thu Nov 26 2015 Michele Baldessari <michele@acksyn.org> - 1.5.2-2
- Remove dependency on sphinx-contrib-napoleon now that sphinx is at version >= 1.3
- Tighten versioned dependencies
- Update to latest python policy
* Thu Nov 19 2015 Michele Baldessari <michele@acksyn.org> - 1.5.2-1
- New upstream (BZ 1283443)
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Tue Oct 13 2015 Michele Baldessari <michele@acksyn.org> - 1.5.1-2
- Add versioned requires as per setup.py
* Thu Sep 17 2015 Michele Baldessari <michele@acksyn.org> - 1.5.1-1
- New upstream (BZ#1263881)
* Fri Sep 04 2015 Michele Baldessari <michele@acksyn.org> - 1.5.0-1
- New upstream (BZ#1259966)
* Sun Jul 12 2015 Michele Baldessari <michele@acksyn.org> - 1.4.12-1
- New upstream (BZ#1241304)
* Mon Jun 22 2015 Michele Baldessari <michele@acksyn.org> - 1.4.11-2
- Use -O1 for python3 as well
- Use python2 macros
- Remove the extra fonts from the -doc package
* Thu Jun 04 2015 Michele Baldessari <michele@acksyn.org> - 1.4.11-1
- Initial packaging
