#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

from typing import Literal
from uuid import UUID
from config.config_manager import ConfigManager
from tractusx_sdk.dataspace.services.connector.v0_9_0.edc_service import EdcService

class EDCManager:
    """Manager for handling EDC (Eclipse DataSpace Connector) related operations."""

    def __init__(
            self,
            backendUrl, 
            edcBaseUrl, 
            edcDMApath
        ):
        # TODO: Initialize any required parameters or configurations here
        
        self.backendUrl = backendUrl #Get the backend url to configure the EDC manager
        self.edcService = EdcService(
            base_url=edcBaseUrl,
            dma_path=edcDMApath
        )

    def createContract(self, DTR:bool = False, semanticId:str = None ):
        
        """
            Method to create a contract in the EDC
            
            @DTR - Specifies if the contract is for DTR - Default=False (for Submodel)
        """
        
        if (DTR):
            #Build contract for registering DTR in the EDC
            (_DTRUrl, _DTRVersion, _DTRDctType, 
                _DTRUsagePolicy, _DTRAccessPolicy) = self._configContract(DTR=True)
            
            #1. Build the Asset
            _DTRAsset = self._createDTRAsset()
            
            #2. Register the Policies in the EDC
            self._registerPolicies(_DTRAccessPolicy, _DTRUsagePolicy)
            
            #3. Create the contract and register it in the EDC
            self._registerContract(_DTRAsset["@id"],_DTRAccessPolicy,_DTRUsagePolicy)
            

        else:
            #Build contract for registering a Submodel in the EDC
            (_submodelUrl, _submodelVersion, _submodelDctType, 
                _submodelUsagePolicy, _submodelAccessPolicy) = self._configContract(DTR=False, semanticId=semanticId)
            
            #1. Build the Asset
            _submodelAsset = self._createSubmodelAsset()
            
            #2. Register the Policies in the EDC
            self._registerPolicies(_submodelAccessPolicy, _submodelUsagePolicy)
            
            #3. Create the contract and register it in the EDC
            self._registerContract(_submodelAsset["@id"],_submodelAccessPolicy,_submodelUsagePolicy)

    def _configContract(self, DTR:bool, semanticId=None):
        """
            Sets the configuration to create a contract in the EDC 
            
            @DTR - Specifies if url is built for the DTR or not (False for a submodel url)
            @semanticId - Specifies the semanticId - Only for building backend Urls for submodels
        """
        pass

    def _registerContract(self, assetId, accessPolicy, usagePolicy):
        contract = {
            "@context": {
                "@vocab": "https://w3id.org/edc/v0.0.1/ns/"
            },
            "@type": "ContractDefinition",
            "@id": "<<uuid>>",
            "accessPolicyId": accessPolicy["@id"],
            "contractPolicyId": usagePolicy["@id"],
            "assetsSelector": [
                {
                "operandLeft": "https://w3id.org/edc/v0.0.1/ns/id",
                "operator": "=",
                "operandRight": assetId,
                }
            ]
        }
        return contract

    def _buildDTRUrl(self):
        """
            Builds the DTR Url according to DTR Manager conventions
        """
        dtr_hostname = ConfigManager.get_config('digitalTwinRegistry.hostname')
        dtr_uri = ConfigManager.get_config('digitalTwinRegistry.uri')
        dtr_api_path = ConfigManager.get_config('digitalTwinRegistry.apiPath')
        dtr_url = f"{dtr_hostname}{dtr_uri}{dtr_api_path}"
        return dtr_url

    def _buildBackendUrlSubmodel(self, semanticId:str):
        """
            Builds the Submodel Url according to conventions <url of ic-hub>/submodel-dispatcher/<semantic-id-placeholder>/<global id>/submodel
        """
        #Create the submodel url
        submodel_url = f"{self.backendUrl}/submodel-dispatcher/{semanticId}"
        return submodel_url
    
        
    def _createUsagePolicy(self):
        """
            Creates an Usage Policy
        """
        pass

    def _createAccessPolicy(self):
        """
            Creates an Access Policy
        """
        pass

    def _registerPolicies(self, accessPolicy, usagePolicy):
        """
            Register the usage and access policies in the EDC
        """
        pass

    def _createDTRAsset(self, dctType, dtrUrl):
        """
            Generates the asset for the DTR
        """
        asset = { "@id": self._generateId(DTR=True),
                    "properties": {
                        "dct:type": {
                            "@id": dctType
                        },
                        "cx-common:version": "3.0",
                    },
                    "privateProperties": {
                    },
                    "dataAddress": {
                        "@type": "DataAddress",
                        "type": "HttpData",
                        "baseUrl": dtrUrl,
                        "proxyQueryParams": "true", #Allowed for the DTR
                        "proxyPath": "true",
                        "proxyMethod": "false"
                    }
                }
        return asset


    def _createSubmodelAsset(self, dctType, semanticId, submodelUrl):
        """
            Generates the asset for the Submodel
        """
        asset = { "@id": self._generateId(DTR=False, semanticId=semanticId),
                    "properties": {
                        "dct:type": {
                            "@id": dctType
                        },
                        "cx-common:version": "3.0",
                        "aas-semantics:semanticId": { 
                            "@id": semanticId
                        }
                    },
                    "privateProperties": {
                    },
                    "dataAddress": {
                        "@type": "DataAddress",
                        "type": "HttpData",
                        "baseUrl": submodelUrl,
                        "proxyQueryParams": "false",
                        "proxyPath": "true",
                        "proxyMethod": "false"
                    }
                }
        return asset
    
    def _generateId(self, DTR:bool, semanticId=None):
        pass

   
            
    
         

    



















































    def register_submodel_asset(self, global_id: str, semantic_id: str, aas_id: UUID, submodel_id: UUID):
        """Register a submodel asset in the EDC."""
        # Implementation for registering a submodel asset
        print("=====================================")
        print("==== Eclipse Dataspace Connector ====")
        print("=====================================")
        print(f"Registering submodel asset with Global ID: {global_id}")
        print(f"Semantic ID: {semantic_id}")
        print(f"AAS ID: {aas_id}")
        print(f"Submodel ID: {submodel_id}")
        print("Submodel asset registered successfully (dummy implementation).")
        print()

    def register_submodel_bundle_asset(self, semantic_id: str):
        """Register a submodel bundle asset in the EDC."""
        # Implementation for registering a submodel bundle asset
        print("=====================================")
        print("==== Eclipse Dataspace Connector ====")
        print("=====================================")
        print(f"Registering submodel bundle asset with Semantic ID: {semantic_id}")
        print("Submodel bundle asset registered successfully (dummy implementation).")
        print()
