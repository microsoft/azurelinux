Vendor:         Microsoft Corporation
Distribution:   Mariner
# Share docs between packages for multiple python versions
%global _docdir_fmt %{name}

# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

Summary:	Cryptography library for Python
Name:		python-crypto
Version:	2.6.1
Release:	31%{?dist}
# Mostly Public Domain apart from parts of HMAC.py and setup.py, which are Python
License:	Public Domain and Python
URL:		http://www.pycrypto.org/
Source0:	http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
Patch0:		python-crypto-2.4-optflags.patch
Patch1:		python-crypto-2.4-fix-pubkey-size-divisions.patch
Patch2:		pycrypto-2.6.1-CVE-2013-7459.patch
Patch3:		pycrypto-2.6.1-unbundle-libtomcrypt.patch
Patch4:		python-crypto-2.6.1-link.patch
Patch5:		pycrypto-2.6.1-CVE-2018-6594.patch
Patch6:		pycrypto-2.6.1-use-os-random.patch
Patch7:		pycrypto-2.6.1-drop-py2.1-support.patch
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	libtomcrypt-devel >= 1.16
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	%{_bindir}/2to3

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

%package -n python%{python3_pkgversion}-crypto
Summary:	Cryptography library for Python 3
%{?python_provide:%python_provide python%{python3_pkgversion}-crypto}

%description -n python%{python3_pkgversion}-crypto
PyCrypto is a collection of both secure hash functions (such as MD5 and
SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

This is the Python 3 build of the package.

%prep
%setup -n pycrypto-%{version} -q

# Use distribution compiler flags rather than upstream's
%patch0 -p1

# Fix divisions within benchmarking suite:
%patch1 -p1

# AES.new with invalid parameter crashes python
# https://github.com/dlitz/pycrypto/issues/176
# CVE-2013-7459
%patch2 -p1

# Unbundle libtomcrypt (#1087557)
rm -rf src/libtom
%patch3

# log() not available in libgmp, need libm too
%patch4

# When creating ElGamal keys, the generator wasn't a square residue: ElGamal
# encryption done with those keys cannot be secure under the DDH assumption
# https://bugzilla.redhat.com/show_bug.cgi?id=1542313 (CVE-2018-6594)
# https://github.com/TElgamal/attack-on-pycrypto-elgamal
# https://github.com/Legrandin/pycryptodome/issues/90
# https://github.com/dlitz/pycrypto/issues/253
# Patch based on this commit from cryptodome:
# https://github.com/Legrandin/pycryptodome/commit/99c27a3b
# Converted to pull request for pycrypto:
# https://github.com/dlitz/pycrypto/pull/256
%patch5

# Replace the user-space RNG with a thin wrapper to os.urandom
# Based on https://github.com/Legrandin/pycryptodome/commit/afd6328f
# Fixes compatibility with Python 3.8 (#1718332)
%patch6

# We already require Python 2.4 or later, so drop support for Python 2.1
# in the code
%patch7

# setup.py doesn't run 2to3 on pct-speedtest.py
cp pct-speedtest.py pct-speedtest3.py
2to3 -wn pct-speedtest3.py

%build
%global optflags %{optflags} -fno-strict-aliasing
%py3_build

%install
%py3_install

# Remove group write permissions on shared objects
find %{buildroot}%{python3_sitearch} -name '*.so' -exec chmod -c g-w {} \;

%check
%{__python3} setup.py test

# Benchmark
PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} pct-speedtest3.py

%files -n python%{python3_pkgversion}-crypto
%license COPYRIGHT LEGAL/
%doc README TODO ACKS ChangeLog Doc/
%{python3_sitearch}/Crypto/
%{python3_sitearch}/pycrypto-%{version}-py3.*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.1-31
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Wed Jan 29 2020 Paul Howarth <paul@city-fan.org> - 2.6.1-30
- Drop Python 2 support

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-29
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-28
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun  7 2019 Paul Howarth <paul@city-fan.org> - 2.6.1-26
- Replace the user-space RNG with a thin wrapper to os.urandom
  - Based on https://github.com/Legrandin/pycryptodome/commit/afd6328f
  - Fixes compatibility with Python 3.8 (#1718332)
- Drop support for Python 2.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.1-23
- Rebuilt for Python 3.7

* Fri Feb 23 2018 Paul Howarth <paul@city-fan.org> - 2.6.1-22
- When creating ElGamal keys, the generator wasn't a square residue: ElGamal
  encryption done with those keys cannot be secure under the DDH assumption
  https://bugzilla.redhat.com/show_bug.cgi?id=1542313 (CVE-2018-6594)
  https://github.com/TElgamal/attack-on-pycrypto-elgamal
  https://github.com/Legrandin/pycryptodome/issues/90
  https://github.com/dlitz/pycrypto/issues/253
  https://github.com/dlitz/pycrypto/pull/256

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Paul Howarth <paul@city-fan.org> - 2.6.1-20
- log() not available in libgmp, need libm too

* Mon Oct 23 2017 Simone Caronni <negativo17@gmail.com> - 2.6.1-19
- Rebuild for libtomcrypt update

* Tue Sep 05 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.6.1-18
- Depend on %%{_bindir}/2to3 instead of python2-tools

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Paul Howarth <paul@city-fan.org> - 2.6.1-15
- BR: python2-tools (for 2to3) rather than plain python-tools

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Paul Howarth <paul@city-fan.org> - 2.6.1-13
- AES.new with invalid parameter crashes python (CVE-2013-7459)
  (https://github.com/dlitz/pycrypto/issues/176)

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.6.1-12
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-11
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Paul Howarth <paul@city-fan.org> - 2.6.1-9
- Enable python3 builds from EPEL-7 (#1110373)
- Modernize spec

* Wed Nov 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 2.6.1-8
- Rebuilt for Python 3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Paul Howarth <paul@city-fan.org> - 2.6.1-4
- Rebuild for python3 3.4 in Rawhide again

* Wed May 14 2014 Paul Howarth <paul@city-fan.org> - 2.6.1-3
- Unbundle libtomcrypt (#1087557)
- Drop %%defattr, redundant since rpm 4.4

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 2.6.1-1
- Update to 2.6.1
  - Fix PRNG not correctly reseeded in some situations (CVE-2013-1445)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Paul Howarth <paul@city-fan.org> - 2.6-1
- Update to 2.6
  - Fix insecure ElGamal key generation (launchpad bug #985164, CVE-2012-2417)
  - Huge documentation cleanup
  - Added more tests, including test vectors from NIST 800-38A
  - Remove broken MODE_PGP, which never actually worked properly
  - A new mode, MODE_OPENPGP, has been added for people wishing to write
    OpenPGP implementations (see also launchpad bug #996814)
  - Fix: getPrime with invalid input causes Python to abort with fatal error
    (launchpad bug #988431)
  - Fix: Segfaults within error-handling paths (launchpad bug #934294)
  - Fix: Block ciphers allow empty string as IV (launchpad bug #997464)
  - Fix DevURandomRNG to work with Python3's new I/O stack
  - Remove automagic dependencies on libgmp and libmpir; let the caller
    disable them using args
  - Many other minor bug fixes and improvements
- Drop upstream patches

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 2.5-2
- Add upstream fixes for issues found by Dave Malcolm's experimental static
  analysis tool (#790584)

* Mon Jan 16 2012 Paul Howarth <paul@city-fan.org> - 2.5-1
- Update to 2.5
  - Added PKCS#1 encryption schemes (v1.5 and OAEP); we now have a decent,
    easy-to-use non-textbook RSA implementation
  - Added PKCS#1 signature schemes (v1.5 and PSS); v1.5 required some
    extensive changes to Hash modules to contain the algorithm-specific ASN.1
    OID, and to that end we now always have a (thin) Python module to hide the
    one in pure C
  - Added 2 standard Key Derivation Functions (PBKDF1 and PBKDF2)
  - Added export/import of RSA keys in OpenSSH and PKCS#8 formats
  - Added password-protected export/import of RSA keys (one old method for
    PKCS#8 PEM only)
  - Added ability to generate RSA key pairs with configurable public
    exponent e
  - Added ability to construct an RSA key pair even if only the private
    exponent d is known, and not p and q
  - Added SHA-2 C source code (fully from Lorenz Quack)
  - Unit tests for all the above
  - Updates to documentation (both inline and in Doc/pycrypt.rst)
  - Minor bug fixes (setup.py and tests)
- Upstream no longer ships python-3-changes.txt

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> - 2.4.1-2
- Rebuild with gcc 4.7

* Mon Nov  7 2011 Paul Howarth <paul@city-fan.org> - 2.4.1-1
- Update to 2.4.1
  - Fix "error: Setup script exited with error: src/config.h: No such file or
    directory" when installing via easy_install

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.4-2.1
- Rebuild with new gmp without compat lib

* Tue Oct 25 2011 Paul Howarth <paul@city-fan.org> - 2.4-2
- Add python3-crypto subpackage (based on patch from Dave Malcolm - #748529)

* Mon Oct 24 2011 Paul Howarth <paul@city-fan.org> - 2.4-1
- Update to 2.4
  - Python 3 support! PyCrypto now supports every version of Python from 2.1
    through to 3.2
  - Timing-attack countermeasures in _fastmath: when built against libgmp
    version 5 or later, we use mpz_powm_sec instead of mpz_powm, which should
    prevent the timing attack described by Geremy Condra at PyCon 2011
  - New hash modules (for Python ≥ 2.5 only): SHA224, SHA384 and SHA512
  - Configuration using GNU autoconf, which should help fix a bunch of build
    issues
  - Support using MPIR as an alternative to GMP
  - Improve the test command in setup.py, by allowing tests to be performed on
    a single sub-package or module only
  - Fix double-decref of "counter" when Cipher object initialization fails
  - Apply patches from Debian's python-crypto 2.3-3 package:
    - fix-RSA-generate-exception.patch
    - epydoc-exclude-introspect.patch
    - no-usr-local.patch
  - Fix launchpad bug #702835: "Import key code is not compatible with GMP
    library"
  - More tests, better documentation, various bugfixes
- Update patch for imposing our own compiler optimization flags
- Drop lib64 patch, no longer needed
- No longer need to fix up permissions and remove shellbangs

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3-5.1
- Rebuild with new gmp

* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 2.3-5
- Upstream rolled new tarball with top-level directory restored
- Nobody else likes macros for commands

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 2.3-3
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-2
- Add "-fno-strict-aliasing" to compilation flags

* Fri Aug 27 2010 Paul Howarth <paul@city-fan.org> - 2.3-1
- Update to 2.3
  - Fix NameError when attempting to use deprecated getRandomNumber() function
  - _slowmath: Compute RSA u parameter when it's not given to RSA.construct;
    this makes _slowmath behave the same as _fastmath in this regard
  - Make RSA.generate raise a more user-friendly exception message when the
    user tries to generate a bogus-length key
- Add -c option to %%setup because upstream tarball has dropped the top-level
  directory
- Run benchmark as part of %%check if we have python 2.4 or later
- BR: python2-devel rather than just python-devel
- Add patch to make sure we can find libgmp in 64-bit multilib environments

* Tue Aug  3 2010 Paul Howarth <paul@city-fan.org> - 2.2-1
- Update to 2.2
  - Deprecated Crypto.Util.number.getRandomNumber()
  - It's been replaced by getRandomNBitInteger and getRandomInteger
  - Better isPrime() and getPrime() implementations
  - getStrongPrime() implementation for generating RSA primes
  - Support for importing and exporting RSA keys in DER and PEM format
  - Fix PyCrypto when floor division (python -Qnew) is enabled
  - When building using gcc, use -std=c99 for compilation
- Update optflags patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 16 2010 Paul Howarth <paul@city-fan.org> - 2.1.0-1
- Update to 2.1.0 (see ChangeLog for details)
- Remove patches (no longer needed)
- Use new upstream URLs
- Upstream has replaced LICENSE with LEGAL/ and COPYRIGHT
- Clarify that license is mostly Public Domain, partly Python
- Add %%check section and run the test suite in it
- Remove upstream's fiddling with compiler optimization flags so we get
  usable debuginfo
- Filter out unwanted provides for python shared objects
- Tidy up egg-info handling
- Simplify %%files list
- Pacify rpmlint as much as is reasonable
- Add dist tag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-17
- Use patches in upstream git to fix #484473

* Fri Feb 13 2009 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-16.1
- add patch to fix #485298 / CVE-2009-0544

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15.1
- Oops, actually apply the patch
- Modify patch so modules remain compatible with PEP 247

* Sat Feb 7 2009 Stewart Adam <s.adam at diffingo.com> - 2.0.1-15
- Add patch to hashlib instead of deprecated md5 and sha modules (#484473)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-14.1
- Rebuild for Python 2.6

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-13
- provide pycrypto

* Sat Feb 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.0.1-12
- rebuilt

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-11
- egg-info file in python_sitearch and not in python_sitelib

* Fri Jan 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-10
- ship egg-file

* Tue Aug 21 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.1-9
- Remove the old and outdated python-abi hack

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Mon Jun 04 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.1-8
- Fix libdir handling so it works on more arches than x86_64

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-7
- Fix typo

* Wed Apr 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-6
- Remove dist
- rebuild, because the older version was much bigger, as it was build when
  distutils was doing static links of libpython

* Sat Dec 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-5
- Rebuild for python 2.5

* Thu Sep 07 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-4
- Don't ghost pyo files (#205408)

* Tue Aug 29 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-3
- Rebuild for Fedora Extras 6

* Mon Feb 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0.1-2
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0.1-1
- Update to 2.0.1
- Use Dist
- Drop python-crypto-64bit-unclean.patch, similar patch was applied
  upstream

* Thu May 05 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-4
- add python-crypto-64bit-unclean.patch (#156173)

* Mon Mar 21 2005 Seth Vidal <skvidal at phy.duke.edu> - 0:2.0-3
- iterate release for build on python 2.4 based systems

* Sat Dec 18 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-2
- Fix build on x86_64: use python_sitearch for files and patch source
  to find gmp

* Thu Aug 26 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:2.0-0.fdr.1
- Update to 2.00

* Fri Aug 13 2004 Ville Skytta <ville.skytta at iki.fi> - 0:1.9-0.fdr.6.a6
- Don't use get_python_version(), it's available in Python >= 2.3 only.

* Thu Aug 12 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.5.a6
- Own dir python_sitearch/Crypto/

* Wed Aug 11 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.4.a6
- Match python spec template more

* Sat Jul 17 2004 Thorsten Leemhuis <fedora at leemhuis dot info> 0:1.9-0.fdr.3.a6
- Own _libdir/python/site-packages/Crypto/

* Wed Mar 24 2004 Panu Matilainen <pmatilai@welho.com> 0.3.2-0.fdr.2.a6
- generate .pyo files during install
- require exact version of python used to build the package
- include more docs + demos
- fix dependency on /usr/local/bin/python
- use fedora.us style buildroot
- buildrequires gmp-devel
- use description from README

* Sun Jan 11 2004 Ryan Boder <icanoop@bitwiser.org>  0.3.2-0.fdr.1.a6
- Initial build.

