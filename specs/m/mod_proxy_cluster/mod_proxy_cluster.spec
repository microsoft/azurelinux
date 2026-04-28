# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#no jars in this native build, so skip signing
%define _jarsign_opts --nocopy

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag} 
%global selinuxtype targeted
%define aplibdir %{_libdir}/httpd/modules/
 
%define serial 1
 
Name:          mod_proxy_cluster
Summary:       JBoss mod_proxy_cluster for Apache httpd
Version:       1.3.22
Release:       %{serial}%{?dist}.1
License:       LGPL-3.0-only
URL:           https://github.com/modcluster/mod_cluster
Source0:       https://github.com/modcluster/mod_cluster/archive/%{namedversion}/mod_cluster-%{namedversion}.tar.gz
Source1:       %{name}.conf.sample
Source2:       %{name}.te
Source3:       %{name}.fc
 
# 64 bit natives only
ExcludeArch:      i686 i386
 
BuildRequires:    httpd-devel
BuildRequires:    apr-devel
BuildRequires:    apr-util-devel
BuildRequires:    autoconf
BuildRequires:    gcc
 
Requires:         (%{name}-selinux if selinux-policy-%{selinuxtype})
 
Requires:         httpd >= 0:2.4.49
Requires:         apr
Requires:         apr-util
 
# SELinux subpackage
%package selinux
Summary:             mod_proxy_cluster SELinux policy
BuildArch:           noarch
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
BuildRequires:       selinux-policy-devel
%{?selinux_requires}
 
%description selinux
mod_proxy_cluster SELinux policy module
 
%description
JBoss mod_proxy_cluster for Apache httpd.
 
%prep
%autosetup -n mod_cluster-%{namedversion}
 
%build
pushd native
for i in advertise mod_manager mod_proxy_cluster mod_cluster_slotmem
do
pushd $i
set -e
sh buildconf
export CFLAGS='%{optflags} -fno-strict-aliasing -DMOD_CLUSTER_RELEASE_VERSION="-%{serial}"'
%configure --with-apxs=/usr/bin/apxs
%make_build
popd
done
popd
 
# for SELinux
mkdir selinux
cp -p %{SOURCE2} selinux/
cp -p %{SOURCE3} selinux/
 
make -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 %{name}.pp
 
%install
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -d -m 755 $RPM_BUILD_ROOT/%{aplibdir}/
cp -p native/*/*.so ${RPM_BUILD_ROOT}/%{aplibdir}/
install -d -m 755 $RPM_BUILD_ROOT/%{_localstatedir}/cache/httpd/mod_proxy_cluster

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -p -m 644 %{SOURCE1} \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/mod_proxy_cluster.conf.sample
 
install -D -m 0644 %{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
 
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}
 
%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
 
%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
fi
 
%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}
 
%post
# first install
if [ $1 -eq 1 ]; then
    %{_sbindir}/semanage port -a -t http_port_t -p udp 23364 || true
    %{_sbindir}/semanage port -a -t http_port_t -p tcp 6666 || true
fi
 
%postun
# Delete port labeling when the package is removed
if [ $1 -eq 0 ]; then
    %{_sbindir}/semanage port -d -t http_port_t -p udp 23364 || true
    %{_sbindir}/semanage port -d -t http_port_t -p tcp 6666 || true
fi
 
%files
%license lgpl.txt
%dir %{_localstatedir}/cache/httpd/mod_proxy_cluster
%attr(0755,root,root) %{aplibdir}/*
%{_sysconfdir}/httpd/conf.d/mod_proxy_cluster.conf.sample
 
%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.*
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.22-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 18 2025 Vladimir Chlup <vchlup@redhat.com> - 1.3.22-1
- Update to upstream 1.3.22.Final release

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.21-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 8 2025 Vladimir Chlup <vchlup@redhat.com> - 1.3.21-1
- Update to upstream 1.3.21.Final release

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.20-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 12 2024 Vladimir Chlup <vchlup@redhat.com> - 1.3.20-1
- Update to upstream 1.3.20.Final release

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.19-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Hui Wang <huwang@redhat.com> - 1.3.19-1
- First build
