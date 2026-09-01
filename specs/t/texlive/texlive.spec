# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Once upon a time, this package had (almost) every component from the TeXLive project living inside of it.
# While it started with the best of intentions, it ended up becoming a truly unmaintainable nightmare.
# With TeXLive 2025, I converted this package into a series of packages, based on the natural
# collection/scheme groupings within TeXLive. This improves things in Fedora in a few ways:
# 1. Updating a component will now only require other components within the same collection to be rebuilt.
#    This is not ideal, but it is way better than before, when _every_ texlive component got rebuilt and
#    sent to Fedora users as updates. This should help some Fedora users get less updates.
# 2. It makes TeXLive much easier to update at major versions.
# 3. It allows for more people to help fix bugs without having to go into the largest known RPM spec file.
#
# I had considered using this also as a "catch-all" for other TeXLive components which people
# are using in Fedora but which were somehow not pulled in as a dependency for a collection/scheme.
# Instead, I think the cleaner approach is to package them individually, unless their numbers explode.
#
# Tom "spot" Callaway, September 18, 2025 <spot@fedoraproject.org>

%global tl_version 2025

Name:           texlive
Epoch:          12
Version:        %{tl_version}
Release:        1%{?dist}
Summary:        Metapackage that provides scheme-basic and collection-latexrecommended
License:        LPPL-1.3c
URL:            http://tug.org/texlive/
BuildArch:      noarch
Requires:       texlive-collection-latexrecommended
Requires:       texlive-scheme-basic
Requires:	texlive-kpathsea

%description
A metapackage to help people get the most useful parts of TeXLive.
Specifically, texlive-scheme-basic and
texlive-collection-latexrecommended. All of the applicable scheme
and collection metapackages exist and you can install them instead
(or in addition).

%prep

%build
# Nothing to build

# This is an easter egg. You have found the rare TeXLive ASCII Frogs.
# They moved in here when everything else moved out.
#               _         _
#   __   ___.--'_`.     .'_`--.___   __
#  ( _`.'. -   'o` )   ( 'o`   - .`.'_ )
#  _\.'_'      _.-'     `-._      `_`./_
# ( \`. )    //\`         '/\\    ( .'/ )
#  \_`-'`---'\\__,       ,__//`---'`-'_/
#   \`        `-\         /-'        '/
#    `                               '   VK

# If you see these magical frogs, and print them out, they will bring
# you good luck. If you show me a print out of these magical frogs
# I will buy you a drink.

%install
# Nothing to install

# Main collection metapackage (empty)
%files

%changelog
* Thu Feb 5 2026 Tom Callaway <spot@fedoraproject.org> - 12:2025-1
- convert to simple metapackage
- thank you for your service, you can rest now.
- lots and lots of old changelogs in the git history, but with the change, they're kinda irrelevant, so I dropped them.
