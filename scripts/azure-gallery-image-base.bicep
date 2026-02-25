param galleryName string
param imageDefinitionName string
param versionName string
param location string = resourceGroup().location
param regions array = [resourceGroup().location]
param sourceDiskId string
param sourceDiskUrl string
param defaultReplicaCount int = 1
param excludedFromLatest bool = false
param allowDeletionOfReplicatedLocations bool = false
param replicationMode string = 'Shallow'
resource imageVersion 'Microsoft.Compute/galleries/images/versions@2024-03-03' = {
  name: '${galleryName}/${imageDefinitionName}/${versionName}'
  location: location
  properties: {
    publishingProfile: {
      replicaCount: defaultReplicaCount
      targetRegions: [
        for region in regions: {
          name: region
          regionalReplicaCount: defaultReplicaCount
          storageAccountType: 'Standard_LRS'
        }
      ]
      excludeFromLatest: excludedFromLatest
      replicationMode: replicationMode
    }
    storageProfile: {
      osDiskImage: {
        hostCaching: 'ReadWrite'
        source: {
          storageAccountId: sourceDiskId
          uri: sourceDiskUrl
        }
      }
    }
    safetyProfile: {
      allowDeletionOfReplicatedLocations: allowDeletionOfReplicatedLocations
    }
  }
  tags: {}
}
