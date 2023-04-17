%global _description %{expand:
Mpmath is a pure-Python library for multiprecision floating-point
arithmetic. It provides an extensive set of transcendental functions,
unlimited exponent sizes, complex numbers, interval arithmetic,
numerical integration and differentiation, root-finding, linear
algebra, and much more. Almost any calculation can be performed just
as well at 10-digit or 1000-digit precision, and in many cases mpmath
implements asymptotically fast algorithms that scale well for
extremely high precision work. If available, mpmath will (optionally)
use gmpy to speed up high precision operations.}
Summary:        A pure Python library for multiprecision floating-point arithmetic
Name:           python-mpmath
Version:        1.3.0
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://mpmath.org
# Source code
Source0:        https://github.com/fredrik-johansson/mpmath/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-sphinx
BuildRequires:  xorg-x11-server-Xvfb
BuildArch:      noarch

%description %{_description}

%package -n python3-mpmath
%{?python_provide:%python_provide python3-mpmath}
Summary:        A pure Python library for multiprecision floating-point arithmetic

%description -n python3-mpmath %{_description}

If you require plotting capabilities in mpmath, install python3-matplotlib.

%package doc
Summary:        HTML documentation for %{name}
Requires:       python3-mpmath = %{version}-%{release}

%description doc
This package contains the HTML documentation for %{name}.

%prep
%setup -q -n mpmath-%{version}

# Convert line encodings
for doc in CHANGES LICENSE README.rst TODO mpmath/tests/runtests.py; do
 sed "s|\r||g" $doc > $doc.new && \
 touch -r $doc $doc.new && \
 mv $doc.new $doc
done
find docs -name *.txt -exec sed -i "s|\r||g" {} \;

shebangs="mpmath/matrices/eigen.py mpmath/matrices/eigen_symmetric.py mpmath/tests/runtests.py mpmath/tests/test_eigen.py mpmath/tests/test_eigen_symmetric.py mpmath/tests/test_levin.py"
# Get rid of unnecessary shebangs
for lib in $shebangs; do
 sed '/^#!.*/d; 1q' $lib > $lib.new && \
 touch -r $lib $lib.new && \
 mv $lib.new $lib
done

sed -i -r 's/use_scm_version=True/version="%{version}"/' setup.py

%build
%py3_build


%install
%py3_install

%check
cd build/lib/mpmath/tests/
xvfb-run -a pytest -v

%files -n python3-mpmath
%license LICENSE
%doc CHANGES README.rst
%{python3_sitelib}/mpmath/
%{python3_sitelib}/mpmath-%{version}-*.egg-info

%changelog
* Thu Apr 06 2023 Riken Maharjan <rmaharjan@microsoft.com> - 1.3.0-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- License Verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.0-2
- Rebuilt for Python 3.10

* Tue Feb  2 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.0-1
- Update to latest version (#1923815)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Subpackage python2-mpmath has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Mar 11 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.0-2
- Build docs using python3-sphinx

* Mon Feb 18 2019 Yatin Karel <ykarel@redhat.com> - 1.1.0-1
- Update to 1.1.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-2
- Rebuilt for Python 3.7

* Fri May 04 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.19-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.19-10
- Python 2 binary package renamed to python2-mpmath
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.19-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 04 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.19-2
- Patch for BZ #1127796.

* Tue Jun 24 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.19-1
- Update to 0.19.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Jan 01 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.18-1
- Update to 0.18.

* Tue Aug 06 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.17-8
- Add python3 package.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.17-5
- Fix %%check phase.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.17-1
- Update to 0.17.

* Sun Sep 26 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.16-1
- Update to 0.16.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 07 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.15-1
- Update to 0.15.

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.14-1
- Update to 0.14.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-5
- Removed BR: python-matplotlib, since it didn't actually help in the missing
  image problem.
- Added versioned require in -doc.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-4
- Replaced R: python-matplotlib with a comment in %%description.
- Added missing BR: python-matplotlib.

* Tue Oct 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-3
- Added missing BR: dvipng.
- Added %%check phase.

* Wed Sep 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-2
- Add missing BR: tex(latex).

* Wed Sep 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.13-1
- First release.
