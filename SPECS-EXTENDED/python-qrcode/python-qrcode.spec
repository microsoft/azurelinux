%bcond_with missing_dependencies

Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pkgname qrcode

Name:           python-%{pkgname}
Version:        6.1
Release:        6%{?dist}
Summary:        Python QR Code image generator

License:        BSD
URL:            https://github.com/lincolnloop/python-qrcode
Source0:        https://pypi.python.org/packages/source/q/qrcode/qrcode-%{version}.tar.gz#/python-qrcode-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

%if %{with missing_dependencies}
BuildRequires:  python3-imaging
%endif

%global _description\
This module uses the Python Imaging Library (PIL) to allow for the\
generation of QR Codes.

%description %_description

%package -n python3-%{pkgname}
Summary:        Python QR Code image generator
%if %{with missing_dependencies}
Requires:       python3-imaging
%endif
# For entry point:
Requires:       python3-setuptools
Requires:       python3-%{pkgname}-core = %{version}-%{release}

%description -n python3-%{pkgname}
This module uses the Python Imaging Library (PIL) to allow for the
generation of QR Codes. Python 3 version.

%package -n python3-%{pkgname}-core
Requires:       python3-six
Summary:        Python 3 QR Code image generator (core library)

%description -n python3-%{pkgname}-core
Core Python 3 module for QR code generation. Does not contain image rendering.

%prep
%autosetup -n qrcode-%{version}

# The pure plugin requires pymaging which is not packaged in Fedora.
rm qrcode/image/pure.py*

# Remove shebang
sed -i '1d' qrcode/console_scripts.py

%build
%py3_build

%install
%py3_install

# Do not install tests
rm -r %{buildroot}%{python3_sitelib}/%{pkgname}/tests

#
# In previous iterations of the package, the qr script had been
# renamed to qrcode. This was an unnecessary change from upstream.
#
# We cary this symlink to maintain compat with old packages.
#
ln -s qr %{buildroot}%{_bindir}/qrcode

%check
# in lieue of a real test suite
modules=$(find qrcode -name '*.py' \
          | grep -v __init__ \
          | sort \
          | sed -e 's|/|.|g' \
          | sed -e 's|.py$||g');


for m in $modules;
do
    %{__python3} -c "import $m"
done

%files -n python3-%{pkgname}
%{_bindir}/qr
%{_bindir}/qrcode
%{_mandir}/man1/qr.1*
%{python3_sitelib}/%{pkgname}/image/svg.py*
%{python3_sitelib}/%{pkgname}/image/pil.py*
%{python3_sitelib}/%{pkgname}/image/__pycache__/svg.*
%{python3_sitelib}/%{pkgname}/image/__pycache__/pil.*

%files -n python3-%{pkgname}-core
%doc README.rst CHANGES.rst
%license LICENSE
%dir %{python3_sitelib}/%{pkgname}/
%dir %{python3_sitelib}/%{pkgname}/image
%dir %{python3_sitelib}/%{pkgname}/image/__pycache__
%{python3_sitelib}/%{pkgname}*.egg-info
%{python3_sitelib}/%{pkgname}/*.py*
%{python3_sitelib}/%{pkgname}/__pycache__
%{python3_sitelib}/%{pkgname}/image/__init__.py*
%{python3_sitelib}/%{pkgname}/image/base.py*
%{python3_sitelib}/%{pkgname}/image/__pycache__/__init__.*
%{python3_sitelib}/%{pkgname}/image/__pycache__/base.*

%changelog
* Tue Aug 31 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disabling optional dependency on "python-pillow".

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 6.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 26 2019 Fabian Affolter <mail@fabian-affolter.ch> - 6.1-1
- Update to latest upstream release 6.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-14
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.1-12
- Rebuilt for Python 3.7

* Fri Mar 23 2018 Iryna Shcherbina <ishcherb@redhat.com> - 5.1-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-10
- Also rename python-qrcode-core to python2-qrcode-core

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-8
- Python 2 binary package renamed to python2-qrcode
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.1-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 10 2015 Miro Hrončok <mhroncok@redhat.com> - 5.1-1
- Update to 5.1
- Introduce python3 subpackages (#1237118)
- Moved LICENSE from %%doc to %%license

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-2
- Make python-qrcode-core conflicts with python-qrcode < 5.0

* Wed Sep 10 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Tue Sep 09 2014 Nathaniel McCallum <npmccallum@redhat.com> - 2.4.1-7
- Create -core subpackage for minimal dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-2
- Clean up spec, removing unnecessary declarations
- Rename tool in %%{_bindir} to the less ambiguous qrcode

* Sat Jun  2 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-1
- Initial package
