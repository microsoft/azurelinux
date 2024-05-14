Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global gem_name rouge

Name:           rubygem-%{gem_name}
Version:        3.26.0
Release:        3%{?dist}
Summary:        Pure-ruby colorizer based on pygments
License:        MIT and BSD
URL:            https://rouge.jneen.net/
Source0:        https://github.com/rouge-ruby/rouge/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.0
BuildRequires:  help2man
BuildArch:      noarch

%description
Rouge aims to a be a simple, easy-to-extend drop-in replacement for pygments.

%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Generate man page from "rougify --help" output
export GEM_PATH="%{buildroot}%{gem_dir}:%{gem_dir}"

mkdir -p %{buildroot}%{_mandir}/man1

help2man -N -s1 -o %{buildroot}%{_mandir}/man1/rougify.1 \
    %{buildroot}%{_bindir}/rougify

%files
%license %{gem_instdir}/LICENSE
%{_bindir}/rougify
%{_mandir}/man1/rougify.1*
%dir %{gem_instdir}
%{gem_instdir}/bin
%exclude %{gem_instdir}/rouge.gemspec
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.26.0-3
- License verified.
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.26.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Dec 11 2020 Fabio Valentini <decathorpe@gmail.com> - 3.26.0-1
- Update to version 3.26.0.

* Wed Nov 18 2020 Fabio Valentini <decathorpe@gmail.com> - 3.25.0-1
- Update to version 3.25.0.

* Fri Oct 16 2020 Fabio Valentini <decathorpe@gmail.com> - 3.24.0-1
- Update to version 3.24.0.

* Wed Sep 09 2020 Fabio Valentini <decathorpe@gmail.com> - 3.23.0-1
- Update to version 3.23.0.

* Wed Aug 12 2020 Fabio Valentini <decathorpe@gmail.com> - 3.22.0-1
- Update to version 3.22.0.

* Wed Jul 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.21.0-1
- Update to version 3.21.0.

* Fri Jun 12 2020 Fabio Valentini <decathorpe@gmail.com> - 3.20.0-1
- Update to version 3.20.0.

* Fri May 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.19.0-1
- Update to version 3.19.0.

* Sat Apr 18 2020 Fabio Valentini <decathorpe@gmail.com> - 3.18.0-1
- Update to version 3.18.0.

* Wed Mar 11 2020 Fabio Valentini <decathorpe@gmail.com> - 3.17.0-1
- Update to version 3.17.0.

* Sat Feb 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.16.0-1
- Update to version 3.16.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Fabio Valentini <decathorpe@gmail.com> - 3.15.0-1
- Update to version 3.15.0.

* Thu Dec 19 2019 Fabio Valentini <decathorpe@gmail.com> - 3.14.0-1
- Update to version 3.14.0.

* Sat Nov 16 2019 Fabio Valentini <decathorpe@gmail.com> - 3.13.0-1
- Update to version 3.13.0.

* Wed Oct 30 2019 Fabio Valentini <decathorpe@gmail.com> - 3.12.0-1
- Update to version 3.12.0.

* Mon Oct 07 2019 Fabio Valentini <decathorpe@gmail.com> - 3.11.1-1
- Update to version 3.11.1.

* Sat Sep 28 2019 Fabio Valentini <decathorpe@gmail.com> - 3.11.0-1
- Update to version 3.11.0.

* Wed Sep 04 2019 Fabio Valentini <decathorpe@gmail.com> - 3.10.0-1
- Update to version 3.10.0.

* Thu Aug 15 2019 Fabio Valentini <decathorpe@gmail.com> - 3.8.0-1
- Update to version 3.8.0.

* Tue Jul 30 2019 Fabio Valentini <decathorpe@gmail.com> - 3.7.0-1
- Update to version 3.7.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Fabio Valentini <decathorpe@gmail.com> - 3.6.0-1
- Update to version 3.6.0.

* Tue Jul 02 2019 Fabio Valentini <decathorpe@gmail.com> - 3.5.1-1
- Update to version 3.5.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 02 2018 Fabio Valentini <decathorpe@gmail.com> - 3.3.0-1
- Update to version 3.3.0.

* Fri Aug 17 2018 Fabio Valentini <decathorpe@gmail.com> - 3.2.1-1
- Update to version 3.2.1.

* Thu Aug 02 2018 Fabio Valentini <decathorpe@gmail.com> - 3.2.0-1
- Update to version 3.2.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Fabio Valentini <decathorpe@gmail.com> - 3.1.1-1
- Update to version 3.1.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 23 2016 Björn Esser <fedora@besser82.io> - 1.11.1-1
- initial import (#1368850)

* Sun Aug 21 2016 Björn Esser <fedora@besser82.io> - 1.11.1-0.1
- initial rpm-release (#1368850)

