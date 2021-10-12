Summary:        Python documentation generator
Name:           python-sphinx
Version:        1.7.9
Release:        16%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.sphinx-doc.org
#Source0:       https://github.com/sphinx-doc/sphinx/archive/v%{version}.tar.gz
Source0:        Sphinx-%{version}.tar.gz
BuildArch:      noarch

%description
Python documentation generator

%package -n    python3-sphinx
Summary:        Python documentation generator
BuildRequires:  python3-babel
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-imagesize
BuildRequires:  python3-jinja2
BuildRequires:  python3-pygments
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-snowballstemmer
BuildRequires:  python3-sphinx-theme-alabaster
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-babel
Requires:       python3-docutils
Requires:       python3-imagesize
Requires:       python3-jinja2
Requires:       python3-libs
Requires:       python3-pygments
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-six
Requires:       python3-snowballstemmer
Requires:       python3-sphinx-theme-alabaster
Requires:       python3-sphinxcontrib-websupport
Provides:       python3-sphinx-locale = %{version}-%{release}
Provides:       python3-sphinx-doc = %{version}-%{release}

%description -n python3-sphinx
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

%prep
%autosetup -n Sphinx-%{version}

%build
%py3_build

%install
%py3_install
ln -sfv sphinx-quickstart %{buildroot}%{_bindir}/sphinx-quickstart-3
ln -sfv sphinx-quickstart %{buildroot}%{_bindir}/sphinx-quickstart3
ln -sfv sphinx-build %{buildroot}%{_bindir}/sphinx-build-3
ln -sfv sphinx-build %{buildroot}%{_bindir}/sphinx-build-%{python3_version}
ln -sfv sphinx-build %{buildroot}%{_bindir}/sphinx-build3
ln -sfv sphinx-autogen %{buildroot}%{_bindir}/sphinx-autogen-3
ln -sfv sphinx-autogen %{buildroot}%{_bindir}/sphinx-autogen3
ln -sfv sphinx-apidoc %{buildroot}%{_bindir}/sphinx-apidoc-3
ln -sfv sphinx-apidoc %{buildroot}%{_bindir}/sphinx-apidoc3

%check
%make_build -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-sphinx
%defattr(-,root,root)
%license LICENSE
%{_bindir}/sphinx-quickstart3
%{_bindir}/sphinx-build3
%{_bindir}/sphinx-autogen3
%{_bindir}/sphinx-apidoc3
%{_bindir}/sphinx-quickstart-3
%{_bindir}/sphinx-build-3
%{_bindir}/sphinx-build-%{python3_version}
%{_bindir}/sphinx-autogen-3
%{_bindir}/sphinx-apidoc-3
%{_bindir}/sphinx-quickstart
%{_bindir}/sphinx-build
%{_bindir}/sphinx-autogen
%{_bindir}/sphinx-apidoc
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.7.9-16
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Aug 10 2021 Jon Slobodzian <joslobo@microsoft.com> - 1.7.9-15
- Merged change from 1.0 branch and bumped dash number 
-   Mon Jun 14 2021 Tom Fay <tomfay@microsoft.com> - 1.7.9-12
-   Add python*-setuptools as a runtime dependency.
-   Clean spec.

* Mon Feb 15 2021 Henry Li <lihl@microsoft.com> - 1.7.9-14
- Provides python-sphinx-locale, python-sphinx-doc.

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.7.9-13
- Ship sphinx-build-3.7 symlink.

* Mon Dec 14 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.7.9-12
- Make python3- package default and python2- optional.
- Reserve unversioned sphinx-* binaries for python3.
- Rename python2 sphinx-* binaries to sphinx-*-2.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 1.7.9-11
- Add sphinx-*-3 binary symlinks for Fedora compatibility
- Add Requires: python(2/3)-sphinxcontrib-websupport
- Correct license shortname

* Tue Jun 02 2020 Jon Slobodzian <joslobo@microsoft.com> 1.7.9-10
- Add python-typing back.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.7.9-9
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-8
- Renaming python-pytest to pytest

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-7
- Renaming python-babel to babel

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-6
- Renaming python-Pygments to python-pygments

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-5
- Renaming python-alabaster to python-sphinx-theme-alabaster

* Mon Apr 13 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.7.9-4
- Remove python-typing from BuildRequires and Requires.

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 1.7.9-3
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.9-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.7.9-1
- Update to version 1.7.9

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.3-5
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-4
- Keep the original python2 scripts and rename the python3 scripts

* Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-3
- BuildRequires and Requires python-babel, python-docutils, python-jinja2,
  python-Pygments, python-six, python-alabaster, python-imagesize,
  python-requests and python-snowballstemmer. Adding python3 version

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.3-2
- Fix arch

* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.5.3-1
- Upgrade version to 1.5.3

* Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
- Initial
