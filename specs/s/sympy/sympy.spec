## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl  https://github.com/sympy/sympy
%global commit  fe935ceb303891d1f8bea4c03b19fd9ec9464b02

Name:           sympy
Version:        1.14.0
Release:        %autorelease
Summary:        A Python library for symbolic mathematics

# The project as a whole is BSD-3-Clause.
# The files in sympy/parsing/latex are MIT.
License:        BSD-3-Clause AND MIT
URL:            https://sympy.org/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/%{name}-%{version}.tar.gz
# For intersphinx
Source1:        https://matplotlib.org/stable/objects.inv#/objects-matplotlib.inv
Source2:        https://docs.scipy.org/doc/scipy/objects.inv#/objects-scipy.inv
# Do not depend on intersphinx_registry, which is not available in Fedora
Patch:          %{name}-intersphinx.patch

# We have to build on an architecture that:
# - Supports Java (for antlr4), which excludes 32-bit x86
# - Has lfortran, which includes x86_64 only
# - Has a version of llvmlite that doesn't crash, which excludes ppc64le,
#   s390x, and riscv64
# So even though this package is noarch, it can only be built on x86_64
ExclusiveArch:  %{x86_64} noarch
BuildArch:      noarch
BuildSystem:    pyproject
BuildOption(generate_buildrequires): -x dev
BuildOption(install): -l isympy sympy

BuildRequires:  antlr4
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  python3-clang
BuildRequires:  python3-devel
BuildRequires:  python3-numpy-doc
BuildRequires:  python3-numpy-f2py
BuildRequires:  %{py3_dist antlr4-python3-runtime}
BuildRequires:  %{py3_dist cython}
BuildRequires:  %{py3_dist gmpy2}
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  %{py3_dist numexpr}
BuildRequires:  %{py3_dist pycosat}
BuildRequires:  %{py3_dist scipy}

# Documentation
BuildRequires:  graphviz
BuildRequires:  ImageMagick
BuildRequires:  librsvg2-tools
BuildRequires:  make
BuildRequires:  %{py3_dist furo}
BuildRequires:  %{py3_dist linkify-it-py}
BuildRequires:  %{py3_dist matplotlib-inline}
BuildRequires:  %{py3_dist mpmath}
BuildRequires:  %{py3_dist myst-parser}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-copybutton}
BuildRequires:  %{py3_dist sphinx-math-dollar}
BuildRequires:  %{py3_dist sphinx-reredirects}
BuildRequires:  %{py3_dist sphinxcontrib-jquery}
BuildRequires:  python-mpmath-doc
BuildRequires:  tex(latex)
BuildRequires:  tex-dvipng

# Tests
BuildRequires:  lfortran
BuildRequires:  %{py3_dist autowrap}
BuildRequires:  %{py3_dist cloudpickle}
BuildRequires:  %{py3_dist ipython}
BuildRequires:  %{py3_dist lark}
BuildRequires:  %{py3_dist llvmlite}
BuildRequires:  %{py3_dist lxml}
BuildRequires:  %{py3_dist pytest-split}
BuildRequires:  %{py3_dist pytest-xdist}
BuildRequires:  %{py3_dist wurlitzer}
BuildRequires:  python3-z3

%global _description\
SymPy aims to become a full-featured computer algebra system (CAS)\
while keeping the code as simple as possible in order to be\
comprehensible and easily extensible. SymPy is written entirely in\
Python and does not require any external libraries.

%description %_description

%package -n python3-%{name}
Summary:        A Python3 library for symbolic mathematics
Recommends:     tex(latex)
Recommends:     tex(amsfonts.sty)
Recommends:     tex(amsmath.sty)
Recommends:     tex(euler.sty)
Recommends:     tex(eulervm.sty)
Recommends:     tex(standalone.cls)
Recommends:     %{py3_dist antlr4-python3-runtime}
Recommends:     %{py3_dist cython}
Recommends:     %{py3_dist gmpy2}
Recommends:     %{py3_dist matplotlib}
Recommends:     %{py3_dist numexpr}
Recommends:     %{py3_dist pycosat}
Recommends:     %{py3_dist pyglet}
Recommends:     %{py3_dist scipy}

%description -n python3-%{name}
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%package doc
# This project is BSD-3-Clause.  Other files bundled with the documentation
# have the following licenses:
# - searchindex.js: BSD-2-Clause
# - _static/basic.css: BSD-2-Clause
# - _static/clipboard.min.js: MIT
# - _static/copy*: MIT
# - _static/doctools.js: BSD-2-Clause
# - _static/graphviz.js: BSD-2-Clause
# - _static/jquery*.js: MIT
# - _static/language_data.js: BSD-2-Clause
# - _static/plot_directive.css: PSF-2.0 (see note)
# - _static/pygments.css: BSD-2-Clause
# - _static/scripts/*: MIT
# - _static/searchtools.js: BSD-2-Clause
# - _static/styles/*: MIT
# - _static/underscore*.js: MIT
#
# NOTE: The license of _static/plot_directive.css is the same as the license of
# matplotlib.  The matplotlib license is functionally identical to PSF-2.0, but
# uses different organization and project names.  I am using the PSF-2.0
# identifier for now, because there is no valid SPDX choice.  Revisit this.
License:        BSD-3-Clause AND BSD-2-Clause AND MIT AND PSF-2.0
Summary:        Documentation for sympy
Provides:       bundled(js-jquery)
Provides:       bundled(js-underscore)

# This can be removed when F46 reaches EOL
Obsoletes:      %{name}-examples < 1.14.0
Provides:       %{name}-examples = %{version}-%{release}

%description doc
HTML documentation for sympy.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%conf
fixtimestamp() {
  touch -r $1.orig $1
  rm -f $1.orig
}

# Remove bogus shebangs
for fil in sympy/physics/mechanics/models.py \
           sympy/physics/optics/polarization.py; do
  sed -i.orig '/env python/d' $fil
  fixtimestamp $fil
done

# Do not depend on env
for fil in $(grep -rl "^#\![[:blank:]]*%{_bindir}/env" .); do
  sed -i.orig 's,^\(#\![[:blank:]]*%{_bindir}/\)env python,\1python3,' $fil
  fixtimestamp $fil
done

# Use local objects.inv for intersphinx
sed -e "s|\('https://matplotlib\.org/stable/', \)None|\1'%{SOURCE1}'|" \
    -e "s|\(.https://docs\.scipy\.org/doc/scipy/., \)None|\1'%{SOURCE2}'|" \
    -e "s|\(.https://numpy\.org/doc/stable/., \)None|\1'%{_docdir}/python3-numpy-doc/objects.inv'|" \
    -i doc/src/conf.py

# Help sphinx find the git commit
echo -n '%{commit}' > doc/commit_hash.txt

# Permit use of antlr4 4.13
sed -i s'/4\.11/4.13/g' sympy/parsing/autolev/_parse_autolev_antlr.py \
    sympy/parsing/latex/_parse_latex_antlr.py

%build -p
# Regenerate the ANTLR files
%{python3} setup.py antlr

%build -a
# Build the documentation
pushd doc
make html SPHINXOPTS=%{?_smp_mflags} PYTHON=%{python3}
make cheatsheet
popd

%install -a
## Remove extra files
rm -f %{buildroot}%{_bindir}/{,doc}test

# Fix permissions
chmod 0755 %{buildroot}%{python3_sitelib}/sympy/benchmarks/bench_symbench.py \
      %{buildroot}%{python3_sitelib}/sympy/testing/tests/diagnose_imports.py

# Install the HTML documentation and link duplicates
mkdir -p %{buildroot}%{_docdir}/%{name}-doc
cp -a doc/_build/html %{buildroot}%{_docdir}/%{name}-doc
rm -f %{buildroot}%{_docdir}/%{name}-doc/html/.buildinfo
rm -fr %{buildroot}%{_docdir}/%{name}-doc/i18n
%fdupes %{buildroot}%{_docdir}/%{name}-doc

%check
%{python3} bin/test -v --parallel

%files -n python3-%{name} -f %{pyproject_files}
%doc AUTHORS README.md
%doc doc/_build/cheatsheet/cheatsheet.pdf
%doc doc/_build/cheatsheet/combinatoric_cheatsheet.pdf
%{_bindir}/isympy
%{_mandir}/man1/isympy.1*

%files doc
%docdir %{_docdir}/%{name}-doc/html
%{_docdir}/%{name}-doc/html

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.14.0-8
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.14.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.14.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.0-5
- Add noarch to ExclusiveArch

* Wed Aug 06 2025 Jerry James <loganjerry@gmail.com> - 1.14.0-4
- Make the package noarch again
- Use the pyproject declarative buildsystem
- Restrict build to x86_64
- Remove note about aesara, which has fallen into disrepair

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 1.14.0-2
- Rebuilt for Python 3.14

* Tue Apr 29 2025 Jerry James <loganjerry@gmail.com> - 1.14.0-1
- Version 1.14.0
- Drop upstreamed tempfile flush patch
- Add patch to avoid intersphinx_registry
- Drop workaround for buggy lark on ppc64le
- Drop examples subpackage

* Tue Mar 18 2025 Jerry James <loganjerry@gmail.com> - 1.13.3-4
- Fix a python 3.14 test failure (rhbz#2353123)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.13.3-2
- Disable llvmlite on riscv64

* Thu Sep 19 2024 Jerry James <loganjerry@gmail.com> - 1.13.3-1
- Version 1.13.3

* Mon Aug 12 2024 Jerry James <loganjerry@gmail.com> - 1.13.2-1
- Version 1.13.2

* Fri Jul 19 2024 Jerry James <loganjerry@gmail.com> - 1.13.1-1
- Version 1.13.1

* Thu Jul 11 2024 Jerry James <loganjerry@gmail.com> - 1.13.0-1
- Version 1.13.0
- Drop unnecessary circuitplot patch
- Drop upstreamed incompatible-pointer patch
- Link duplicate documentation files
- Run tests on all architectures

* Wed Jun 12 2024 Jerry James <loganjerry@gmail.com> - 1.12.1-1
- Version 1.12.1
- Drop upstreamed python 3.12 patch

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 1.12-9
- Rebuilt for Python 3.13

* Mon Jun 10 2024 Miro Hrončok <miro@hroncok.cz> - 1.12-8
- Drop unneeded build dependency on sphinx-autobuild

* Fri Mar 22 2024 Jerry James <loganjerry@gmail.com> - 1.12-7
- Fix test failure with python 3.13 (rhbz#2271058)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 Jerry James <loganjerry@gmail.com> - 1.12-3
- Fix incompatible pointer types for GCC 14 compatibility

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Jerry James <loganjerry@gmail.com> - 1.12-1
- Version 1.12
- Add patch for python 3.12 compatibility

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 1.11.1-5
- Rebuilt for Python 3.12

* Tue Feb 21 2023 Jerry James <loganjerry@gmail.com> - 1.11.1-4
- Fix the antlr4 Recommends (bz 2172030)
- Dynamically generate BuildRequires (to the extent possible)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 27 2022 Jerry James <loganjerry@gmail.com> - 1.11.1-2
- Do not run antlr on i386 where it doesn't exist
- Be archful so we don't BR a package that doesn't exist on i386

* Tue Sep  6 2022 Jerry James <loganjerry@gmail.com> - 1.11.1-1
- Version 1.11.1
- Convert License tag to SPDX
- Drop upstreamed patches: -tests, -distutils, -signature
- Drop fastcache dependency
- Regenerate ANTLR4 files

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.10.1-2
- Rebuilt for Python 3.11

* Sat Mar 19 2022 Jerry James <loganjerry@gmail.com> - 1.10.1-1
- Version 1.10.1

* Thu Mar 17 2022 Jerry James <loganjerry@gmail.com> - 1.10-1
- Version 1.10
- Drop upstreamed patches: -python3, -png-decoder, -gmpy2-mpq,
  and -rational-exponent

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct  8 2021 Jerry James <loganjerry@gmail.com> - 1.9-1
- Version 1.9
- Drop theano support due to incompatibility with the Fedora version
- Add -tests, -distutils, -gmpy2-mpq, and -rational-exponent patches to
  work around test failures

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8-2~bootstrap
- Build in bootstrap mode to work-around missing theano

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8-2
- Rebuilt for Python 3.10

* Mon Apr 12 2021 Jerry James <loganjerry@gmail.com> - 1.8-1
- Version 1.8
- Drop the -float patch and only run tests on x86_64
- Add -circuitplot patch to skip tests that fail with no display
- Drop the -texmacs subpackage; the TeXmacs package ships its own sympy plugin

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 12 2020 Jerry James <loganjerry@gmail.com> - 1.7.1-1
- Version 1.7.1

* Thu Dec 10 2020 Jerry James <loganjerry@gmail.com> - 1.7-2
- Fix preview of PNG images (bz 1906363)
- Add missing Recommends needed to preview images (bz 1906363)

* Sat Nov 28 2020 Jerry James <loganjerry@gmail.com> - 1.7-1
- Version 1.7

* Thu Nov 26 2020 Jerry James <loganjerry@gmail.com> - 1.6.2-2
- Update Theano dependency for Theano-PyMC
- Add -theano-pymc patch to adapt

* Mon Aug 10 2020 Jerry James <loganjerry@gmail.com> - 1.6.2-1
- Version 1.6.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Jerry James <loganjerry@gmail.com> - 1.6.1-1
- Version 1.6.1
- Drop upstreamed -ast patch

* Wed Jun 24 2020 Jerry James <loganjerry@gmail.com> - 1.6-2
- Add setuptools BR
- Add -ast patch to fix compilation with python 3.9

* Fri May 29 2020 Jerry James <loganjerry@gmail.com> - 1.6-1
- Version 1.6
- Drop upstreamed -doc and -sample-set patches
- Disable testing on 32-bit systems; too many tests need 64-bit integers

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.1-4
- Rebuilt for Python 3.9

* Mon May 11 2020 Jerry James <loganjerry@gmail.com> - 1.5.1-3
- Add -sample-set patch to fix test failure with python 3.9

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan  8 2020 Jerry James <loganjerry@gmail.com> - 1.5.1-1
- Update to 1.5.1
- Drop upstreamed patches
- Drop upstreamed workaround for numpy with a release candidate version

* Mon Nov  4 2019 Jerry James <loganjerry@gmail.com> - 1.4-6
- Fix broken dependencies in the -texmacs subpackage
- Recommend numexpr

* Fri Sep 13 2019 Jerry James <loganjerry@gmail.com> - 1.4-5
- Add one more patch to fix a python 3.8 warning

* Sat Aug 24 2019 Robert-André Mauchin <zebob.m@gmail.com>  - 1.4-4
- Add patches to fix build with Python 3.8 and Numpy 1.17

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Jerry James <loganjerry@gmail.com> - 1.4-1
- Update to 1.4
- Drop -factorial patch

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Jerry James <loganjerry@gmail.com> - 1.3-2
- Add -sympify and -factorial patches to work around test failures

* Mon Jan 14 2019 Jerry James <loganjerry@gmail.com> - 1.3-2
- Drop Requires from the -doc subpackage (bz 1665767)

* Sat Oct  6 2018 Jerry James <loganjerry@gmail.com> - 1.3-1
- Update to 1.3
- Drop upstreamed patches: subexpr-lambdify, test-code-quality, tex-encoding
- Drop the python2 subpackage
- Add -python3 patch to ask cython to generate python 3 code

* Tue Aug 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2-2
- Fix _subexpr method in lambdify

* Sat Jul 21 2018 Jerry James <loganjerry@gmail.com> - 1.2-1
- Update to 1.2 (bz 1599502)
- Drop upstreamed -python3 patch
- Add -test-code-quality and -doc patches

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-5
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.1-2
- Python 2 binary package renamed to python2-sympy
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Jerry James <loganjerry@gmail.com> - 1.1.1-1
- Update to 1.1.1 (bz 1468405)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Jerry James <loganjerry@gmail.com> - 1.1-3
- Fix dependency on python2 from python3 package (bz 1471886)

* Sat Jul  8 2017 Jerry James <loganjerry@gmail.com> - 1.1-2
- Disable tests that fail due to overflow on some 32-bit architectures

* Fri Jul  7 2017 Jerry James <loganjerry@gmail.com> - 1.1-1
- Update to 1.1 (bz 1468405)
- All patches have been upstreamed; drop them all

* Sat Apr  1 2017 Jerry James <loganjerry@gmail.com> - 1.0-7
- Update theano test for theano 0.9

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Iryna Shcherbina <ishcherb@redhat.com> - 1.0-5
- Make documentation scripts non-executable to avoid
  autogenerating Python 2 dependency in sympy-examples (#1360766)

* Fri Jan 13 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0-4
- Run tests in parallel
- Work around some broken tests
- Use python3 in texmacs-sympy (#1360766)

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0-4
- Rebuild for Python 3.6

* Fri Jul 22 2016 Jerry James <loganjerry@gmail.com> - 1.0-3
- Update the -test patch for the latest matplotlib release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Apr  2 2016 Jerry James <loganjerry@gmail.com> - 1.0-2
- Fix bad /usr/bin/env substitution

* Thu Mar 31 2016 Jerry James <loganjerry@gmail.com> - 1.0-1
- Update to 1.0
- All patches have been upstreamed; drop them all
- Add -test patch to fix test failures with recent mpmath
- Recommend scipy

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Sep  3 2015 Jerry James <loganjerry@gmail.com> - 0.7.6.1-1
- Update to 0.7.6.1 (bz 1259971)

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.6-3
- Fix failure in tests (#1240097)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec  5 2014 Jerry James <loganjerry@gmail.com> - 0.7.6-1
- Update to 0.7.6
- Drop upstreamed -test and -is-tangent patches
- Drop obsolete bug workarounds
- Add python(3)-fastcache BR and R
- Recommend python-theano
- Fix executable bits on tm_sympy

* Tue Sep 16 2014 Jerry James <loganjerry@gmail.com> - 0.7.5-4
- Drop python3-six BR and R now that bz 1140413 is fixed
- Use gmpy2

* Wed Sep  3 2014 Jerry James <loganjerry@gmail.com> - 0.7.5-3
- Install both isympy and python3-isympy to comply with packaging standards
- Add -is-tangent patch (bz 1135677)
- Temporarily disable tests that fail due to mpmath bugs (bz 1127796)
- Fix license handling
- Add python3-six BR and R; see bz 1140413 for details

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 13 2014 Jerry James <loganjerry@gmail.com> - 0.7.5-1
- Update to 0.7.5 (bz 1066951)
- Binaries now default to using python3
- Use py3dir macro to simplify python3 build
- Add BRs for more comprehensive testing
- Workaround bz 1075826
- Add -test patch to fix Unicode problem in the tests

* Mon Dec  9 2013 Jerry James <loganjerry@gmail.com> - 0.7.4-1
- Update to 0.7.4
- Python 2 and 3 sources are now in the same tarball

* Fri Oct 18 2013 Jerry James <loganjerry@gmail.com> - 0.7.3-2
- Build a python3 subpackage (bz 982759)

* Fri Aug  2 2013 Jerry James <loganjerry@gmail.com> - 0.7.3-1
- Update to 0.7.3
- Upstream dropped all tutorial translations
- Add graphviz BR for documentation
- Sources now distributed from github instead of googlecode
- Adapt to versionless _docdir in Rawhide

* Mon Jun 17 2013 Jerry James <loganjerry@gmail.com> - 0.7.2-1
- Update to 0.7.2 (bz 866044)
- Add python-pyglet R (bz 890312)
- Package the TeXmacs integration
- Build and provide documentation
- Provide examples
- Minor spec file cleanups

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-5
- Patch around BZ #564504.

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.7-4
- fix a python 2.7 incompatibility

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-2
- Added %%check phase.

* Tue Apr 27 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.7-1
- Update to 0.6.7.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 0.6.6-3
- Patch around private copy nicely; avoid breakage from trying to replace
  a directory with a symlink.

* Mon Feb 15 2010 Conrad Meyer <konrad@tylerc.org> - 0.6.6-2
- Remove private copy of system lib 'mpmath' (rhbz #551576).

* Sun Dec 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.6-1
- Update to 0.6.6.

* Sat Nov 07 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.6.5-1
- Update to 0.6.5.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.3-1
- Bump to 0.6.3, supports python 2.6.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.2-3
- Rebuild for Python 2.6

* Mon Oct 13 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.2-2
- Patch to remove extraneous shebangs.

* Sun Oct 12 2008 Conrad Meyer <konrad@tylerc.org> - 0.6.2-1
- Initial package.

## END: Generated by rpmautospec
