%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?__python3: %global __python3 /usr/bin/python3}

%global pypi_name dnspython
%global py_package_name dns
%global rctag rc1

Name:           python-%{py_package_name}
Version:        2.1.0
Release:        1%{?dist}
Summary:        DNS toolkit for Python

# The entire package is licensed with both licenses, see LICENSE file
License:        ISC and MIT
URL:            http://www.dnspython.org

#Source0:       https://github.com/rthalley/%{pypi_name}/archive/v%{version}%{rctag}/%{pypi_name}-%{version}%{rctag}.tar.gz
Source0:        https://github.com/rthalley/%{pypi_name}/archive/v%{version}%{rctag}/%{name}-%{version}%{rctag}.tar.gz
# Fix proposed upstream: https://github.com/rthalley/dnspython/issues/610#issuecomment-734704756
Patch0:         0001-fix-resolve-chaining.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cryptography
BuildRequires:  python3-trio
BuildRequires:  python3-curio
BuildRequires:  python3-sniffio
BuildRequires:  python3-requests
BuildRequires:  python3-requests-toolbelt
BuildRequires:  python3-idna
BuildRequires:  python3-pytest

%global _description %{expand:
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic
updates. It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high
level classes perform queries for data of a given name, type, and
class, and return an answer set. The low level classes allow direct
manipulation of DNS zones, messages, names, and records.
}

%description %_description
%package -n python3-%{py_package_name}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{py_package_name}}

%description -n python3-%{py_package_name} %_description

# curio extras cannot be packages because nothing provides python3.9dist(curio) >= 1.2
%{?python_extras_subpkg:%python_extras_subpkg -n python3-dns -i %{python3_sitelib}/*.egg-info dnssec trio doh idna}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}%{rctag}

# strip exec permissions so that we don't pick up dependencies from docs
find examples -type f | xargs chmod a-x

%build
%py3_build

%install
%py3_install

%check
# Skipped test: https://github.com/rthalley/dnspython/issues/590#issuecomment-729644000
%pytest -k "not test_override"

%files -n python3-%{py_package_name}
%license LICENSE
%doc README.md examples
%{python3_sitelib}/%{py_package_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-1
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 2.1.0-0.3.rc1
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Fri Nov 27 2020 Lumír Balhar <lbalhar@redhat.com> - 2.1.0-0.2.rc1
- Fix upstream issue in resolve chaining
* Wed Nov 18 2020 Lumír Balhar <lbalhar@redhat.com> - 2.1.0-0.1.rc1
- Update to 2.1.0-0.1.rc1 (#1893295)
* Thu Jul 30 2020 Lumír Balhar <lbalhar@redhat.com> - 2.0.0-1
- Update to 2.0.0 (#1849341)
- python2-dns moved to its own SRPM
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.16.0-12
- Rebuilt for Python 3.9
* Tue Apr 28 2020 Lumír Balhar <lbalhar@redhat.com> - 1.16.0-11
- Switch crypto backend to python-cryptography
- Related to: rhbz#1819086
* Fri Apr 17 2020 Lumír Balhar <lbalhar@redhat.com> - 1.16.0-10
- Bring python2 subpackage back
- Fix weak dependencies
* Wed Apr 15 2020 Paul Wouters <pwouters@redhat.com> - 1.16.0-9
- Remove python2 and "other_python3" support
- Resolves: rhbz#1802998 Make pycryptodomex and ecdsa weak dependencies of python-dns
- Resolves: rhbz#1801247 python-certbot-dns-rfc2136 fails to build with Python 3.9: base64.decodestring() was removed
* Mon Feb 03 2020 Miro Hrončok <mhroncok@redhat.com> - 1.16.0-8
- Drop build dependency on python2-typing
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Tue Jan 21 2020 Avram Lubkin <aviso@fedoraproject.org> - 1.16.0-6
- Enable unicode patch (rhbz#1731100)
- Fix collections.abc import for Python 3.9 (rhbz#1792919)
* Tue Nov 05 2019 Paul Howarth <paul@city-fan.org> - 1.16.0-5
- Use pycryptodomex instead of pycrypto
- Also use python-ecdsa (except with Python 2)
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.16.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Tue Aug 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.16.0-3
- Reintroduce dropped python2-dns, it is still needed
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.16.0-2
- Rebuilt for Python 3.8
* Sat Jul 27 2019 Avram Lubkin <aviso@fedoraproject.org> - 1.16.0-1
- Latest Release
- Cleanup spec
- Patch to fix unicode escapes
- Drop el6 from master (el6 requires patch for 1.16.0)
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Thu Jul 12 2018 Paul Wouters <pwouters@redhat.com> - 1.15.0-8
- Resolves: rhbz#1600418 - NVR of python-dns is lower in rawhide than in f28
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-7
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.15.0-5
- Cleanup spec file conditionals
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Tue Dec 13 2016 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-2
- Rebuild for Python 3.6
* Tue Oct 04 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.15.0-1
- Latest Release
* Wed Jun 15 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.14.0-1
- Latest Release
* Sun Mar 27 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT99fd864-1
- Latest Snapshot
- Fixed SRPM naming for EPEL7+
* Fri Feb 12 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GITa4774ee-1
- Latest Snapshot
- Drop EPEL5 from master spec
- Patch to support EL6
- Disable python2 package for EPEL7+
* Mon Feb 01 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT465785f-4
- Changed Python2 package name to python2-dns for Fedora 24+
* Fri Jan 22 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.12.0GIT465785f-3
- Using python3_pkgversion to support python34 package in el7
- Build Python3 package for el7+
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0GIT465785f-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Fri Sep 11 2015 Petr Spacek <pspacek@redhat.com> - 1.12.0GIT465785f
- Rebase to GIT snapshots 465785f85f87508209117264c677080e901e957c (Python 2)
  and 1b0c15086f0e5f6eacc06d77a119280c31731b3c (Python 3)
  to pull in latest fixes
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
* Tue Feb 18 2014 Paul Wouters <pwouters@redhat.com> - 1.11.1-2
- Added LOC and ECDSA fixes from git (rhbz#1059594)
* Thu Sep  5 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.1-1
- New since 1.11.0:
-
-         Nothing
-
- Bugs fixed since 1.11.1:
-
-         dns.resolver.Resolver erroneously referred to 'retry_servfail'
-         instead of 'self.retry_servfail'.
-
-         dns.tsigkeyring.to_text() would fail trying to convert the
-         keyname to text.
-
-         Multi-message TSIGs were broken for algorithms other than
-         HMAC-MD5 because we weren't passing the right digest module to
-         the HMAC code.
-
-         dns.dnssec._find_candidate_keys() tried to extract the key
-         from the wrong variable name.
-
-         $GENERATE tests were not backward compatible with python 2.4.
-
-         APL RR trailing zero suppression didn't work due to insufficient
-         python 3 porting.   [dnspython3 only]

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Sun Jul  7 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.0-2
- Integrate Python 2.6 packaging, EPEL5, EPEL6 support
* Sun Jul  7 2013 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.11.0-1
- New since 1.10.0:
-
-         $GENERATE support
-
-         TLSA RR support
-
-         Added set_flags() method to dns.resolver.Resolver
-
- Bugs fixed since 1.10.0:
-
-         Names with offsets >= 2^14 are no longer added to the
-         compression table.
-
-         The "::" syntax is not used to shorten a single 16-bit section
-         of the text form an IPv6 address.
-
-         Caches are now locked.
-
-         YXDOMAIN is raised if seen by the resolver.
-
-         Empty rdatasets are not printed.
-
-         DNSKEY key tags are no longer assumed to be unique.
* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1.10.0-3
- add python3-dns subpackage (rhbz#911933)
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Mon Sep 17 2012 Paul Wouters <pwouters@redhat.com> - 1.10.0-1
- Updated to 1.10.0
- Patch to support TLSA RRtype
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Mon Mar 28 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.4-1
-
- dnspython 1.9.4 has been released and is available at
- http://www.dnspython.org/kits/1.9.4/
-
- There is no new functionality in this release; just a few bug fixes
- in RRSIG and SIG code.
-
- I will be eliminating legacy code for earlier versions of DNSSEC in a
- future release of dnspython.
* Fri Mar 25 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.3-1
-
- New since 1.9.2:
-
-     A boolean parameter, 'raise_on_no_answer', has been added to
- the query() methods.  In no-error, no-data situations, this
- parameter determines whether NoAnswer should be raised or not.
- If True, NoAnswer is raised.  If False, then an Answer()
- object with a None rrset will be returned.
-
- Resolver Answer() objects now have a canonical_name field.
-
- Rdata now have a __hash__ method.
-
- Bugs fixed since 1.9.2:
-
-        Dnspython was erroneously doing case-insensitive comparisons
- of the names in NSEC and RRSIG RRs.
-
- We now use "is" and not "==" when testing what section an RR
- is in.
-
- The resolver now disallows metaqueries.
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
* Thu Dec  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.2-2
- Build Python 2.6 subpackage for EPEL 5
* Tue Nov 23 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.2-1
- It's brown paper bag time :) The fix for the import problems was
- actually bad, but didn't show up in testing because the test suite's
- conditional importing code hid the problem.
-
- Any, 1.9.2 is out.
-
- Sorry for the churn!
* Mon Nov 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.9.1-1
- New since 1.9.0:
-
-        Nothing.
-
- Bugs fixed since 1.9.0
-
-        The dns.dnssec module didn't work with DSA due to namespace
-        contamination from a "from"-style import.
-
- New since 1.8.0:
-
-        dnspython now uses poll() instead of select() when available.
-
-        Basic DNSSEC validation can be done using dns.dnsec.validate()
-        and dns.dnssec.validate_rrsig() if you have PyCrypto 2.3 or
-        later installed.  Complete secure resolution is not yet
-        available.
-
-        Added key_id() to the DNSSEC module, which computes the DNSSEC
-        key id of a DNSKEY rdata.
-
-        Added make_ds() to the DNSSEC module, which returns the DS RR
-        for a given DNSKEY rdata.
-
-        dnspython now raises an exception if HMAC-SHA284 or
-        HMAC-SHA512 are used with a Python older than 2.5.2.  (Older
-        Pythons do not compute the correct value.)
-
-        Symbolic constants are now available for TSIG algorithm names.
-
- Bugs fixed since 1.8.0
-
-        dns.resolver.zone_for_name() didn't handle a query response
-        with a CNAME or DNAME correctly in some cases.
-
-        When specifying rdata types and classes as text, Unicode
-        strings may now be used.
-
-        Hashlib compatibility issues have been fixed.
-
-        dns.message now imports dns.edns.
-
-        The TSIG algorithm value was passed incorrectly to use_tsig()
-        in some cases.

* Fri Aug 13 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-3
- Add a patch from upstream to fix a Python 2.7 issue.
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.8.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild
* Wed Jan 27 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-1.1
- Fix error
* Wed Jan 27 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.8.0-1
- New since 1.7.1:
-
-  Support for hmac-sha1, hmac-sha224, hmac-sha256, hmac-sha384 and
-  hmac-sha512 has been contributed by Kevin Chen.
-
-  The tokenizer's tokens are now Token objects instead of (type,
-  value) tuples.
-
- Bugs fixed since 1.7.1:
-
-  Escapes in masterfiles now work correctly.  Previously they were
-  only working correctly when the text involved was part of a domain
-  name.
-
-  When constructing a DDNS update, if the present() method was used
-  with a single rdata, a zero TTL was not added.
-
-  The entropy pool needed locking to be thread safe.
-
-  The entropy pool's reading of /dev/random could cause dnspython to
-  block.
-
-  The entropy pool did buffered reads, potentially consuming more
-  randomness than we needed.
-
-  The entropy pool did not seed with high quality randomness on
-  Windows.
-
-  SRV records were compared incorrectly.
-
-  In the e164 query function, the resolver parameter was not used.
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Fri Jun 19 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- New since 1.7.0:
-
-        Nothing
-
- Bugs fixed since 1.7.0:
-
-        The 1.7.0 kitting process inadventently omitted the code for the
-        DLV RR.
-
-        Negative DDNS prerequisites are now handled correctly.
* Fri Jun 19 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.0-1
- New since 1.6.0:
-
-        Rdatas now have a to_digestable() method, which returns the
-        DNSSEC canonical form of the rdata, suitable for use in
-        signature computations.
-
-        The NSEC3, NSEC3PARAM, DLV, and HIP RR types are now supported.
-
-        An entropy module has been added and is used to randomize query ids.
-
-        EDNS0 options are now supported.
-
-        UDP IXFR is now supported.
-
-        The wire format parser now has a 'one_rr_per_rrset' mode, which
-        suppresses the usual coalescing of all RRs of a given type into a
-        single RRset.
-
-        Various helpful DNSSEC-related constants are now defined.
-
-        The resolver's query() method now has an optional 'source' parameter,
-        allowing the source IP address to be specified.
-
- Bugs fixed since 1.6.0:
-
-        On Windows, the resolver set the domain incorrectly.
-
-        DS RR parsing only allowed one Base64 chunk.
-
-        TSIG validation didn't always use absolute names.
-
-        NSEC.to_text() only printed the last window.
-
-        We did not canonicalize IPv6 addresses before comparing them; we
-        would thus treat equivalent but different textual forms, e.g.
-        "1:00::1" and "1::1" as being non-equivalent.
-
-        If the peer set a TSIG error, we didn't raise an exception.
-
-        Some EDNS bugs in the message code have been fixed (see the ChangeLog
-        for details).
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Sat Nov 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-3
- Rebuild for Python 2.6
* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-2
- fix license tag
* Tue Dec  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-1
- Update to 1.6.0
* Tue Oct  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-2
- Follow new Python egg packaging specs
* Thu Jan 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-1
- Update to 1.5.0
* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-3
- Bump release for rebuild with Python 2.5
* Mon Aug 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-2
- No longer ghost *.pyo files, thus further simplifying the files section.
* Sat Aug  5 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-1
- Update to 1.4.0
- Remove unneeded python-abi requires
- Remove unneeded python_sitearch macro
* Fri May 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.5-1
- First version for Fedora Extras