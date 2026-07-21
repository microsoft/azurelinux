// Dependabot does not update dependencies declared only with Go tool directives.
// Keep this blank import until https://github.com/dependabot/dependabot-core/issues/12050 is resolved.
//go:build tools

package azldev

import (
	_ "github.com/microsoft/azure-linux-dev-tools/pkg/app/azldev_cli"
)
