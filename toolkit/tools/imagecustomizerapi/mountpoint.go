package imagecustomizerapi

import (
	"fmt"

	"gopkg.in/yaml.v3"
)

// MountPoint holds the mounting information for each partition.
type MountPoint struct {
	// The ID type to use for the source in the /etc/fstab file.
	IdType MountIdentifierType `yaml:"idType,omitempty"`
	// The additional options for the mount.
	Options string `yaml:"options,omitempty"`
	// The target directory path of the mount.
	Path string `yaml:"path,omitempty"`
}

// UnmarshalYAML enables MountPoint to handle both a shorthand path and a structured object.
func (p *MountPoint) UnmarshalYAML(value *yaml.Node) error {
	// Check if the node is a scalar (i.e., single path string).
	if value.Kind == yaml.ScalarNode {
		// Treat scalar value as the Path directly.
		p.Path = value.Value
		return nil
	}

	// Otherwise, decode as a full MountPoint struct.
	type Alias MountPoint
	var mp Alias
	if err := value.Decode(&mp); err != nil {
		return fmt.Errorf("failed to parse MountPoint struct: %w", err)
	}
	*p = MountPoint(mp)
	return nil
}

// IsValid returns an error if the MountPoint is not valid
func (p *MountPoint) IsValid() error {

	if p.Path == "" {
		return fmt.Errorf("invalid path: path cannot be empty")
	}

	err := p.IdType.IsValid()
	if err != nil {
		return fmt.Errorf("invalid idType value:\n%w", err)
	}

	// Use validatePath to check the Path field.
	if err := validatePath(p.Path); err != nil {
		return fmt.Errorf("invalid path:\n%w", err)
	}

	// Use validateMountOptions to check Options.
	if validateMountOptions(p.Options) {
		return fmt.Errorf("options (%s) contain spaces, tabs, or newlines and are invalid", p.Options)
	}

	return nil
}
