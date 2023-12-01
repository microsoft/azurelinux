Summary:        A Python interface to libcurl
Name:           python-pycurl
Version:        7.43.0.2
Release:        10%{?dist}
License:        LGPLv2+ OR MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            http://pycurl.sourceforge.net/
Source0:        https://pypi.io/packages/source/p/pycurl/pycurl-%{version}.tar.gz
Patch0:         skip-incompatible-libcurl-tests.patch

%description
A Python interface to libcurl

%package -n     python3-pycurl
Summary:        A Python interface to libcurl
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
Requires:       curl
Requires:       python3
%if %{with_check}
BuildRequires:  curl-libs
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  vsftpd
%endif

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package doc
Summary:        Documentation and examples for pycurl
Requires:       python3-pycurl = %{version}-%{release}

%description doc
Documentation and examples for pycurl

%prep
%autosetup -p 1 -n pycurl-%{version}
rm -f doc/*.xml_validity
#chmod a-x examples/*

# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so

%build
CFLAGS="%{optflags} -DHAVE_CURL_OPENSSL" %{py3_build "--with-ssl"}

%install
%{py3_install "--with-ssl"}
rm -rf %{buildroot}%{_docdir}/pycurl
chmod 755 %{buildroot}%{python3_sitelib}/pycurl*.so

%check
export PYCURL_SSL_LIBRARY=openssl
export PYCURL_VSFTPD_PATH=vsftpd

pip3 install nose nose-show-skipped bottle==0.12.16 flaky pyflakes
rm -vf tests/multi_option_constants_test.py tests/ftp_test.py tests/option_constants_test.py tests/seek_cb_test.py tests/memory_mgmt_test.py tests/multi_timer_test.py
LANG=en_US.UTF-8  make test PYTHON=python%{python3_version} NOSETESTS="nosetests-3.4 -v"

%files -n python3-pycurl
%defattr(-,root,root,-)
%license COPYING-MIT COPYING-LGPL
%{python3_sitelib}/*

%files doc
%defattr(-,root,root)
%doc RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.43.0.2-10
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.43.0.2-9
- Add licenses to python3 package, remove from docs package
- Remove python2 package
- Lint spec

* Wed Jun 16 2021 Andrew Phelps <anphel@microsoft.com> 7.43.0.2-8
- Add patch to fix libcurl package test issue 
- (JOSLOBO: 7/26/21 Bumped dash verison due to merge conflict)

* Mon May 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 7.43.0.2-7
- Update source URL

* Wed Mar 03 2021 Andrew Phelps <anphel@microsoft.com> 7.43.0.2-6
- Disable unreliable multi_timer_test

* Wed Jan 20 2021 Andrew Phelps <anphel@microsoft.com> 7.43.0.2-5
- Disable unreliable memory_mgmt_test

* Fri Jan 15 2021 Andrew Phelps <anphel@microsoft.com> 7.43.0.2-4
- Fix check tests by setting PYCURL_SSL_LIBRARY and using specific bottle version.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 7.43.0.2-3
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 7.43.0.2-2
- Renaming pycurl to python-pycurl

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 7.43.0.2-1
- Update to version 7.43.0.2. License verified. Remove fixed patch.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.43.0-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> 7.43.0-4
- Fixed the make check.

* Mon Aug 14 2017 Chang Lee <changlee@vmware.com> 7.43.0-3
- Added check requires and fixed check

* Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.43.0-2
- Using python2 explicitly while building

* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 7.43.0-1
- Upgrade to 7.43.0  and add pycurl3

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.21.5-5
- BuildRequires curl-devel.

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 7.21.5-4
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
- GA - Bump release of all rpms

* Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
- Removing prebuilt binaries

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
- Upgrade version

* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
- Added Doc subpackage. Removed chmod a-x for examples.

* Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
- Initial build.  First version
