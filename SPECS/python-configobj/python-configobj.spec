%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-configobj
Version:        5.0.6
Release:        6%{?dist}
Summary:        Config file reading, writing and validation
License:        BSD
Group:          Development/Languages/Python
Url:            https://github.com/DiffSK/configobj
# Source to be fixed as part of https://microsoft.visualstudio.com/OS/_workitems/edit/25936171.
Source0:        https://files.pythonhosted.org/packages/64/61/079eb60459c44929e684fa7d9e2fdca403f67d64dd9dbac27296be2e0fab/configobj-%{version}.tar.gz
Source1:        LICENSE.BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python-six

BuildArch:      noarch

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.

%package -n     python3-configobj
Summary:        python-configobj

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3-six

%description -n python3-configobj
Python 3 version.

%prep
%setup -q -n configobj-%{version}
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
cp %{SOURCE1} ./

%check
python2 validate.py
pushd ../p3dir
python3 validate.py
popd

%files
%defattr(-,root,root,-)
%license LICENSE.BSD
%{python2_sitelib}/*


%files -n python3-configobj
%defattr(-,root,root)
%license LICENSE.BSD
%{python3_sitelib}/*

%changelog
*   Wed May 27 2020 Nick Samson <nisamson@microsoft.com> 5.0.6-6
-   Added License file and %%license invocation
*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 5.0.6-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Fixed "Source0" tag.
-   License verified.
-   Removed "%%define sha1".
-   Making %%setup quiet.
*   Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.6-4
-   Adding python 3 support.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 5.0.6-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.0.6-2
-   GA - Bump release of all rpms
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
