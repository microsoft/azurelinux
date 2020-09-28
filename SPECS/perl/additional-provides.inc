# Mariner perl.spec provides mostly the same modules as Fedora's version. This file lists additional subpackage and explicit provides to meet Fedora spec's build requirements

# version and compat versions provided by perl-libs
Provides: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides: perl(:MODULE_COMPAT_5.30.0)
Provides: perl(:MODULE_COMPAT_5.30.1)
Provides: perl(:MODULE_COMPAT_5.30.2)
Provides: perl(:VERSION) = 5.30.3

# subpackages that are used for building other specs
Provides: perl-interpreter
Provides: perl-devel
Provides: perl-macros
Provides: perl-ExtUtils-Embed
Provides: perl-open
Provides: perl-Test

