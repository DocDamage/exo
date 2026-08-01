.PHONY: dev release test hello snow check shaders clean

dev release test hello snow:
	./scripts/build.sh $@

check:
	python3 scripts/check_repo.py

shaders:
	python3 scripts/compile_shaders.py --clean

clean:
	rm -rf build
	find assets/shaders -name '*.spv' -delete
