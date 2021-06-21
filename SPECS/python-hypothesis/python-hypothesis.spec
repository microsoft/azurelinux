%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-hypothesis
Version:        3.71.0
Release:        4%{?dist}
Summary:        Python library for creating unit tests which are simpler to write and more powerful
License:        MPLv2.0
Group:          Development/Languages/Python
Url:            https://github.com/HypothesisWorks/hypothesis-python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/65/57/c4e2cc37a7b9de3d57a1cd6c200f931807cfdd9f7e05ef4c67fb9c507d65/hypothesis-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-enum34

Requires:       python2
Requires:       python2-libs
Requires:       python-enum34

BuildArch:      noarch

%description
Hypothesis is an advanced testing library for Python. It lets you write tests which are parametrized by a source of examples,
and then generates simple and comprehensible examples that make your tests fail. This lets you find more bugs in your code with less work

%package -n     python3-hypothesis
Summary:        Python library for creating unit tests which are simpler to write and more powerful
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-hypothesis

Python 3 version.

%prep
%setup -n hypothesis-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-hypothesis
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:36 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.71.0-4
- Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodizan <joslobo@microsoft.com> 3.71.0-3
-   Verified license.  Fixed Source0 download link. Remove sha1 define.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.71.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.71.0-1
-   Update to version 3.71.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.8.2-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-2
-   Changed python to python2
*   Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.8.2-1
-   Initial
