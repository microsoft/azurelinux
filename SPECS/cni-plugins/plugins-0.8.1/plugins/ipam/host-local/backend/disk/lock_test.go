// Copyright 2016 CNI authors
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

package disk

import (
	"io/ioutil"
	"os"
	"path/filepath"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

var _ = Describe("Lock Operations", func() {
	It("locks a file path", func() {
		dir, err := ioutil.TempDir("", "")
		Expect(err).ToNot(HaveOccurred())
		defer os.RemoveAll(dir)

		// create a dummy file to lock
		path := filepath.Join(dir, "x")
		f, err := os.OpenFile(path, os.O_RDONLY|os.O_CREATE, 0666)
		Expect(err).ToNot(HaveOccurred())
		err = f.Close()
		Expect(err).ToNot(HaveOccurred())

		// now use it to lock
		m, err := NewFileLock(path)
		Expect(err).ToNot(HaveOccurred())

		err = m.Lock()
		Expect(err).ToNot(HaveOccurred())
		err = m.Unlock()
		Expect(err).ToNot(HaveOccurred())
	})

	It("locks a folder path", func() {
		dir, err := ioutil.TempDir("", "")
		Expect(err).ToNot(HaveOccurred())
		defer os.RemoveAll(dir)

		// use the folder to lock
		m, err := NewFileLock(dir)
		Expect(err).ToNot(HaveOccurred())

		err = m.Lock()
		Expect(err).ToNot(HaveOccurred())
		err = m.Unlock()
		Expect(err).ToNot(HaveOccurred())
	})
})
