// Copyright 2017 CNI authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package hns

import (
	"encoding/json"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("HNS NetConf", func() {
	Describe("ApplyOutBoundNATPolicy", func() {
		Context("when not set by user", func() {
			It("sets it by adding a policy", func() {

				// apply it
				n := NetConf{}
				n.ApplyOutboundNatPolicy("192.168.0.0/16")

				addlArgs := n.Policies
				Expect(addlArgs).Should(HaveLen(1))

				policy := addlArgs[0]
				Expect(policy.Name).Should(Equal("EndpointPolicy"))

				value := make(map[string]interface{})
				json.Unmarshal(policy.Value, &value)

				Expect(value).Should(HaveKey("Type"))
				Expect(value).Should(HaveKey("ExceptionList"))
				Expect(value["Type"]).Should(Equal("OutBoundNAT"))

				exceptionList := value["ExceptionList"].([]interface{})
				Expect(exceptionList).Should(HaveLen(1))
				Expect(exceptionList[0].(string)).Should(Equal("192.168.0.0/16"))
			})
		})

		Context("when set by user", func() {
			It("appends exceptions to the existing policy", func() {
				// first set it
				n := NetConf{}
				n.ApplyOutboundNatPolicy("192.168.0.0/16")

				// then attempt to update it
				n.ApplyOutboundNatPolicy("10.244.0.0/16")

				// it should be unchanged!
				addlArgs := n.Policies
				Expect(addlArgs).Should(HaveLen(1))

				policy := addlArgs[0]
				Expect(policy.Name).Should(Equal("EndpointPolicy"))

				var value map[string]interface{}
				json.Unmarshal(policy.Value, &value)

				Expect(value).Should(HaveKey("Type"))
				Expect(value).Should(HaveKey("ExceptionList"))
				Expect(value["Type"]).Should(Equal("OutBoundNAT"))

				exceptionList := value["ExceptionList"].([]interface{})
				Expect(exceptionList).Should(HaveLen(2))
				Expect(exceptionList[0].(string)).Should(Equal("192.168.0.0/16"))
				Expect(exceptionList[1].(string)).Should(Equal("10.244.0.0/16"))
			})
		})
	})

	Describe("ApplyDefaultPAPolicy", func() {
		Context("when not set by user", func() {
			It("sets it by adding a policy", func() {

				n := NetConf{}
				n.ApplyDefaultPAPolicy("192.168.0.1")

				addlArgs := n.Policies
				Expect(addlArgs).Should(HaveLen(1))

				policy := addlArgs[0]
				Expect(policy.Name).Should(Equal("EndpointPolicy"))

				value := make(map[string]interface{})
				json.Unmarshal(policy.Value, &value)

				Expect(value).Should(HaveKey("Type"))
				Expect(value["Type"]).Should(Equal("PA"))

				paAddress := value["PA"].(string)
				Expect(paAddress).Should(Equal("192.168.0.1"))
			})
		})

		Context("when set by user", func() {
			It("does not override", func() {
				n := NetConf{}
				n.ApplyDefaultPAPolicy("192.168.0.1")
				n.ApplyDefaultPAPolicy("192.168.0.2")

				addlArgs := n.Policies
				Expect(addlArgs).Should(HaveLen(1))

				policy := addlArgs[0]
				Expect(policy.Name).Should(Equal("EndpointPolicy"))

				value := make(map[string]interface{})
				json.Unmarshal(policy.Value, &value)

				Expect(value).Should(HaveKey("Type"))
				Expect(value["Type"]).Should(Equal("PA"))

				paAddress := value["PA"].(string)
				Expect(paAddress).Should(Equal("192.168.0.1"))
				Expect(paAddress).ShouldNot(Equal("192.168.0.2"))
			})
		})
	})

	Describe("MarshalPolicies", func() {
		Context("when not set by user", func() {
			It("sets it by adding a policy", func() {

				n := NetConf{
					Policies: []policy{
						{
							Name:  "EndpointPolicy",
							Value: []byte(`{"someKey": "someValue"}`),
						},
						{
							Name:  "someOtherType",
							Value: []byte(`{"someOtherKey": "someOtherValue"}`),
						},
					},
				}

				result := n.MarshalPolicies()
				Expect(len(result)).To(Equal(1))

				policy := make(map[string]interface{})
				err := json.Unmarshal(result[0], &policy)
				Expect(err).ToNot(HaveOccurred())
				Expect(policy).Should(HaveKey("someKey"))
				Expect(policy["someKey"]).To(Equal("someValue"))
			})
		})

		Context("when set by user", func() {
			It("appends exceptions to the existing policy", func() {
				// first set it
				n := NetConf{}
				n.ApplyOutboundNatPolicy("192.168.0.0/16")

				// then attempt to update it
				n.ApplyOutboundNatPolicy("10.244.0.0/16")

				// it should be unchanged!
				addlArgs := n.Policies
				Expect(addlArgs).Should(HaveLen(1))

				policy := addlArgs[0]
				Expect(policy.Name).Should(Equal("EndpointPolicy"))

				var value map[string]interface{}
				json.Unmarshal(policy.Value, &value)

				Expect(value).Should(HaveKey("Type"))
				Expect(value).Should(HaveKey("ExceptionList"))
				Expect(value["Type"]).Should(Equal("OutBoundNAT"))

				exceptionList := value["ExceptionList"].([]interface{})
				Expect(exceptionList).Should(HaveLen(2))
				Expect(exceptionList[0].(string)).Should(Equal("192.168.0.0/16"))
				Expect(exceptionList[1].(string)).Should(Equal("10.244.0.0/16"))
			})
		})
	})
})
