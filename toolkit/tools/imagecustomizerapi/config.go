// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import "fmt"

type Config struct {
	Storage Storage `yaml:"storage"`
	Iso     *Iso    `yaml:"iso"`
	OS      *OS     `yaml:"os"`
	Scripts Scripts `yaml:"scripts"`
}

func (c *Config) IsValid() (err error) {
	err = c.Storage.IsValid()
	if err != nil {
		return err
	}

	hasResetPartitionsUuids := c.Storage.ResetPartitionsUuidsType != ResetPartitionsUuidsTypeDefault

	if c.Iso != nil {
		err = c.Iso.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'iso' field:\n%w", err)
		}
	}

	hasResetBootLoader := false
	if c.OS != nil {
		err = c.OS.IsValid()
		if err != nil {
			return fmt.Errorf("invalid 'os' field:\n%w", err)
		}
		hasResetBootLoader = c.OS.ResetBootLoaderType != ResetBootLoaderTypeDefault
	}

	err = c.Scripts.IsValid()
	if err != nil {
		return err
	}

	if c.CustomizePartitions() && !hasResetBootLoader {
		return fmt.Errorf("'os.resetBootLoaderType' must be specified if 'storage.disks' is specified")
	}

	if hasResetPartitionsUuids && !hasResetBootLoader {
		return fmt.Errorf("'os.resetBootLoaderType' must be specified if 'storage.resetPartitionsUuidsType' is specified")
	}

	if c.OS != nil && c.OS.Verity != nil {
		err := ensureVerityPartitionIdExists(c.OS.Verity.DataPartition, &c.Storage)
		if err != nil {
			return fmt.Errorf("invalid verity 'dataPartition':\n%w", err)
		}

		err = ensureVerityPartitionIdExists(c.OS.Verity.HashPartition, &c.Storage)
		if err != nil {
			return fmt.Errorf("invalid verity 'hashPartition':\n%w", err)
		}
	}

	return nil
}

func ensureVerityPartitionIdExists(verityPartition IdentifiedPartition, storage *Storage) error {
	switch verityPartition.IdType {
	case IdTypeId:
		if !storage.CustomizePartitions() {
			return fmt.Errorf("'idType' cannot be 'id' if 'storage.disks' is not specified")
		}

		foundPartition := false
		for _, disk := range storage.Disks {
			for _, partition := range disk.Partitions {
				if partition.Id == verityPartition.Id {
					foundPartition = true
					break
				}
			}
		}

		if !foundPartition {
			return fmt.Errorf("partition with 'id' (%s) not found", verityPartition.Id)
		}
	}

	return nil
}

func (c *Config) CustomizePartitions() bool {
	return c.Storage.CustomizePartitions()
}
