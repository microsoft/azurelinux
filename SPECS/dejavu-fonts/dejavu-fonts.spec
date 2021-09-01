%define _fontdir %{_datadir}/fonts
%define _fontconfig_dir %{_datadir}/fontconfig/conf.avail/
%define _fontconfig_links_dir %{_sysconfdir}/fonts/conf.d
%define _mono_fontdir %{_fontdir}/dejavu-sans-mono-fonts
%define _sans_fontdir %{_fontdir}/dejavu-sans-fonts
%define _serif_fontdir %{_fontdir}/dejavu-serif-fonts

Summary:        The DejaVu fonts families
Name:           dejavu-fonts
Version:        2.37
Release:        2%{?dist}
License:        Bistream Vera Font AND Arev Fonts
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://dejavu-fonts.github.io/
Source0:        https://sourceforge.net/projects/dejavu/files/dejavu/%{version}/%{name}-ttf-%{version}.tar.bz2

BuildRequires:  tar

%description
The DejaVu fonts are a font family based on the Vera Fonts.
Its purpose is to provide a wider range of characters while maintaining
the original look and feel through the process of collaborative development

%package -n dejavu-sans-fonts
Summary:        DejaVu Sans fonts family. Variable-width, sans-serif.

# Last time package was called 'dejavu-sans' was for the 2.37-1 version.
Obsoletes:      dejavu-sans < 2.37-2
Provides:       dejavu-sans = %{version}-%{release}

%description -n dejavu-sans-fonts
%{summary}

%package -n dejavu-sans-mono-fonts
Summary:        DejaVu Sans Mono fonts family. Monospaced, sans-serif.

%description -n dejavu-sans-mono-fonts
%{summary}

%package -n dejavu-serif-fonts
Summary:        DejaVu Serif fonts family. Variable-width, serif.

%description -n dejavu-serif-fonts
%{summary}

%prep
%setup -q -n %{name}-ttf-%{version}

%install
install -d %{buildroot}%{_fontconfig_dir}/
install -d %{buildroot}%{_fontconfig_links_dir}

install fontconfig/*.conf %{buildroot}%{_fontconfig_dir}
for fontconfig in fontconfig/*.conf
do
    ln -s %{_fontconfig_dir}/$(basename $fontconfig) %{buildroot}%{_fontconfig_links_dir}
done

# Sans fonts
install -d %{buildroot}%{_sans_fontdir}
install ttf/*Sans.ttf %{buildroot}%{_sans_fontdir}
install ttf/*Sans-*.ttf %{buildroot}%{_sans_fontdir}
install ttf/*SansCondensed*.ttf %{buildroot}%{_sans_fontdir}

# Sans Mono fonts
install -d %{buildroot}%{_mono_fontdir}
install ttf/*Mono*.ttf %{buildroot}%{_mono_fontdir}

# Sans Serif fonts
install -d %{buildroot}%{_serif_fontdir}
install ttf/*Serif*.ttf %{buildroot}%{_serif_fontdir}
install ttf/DejaVuMathTeXGyre.ttf %{buildroot}%{_serif_fontdir}

%files -n dejavu-sans-fonts
%defattr(-,root,root)
%license LICENSE
%doc AUTHORS BUGS NEWS README.md
%dir %{_sans_fontdir}
%{_fontconfig_dir}/*sans.conf
%{_fontconfig_links_dir}/*sans.conf
%{_sans_fontdir}/*.ttf

%files -n dejavu-sans-mono-fonts
%defattr(-,root,root)
%license LICENSE
%doc AUTHORS BUGS NEWS README.md
%dir %{_mono_fontdir}
%{_fontconfig_dir}/*mono.conf
%{_fontconfig_links_dir}/*mono.conf
%{_mono_fontdir}/*.ttf

%files -n dejavu-serif-fonts
%defattr(-,root,root)
%license LICENSE
%doc AUTHORS BUGS NEWS README.md
%dir %{_serif_fontdir}
%{_fontconfig_dir}/*serif.conf
%{_fontconfig_links_dir}/*serif.conf
%{_serif_fontdir}/*.ttf

%changelog
* Fri Jul 09 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.37-2
- Renaming to 'dejavu-fonts'.
- Adding 'dejavu-sans-mono-fonts' and 'dejavu-serif-fonts' subpackages.
- Adding font configurations.

* Fri May 21 2021 Jon Slobodzian <joslobo@microsoft.com> 2.37-1
- Original version for CBL-Mariner.
