%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Name:           python-pycurl
Version:        7.43.0.2
Release:        4%{?dist}
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://dl.bintray.com/pycurl/pycurl/pycurl-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  curl-devel

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires: python-setuptools, vsftpd, curl-libs
BuildRequires: python3-setuptools, python3-xml
%endif

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package -n     python2-pycurl
Summary:        python2-pycurl
Requires:       python2
Requires:       python2-libs
Requires:       curl
Provides:       pycurl = %{version}-%{release}

%description -n python2-pycurl
Python 2 version.

%package -n     python3-pycurl
Summary:        python3 pycurl
Requires:       python3
Requires:       python3-libs
Requires:       curl

%description -n python3-pycurl
Python 3 version.

%package doc
Summary:    Documentation and examples for pycurl
Requires:   python2-pycurl = %{version}

%description doc
Documentation and examples for pycurl

%prep
%setup -q -n pycurl-%{version}
rm -f doc/*.xml_validity
#chmod a-x examples/*

# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python2 setup.py build --with-ssl
pushd ../p3dir
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python3 setup.py build --with-ssl
popd

%install
rm -rf %{buildroot}
python2 setup.py install -O1 --skip-build --root %{buildroot} --with-ssl
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python2_sitelib}/pycurl*.so
pushd ../p3dir
python3 setup.py install -O1 --skip-build --root %{buildroot} --with-ssl
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python3_sitelib}/pycurl*.so
popd


%check
export PYCURL_SSL_LIBRARY=openssl
export PYCURL_VSFTPD_PATH=vsftpd

easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose nose-show-skipped bottle flaky pyflakes
rm -f tests/multi_option_constants_test.py tests/ftp_test.py tests/option_constants_test.py tests/seek_cb_test.py
LANG=en_US.UTF-8  make test PYTHON=python%{python2_version} NOSETESTS="nosetests-%{python2_version} -v"

cd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose nose-show-skipped bottle==0.12.16 flaky pyflakes
rm -f tests/multi_option_constants_test.py tests/ftp_test.py tests/option_constants_test.py tests/seek_cb_test.py
LANG=en_US.UTF-8  make test PYTHON=python%{python3_version} NOSETESTS="nosetests-3.4 -v"

%clean
rm -rf %{buildroot}

%files -n python2-pycurl
%defattr(-,root,root,-)
%license COPYING-MIT
%{python2_sitelib}/*

%files -n python3-pycurl
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files doc
%defattr(-,root,root)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
*   Fri Jan 15 2021 Andrew Phelps <anphel@microsoft.com> 7.43.0.2-4
-   Fix check tests by setting PYCURL_SSL_LIBRARY and using specific bottle version.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 7.43.0.2-3
-   Added %%license line automatically
*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 7.43.0.2-2
-   Renaming pycurl to python-pycurl
*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 7.43.0.2-1
-   Update to version 7.43.0.2. License verified. Remove fixed patch.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.43.0-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> 7.43.0-4
-   Fixed the make check.
*   Mon Aug 14 2017 Chang Lee <changlee@vmware.com> 7.43.0-3
-   Added check requires and fixed check
*   Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.43.0-2
-   Using python2 explicitly while building
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 7.43.0-1
-   Upgrade to 7.43.0  and add pycurl3
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.21.5-5
-   BuildRequires curl-devel.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 7.21.5-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
-   GA - Bump release of all rpms
*   Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
-   Removing prebuilt binaries
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
-   Upgrade version
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
-   Added Doc subpackage. Removed chmod a-x for examples.
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-   Initial build.  First version
