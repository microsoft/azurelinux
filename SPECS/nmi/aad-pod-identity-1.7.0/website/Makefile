bootstrap:
	git submodule update --init --recursive
	npm i

serve: bootstrap
	hugo server \
		--buildDrafts \
		--buildFuture \
		--disableFastRender

production-build: bootstrap
	hugo --minify

preview-build: bootstrap
	hugo \
		--baseURL $(DEPLOY_PRIME_URL) \
		--buildDrafts \
		--buildFuture \
		--minify
