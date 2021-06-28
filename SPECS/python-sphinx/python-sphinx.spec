%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Python documentation generator
Name:           python-sphinx
Version:        1.7.9
Release:        12%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.sphinx-doc.org
#Source0:      https://github.com/sphinx-doc/sphinx/archive/v%{version}.tar.gz
Source0:        Sphinx-%{version}.tar.gz
BuildRequires:  babel
BuildRequires:  pytest
BuildRequires:  python-docutils
BuildRequires:  python-imagesize
BuildRequires:  python-jinja2
BuildRequires:  python-pip
BuildRequires:  python-pygments
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-snowballstemmer
BuildRequires:  python-sphinx-theme-alabaster
BuildRequires:  python-typing
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:       babel
Requires:       python-docutils
Requires:       python-imagesize
Requires:       python-jinja2
Requires:       python-pygments
Requires:       python-requests
Requires:       python-setuptools
Requires:       python-six
Requires:       python-snowballstemmer
Requires:       python-sphinx-theme-alabaster
Requires:       python-typing
Requires:       python2
Requires:       python2-libs
Requires:       python2-sphinxcontrib-websupport
BuildArch:      noarch

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

%package -n    python3-sphinx
Summary:        Python documentation generator
BuildRequires:  python3
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

%description -n python3-sphinx

Python 3 version.

%prep
%setup -q -n Sphinx-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mv %{buildroot}/%{_bindir}/sphinx-quickstart %{buildroot}/%{_bindir}/sphinx-quickstart3
mv %{buildroot}/%{_bindir}/sphinx-build %{buildroot}/%{_bindir}/sphinx-build3
mv %{buildroot}/%{_bindir}/sphinx-autogen %{buildroot}/%{_bindir}/sphinx-autogen3
mv %{buildroot}/%{_bindir}/sphinx-apidoc %{buildroot}/%{_bindir}/sphinx-apidoc3
ln -sfv sphinx-quickstart3 %{buildroot}%{_bindir}/sphinx-quickstart-3
ln -sfv sphinx-build3 %{buildroot}%{_bindir}/sphinx-build-3
ln -sfv sphinx-autogen3 %{buildroot}%{_bindir}/sphinx-autogen-3
ln -sfv sphinx-apidoc3 %{buildroot}%{_bindir}/sphinx-apidoc-3
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/sphinx-quickstart
%{_bindir}/sphinx-build
%{_bindir}/sphinx-autogen
%{_bindir}/sphinx-apidoc
%{python2_sitelib}/*

%files -n python3-sphinx
%defattr(-,root,root)
%{_bindir}/sphinx-quickstart3
%{_bindir}/sphinx-build3
%{_bindir}/sphinx-autogen3
%{_bindir}/sphinx-apidoc3
%{_bindir}/sphinx-quickstart-3
%{_bindir}/sphinx-build-3
%{_bindir}/sphinx-autogen-3
%{_bindir}/sphinx-apidoc-3
%{python3_sitelib}/*

%changelog
* Mon Jun 14 2021 Tom Fay <tomfay@microsoft.com> - 1.7.9-12
- Add python*-setuptools as a runtime dependency.
- Clean spec.

*   Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 1.7.9-11
-   Add sphinx-*-3 binary symlinks for Fedora compatibility
-   Add Requires: python(2/3)-sphinxcontrib-websupport
-   Correct license shortname
-   License verified

*   Tue Jun 02 2020 Jon Slobodzian <joslobo@microsoft.com> 1.7.9-10
-   Add python-typing back.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.7.9-9
-   Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-8
-   Renaming python-pytest to pytest

*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-7
-   Renaming python-babel to babel

*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-6
-   Renaming python-Pygments to python-pygments

*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 1.7.9-5
-   Renaming python-alabaster to python-sphinx-theme-alabaster

*   Mon Apr 13 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.7.9-4
-   Remove python-typing from BuildRequires and Requires.

*   Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> 1.7.9-3
-   Update URL.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.9-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.7.9-1
-   Update to version 1.7.9

*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.3-5
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-4
-   Keep the original python2 scripts and rename the python3 scripts

*   Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-3
-   BuildRequires and Requires python-babel, python-docutils, python-jinja2,
    python-Pygments, python-six, python-alabaster, python-imagesize,
    python-requests and python-snowballstemmer. Adding python3 version

*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.3-2
-   Fix arch

*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.5.3-1
-   Upgrade version to 1.5.3

*   Fri Dec 16 2016 Dheeraj Shetty <dheerajs@vmware.com> 1.5.1-1
-   Initial
