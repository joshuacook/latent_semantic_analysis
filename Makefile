default: pdf

bash: 
	docker run -it -v $(shell pwd):/source --name bash joshuacook/miniconda /bin/bash
	docker rm bash
	
clean_docker:
	docker rm $(docker ps -aq)	

jupyter:
	docker run -v $(shell pwd):/home/jovyan/work --name jupyter -d -p 80:8888 joshuacook/datascience 

notebook:
	docker run -d \
		-p 27017:27017 \
		-v $(pwd)/data:/data/db \
		--name mongo \
		mongo
	docker run -it \
		-v $(shell pwd):/source \
		--name miniconda \
		--link mongo:mongo \
		joshuacook/miniconda python src/notebook.py
	docker rm miniconda mongo
	
pdf:
	pandoc doc/latent_semantic_analysis.md \
	-t latex \
	-H doc/fix.tex \
	--toc \
	-f markdown+tex_math_double_backslash \
	-o doc/latent_semantic_analysis.pdf \
	--latex-engine=xelatex

test_binaries:
	python3 test/binaries.py
	
watch_and_make:
	while true; do kqwait doc/latent_semantic_analysis.md; make; done