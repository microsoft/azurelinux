# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		libfastjson
Version:	1.2304.0
Release:	7%{?dist}
Summary:	A JSON implementation in C
License:	MIT
URL:		https://github.com/rsyslog/libfastjson
Source0:	http://download.rsyslog.com/libfastjson/libfastjson-%{version}.tar.gz

BuildRequires: autoconf automake libtool
BuildRequires: make

%description
LIBFASTJSON implements a reference counting object
model that allows you to easily construct JSON
objects in C, output them as JSON formatted strings
and parse JSON formatted strings back into the
C representation of JSON objects.

%package	devel
Summary:	Development files for libfastjson
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
This package contains libraries and header files for
developing applications that use libfastjson.

%prep
%setup -q

for doc in ChangeLog; do
 iconv -f iso-8859-1 -t utf8 $doc > $doc.new &&
 touch -r $doc $doc.new &&
 mv $doc.new $doc
done

%build
autoreconf -iv
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" # temporary workaround for EPEL5, fixed upstream
%configure --enable-shared --disable-static

%install
make V=1 DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete -print

%check
make V=1 check

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog README.html
%{_libdir}/libfastjson.so.*

%files devel
%{_includedir}/libfastjson
%{_libdir}/libfastjson.so
%{_libdir}/pkgconfig/libfastjson.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2304.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 16 2023 Attila Lakatos <alakatos@redhat.com> - 1.2304.0-1
- Rebase to 1.2304.0 (new release number scheme, now like rsyslog)
Resolves: rhbz#2183193
- Address CVE-2020-12762
Resolves: rhbz#2203170

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 08 2021 Attila Lakatos <alakatos@redhat.com> - 0.99.9-1
- rebase to v0.99.9
Resolves: rhbz#1920145

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Jiri Vymazal <jvymazal@redhat.com> - 0.99.8-1
- rebase to v0.99.8

* Mon Oct 23 2017 Radovan Sroka <rsroka@redhat.com> - 0.99.7-1
- rebase to v0.99.7

* Tue Aug 15 2017 Marek Tamaskovic <mtamasko@redhat.com> - 0.99.6-1
- rebase to v0.99.6

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Radovan Sroka <rsroka@redhat.com> - 0.99.5-1
- added autoreconf
- rebase to v0.99.5

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 27 2016 Radovan Sroka <rsroka@redhat.com> - 0.99.4-1
- Package created
