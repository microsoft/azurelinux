Building of "toolchain" packages - packages, which form the base of every Mock build environment.

Pre-test state:
- No explicit build dependencies between A and B.


Test case I:
- A and B are "toolchain" packages.
- Mock build environment has A and B installed from upstream.
- Upstream A and B older than local.

Expectation:
- B builds.     [Mock state: older A,   older B]
- A builds.     [Mock state: older A,   dirty B]
- B rebuilds.   [Mock state: dirty A,   current B]
- A rebuilds.   [Mock state: current A, current B]

Where:
- dirty package == the package built in Mock containing at least one older package.
- older package == package build input doesn't match anything available upstream.


Test case II:
- A and B are "toolchain" packages.
- Mock build environment has A and B installed from upstream.
- Upstream A current with local A.
- Upstream B older than local B.
- "Cascading rebuilds" set to 1.

Expectation:
- B builds.                     [Mock state: current A, older B]
- A and B rebuild in parallel.  [Mock state: current A, dirty B]
- A rebuilt caused by cascading rebuilds.
- B rebuilt caused by a need to build in a Mock with no older packages.


Test case III:
- A and B are "toolchain" packages.
- Mock build environment has A and B installed from upstream.
- Upstream A current with local A.
- Upstream B older than local B.
- "Cascading rebuilds" set to 0.

Expectation:
- B builds.     [Mock state: current A, older B]
- B rebuilds.   [Mock state: current A, dirty B]
- A doesn't rebuild.
- B rebuilt caused by a need to build in a Mock with no older packages.


Test case IV:
- A is a "regular" package.
- B is a "toolchain" package.
- Mock build environment has B installed from upstream.
- Upstream A current with local A.
- Upstream B older than local B.
- "Cascading rebuilds" set to 1.

Expectation:
- B builds.             [Mock state: older B]
- B rebuilds.           [Mock state: dirty B]
- A rebuilds after B.   [Mock state: current B]
- A rebuilt caused by cascading rebuilds.
- B rebuilt caused by a need to build in a Mock with no older packages.




Question from cases II and IV:

Do we require "regular" packages to build with current-only packages,
while a mix of current and dirty ones are OK for "toolchain" packages?
