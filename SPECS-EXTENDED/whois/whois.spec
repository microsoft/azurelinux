# Package mkpasswd tool
%{bcond_without whois_enables_mkpasswd}
# Enable IDN, use libidn2 instead of libidn
%{bcond_without whois_enables_libidn2}
# Add libidn support
%{bcond_with    whois_enables_idn}

%global forgeurl https://github.com/rfc1036/whois
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:       whois       
Version:    5.5.20
Release:    1%{?dist}
Summary:    Improved WHOIS client
License:    GPL-2.0-or-later
URL:        https://www.linux.it/~md/software/
VCS:        git:%{forgeurl}
Source0:    https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.tar.xz
Source1:    https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.dsc
# This keyring needs to be processed at prep time, dscverify is not able to use it as it is
Source2:    https://www.linux.it/~md/md-pgp.asc
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext
%if %{with whois_enables_libidn2}
BuildRequires:  pkgconfig(libidn2) >= 2.0.3
%elif %{with whois_enables_idn}
BuildRequires:  pkgconfig(libidn)
BuildConflicts: pkgconfig(libidn2)
%else
BuildConflicts: pkgconfig(libidn)
BuildConflicts: pkgconfig(libidn2)
%endif
%if %{with whois_enables_mkpasswd}
BuildRequires:  pkgconfig(libxcrypt) >= 4.1
%endif
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl(autodie)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%if 0%{?fedora}
# Extra source verification. devscripts are not in rhel
BuildRequires:  devscripts
BuildRequires:  gnupg2
%endif
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires:   whois-nls = %{version}-%{release}

%global genname whois
%global alternative md
%global cfgfile %{name}.conf

%description
Searches for an object in a RFC 3912 database.

This version of the WHOIS client tries to guess the right server to ask for
the specified object. If no guess can be made it will connect to
whois.networksolutions.com for NIC handles or whois.arin.net for IPv4
addresses and network names.

%if %{with whois_enables_mkpasswd}
%package -n mkpasswd
Summary:    Encrypt a password with crypt(3) function using a salt
# /usr/bin/mkpasswd was provided by "expect" package, bug #1649426
Conflicts:  expect < 5.45.4-8.fc30
Requires:   whois-nls = %{version}-%{release}
# whois-mkpasswd package renamed to mkpasswd in 5.4.0-2.fc30, bug #1649426
Obsoletes:  whois-mkpasswd <= 5.4.0-1.fc30
# but we continued upgrading whois in Fedoras < 30 without the rename
Obsoletes:  whois-mkpasswd <= 5.5.3-1.fc29
Provides:   whois-mkpasswd = %{version}-%{release}

%description -n mkpasswd
mkpasswd tool encrypts a given password with the crypt(3) libc function
using a given salt.
%endif

# The same gettext catalogs are used by whois tool and mkpasswd tool. But we
# want to have the tools installable independently.
%package nls
Summary:    Gettext catalogs for whois tools
Conflicts:  whois < 5.3.2-2
BuildArch:  noarch

%description nls
whois tools messages translated into different natural languages.

%prep
%if 0%{?fedora}
  export GNUPGHOME="$(mktemp --tmpdir -d %{name}-XXXXXXX)"
  TMPKEY="$GNUPGHOME/keyring.key"
  gpg --no-default-keyring --keyring "${TMPKEY}" --trust-model always --import %{SOURCE2}
  dscverify --keyring "${TMPKEY}" %{SOURCE1}
  rm -rf "$GNUPGHOME"
%endif
%autosetup -p1 -n %{name}

%build
%{make_build} CONFIG_FILE="%{_sysconfdir}/%{cfgfile}" \
    HAVE_ICONV=1 \
    CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="%{__global_ldflags}" INSTALL="install -p"

%install
%if %{with whois_enables_mkpasswd}
make install-mkpasswd install-pos BASEDIR=$RPM_BUILD_ROOT
%endif
make install-whois install-pos BASEDIR=$RPM_BUILD_ROOT
install -p -m644 -D %{cfgfile} $RPM_BUILD_ROOT%{_sysconfdir}/%{cfgfile}
%find_lang %{name}

# Rename to alternative names
mv $RPM_BUILD_ROOT%{_bindir}/%{name}{,.%{alternative}}
touch $RPM_BUILD_ROOT%{_bindir}/%{name}
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}
mv $RPM_BUILD_ROOT%{_mandir}/man1/%{name}{,.%{alternative}}.1
touch $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

%post
%{_sbindir}/update-alternatives \
    --install %{_bindir}/%{name} \
        %{genname} %{_bindir}/%{name}.%{alternative} 30 \
    --slave %{_mandir}/man1/%{name}.1.gz \
        %{genname}-man %{_mandir}/man1/%{name}.%{alternative}.1.gz 

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove \
        %{genname} %{_bindir}/%{name}.%{alternative}
fi

%files
%license COPYING debian/copyright
%doc README debian/changelog
%config(noreplace) %{_sysconfdir}/%{cfgfile}
%{_bindir}/%{name}.%{alternative}
%ghost %{_bindir}/%{name}
%{_mandir}/man1/%{name}.%{alternative}.*
%ghost %{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{cfgfile}.5.*

%files nls -f %{name}.lang

%if %{with whois_enables_mkpasswd}
%files -n mkpasswd
%license COPYING debian/copyright
%doc README
%{_bindir}/mkpasswd
%{_mandir}/man1/mkpasswd.*
%endif

%changelog
* Tue Mar 18 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 5.5.20-1
- Initial AzureLinux import from Fedora 41 .
- License verified
