.PHONY: twitter_sync_from_scraper twitter_sync_to_scraper \
		data_sync_from_gcp data_sync_to_gcp \
		twitter twitter_images \
		download \
		text_sentiment image_sentiment twitter_features \
		features \
		twitter_dataset \
		datasets \
		all build post_build

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(patsubst %/$(firstword $(MAKEFILE_LIST)),%,$(realpath $(firstword $(MAKEFILE_LIST))))
BUCKET = cashification.appspot.com
PROJECT_NAME = cashification
PYTHON_FLAGS = PYTHONPATH=$(PYTHONPATH):"$(PROJECT_DIR)/src"

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

twitter_sync_from_scraper:
	mkdir -p data/raw/twitter/
	gsutil -m rsync -r gs://$(BUCKET)/Tweets/ data/raw/twitter/
	mkdir -p data/raw/twitter_images/
	gsutil -m rsync -r gs://$(BUCKET)/TweetImages/ data/raw/twitter_images/

twitter_sync_to_scraper:
	gsutil -m rsync -r data/raw/twitter/ gs://$(BUCKET)/Tweets/
	gsutil -m rsync -r data/raw/twitter_images/ gs://$(BUCKET)/TweetImages/

data_sync_from_gcp:
	mkdir -p data/raw/
	gsutil -m rsync -r gs://$(BUCKET)/data/raw/ data/raw/
	mkdir -p data/features/
	gsutil -m rsync -r gs://$(BUCKET)/data/features/ data/features/

data_sync_to_gcp:
	gsutil -m rsync -r data/raw/ gs://$(BUCKET)/data/raw/
	gsutil -m rsync -r data/features/ gs://$(BUCKET)/data/features/

data_sync_minimum_from_gcp:
	mkdir -p data/raw/twitter/
	gsutil -m rsync -r gs://$(BUCKET)/data/raw/twitter/ data/raw/twitter/
	mkdir -p data/features/
	gsutil -m rsync -r gs://$(BUCKET)/data/features/ data/features/

stocks:
	$(PYTHON_FLAGS) python -m download.stocks \
		data/raw/twitter/ \
		data/raw/stocks/ \
		AAPL TSLA SPY

# NOTE:
# Twitter fetch from scraper is never-ending, so don't include it in the `make` pipeline
twitter:
	$(PYTHON_FLAGS) python -m download.twitter \
		data/raw/twitter/

twitter_images:
	$(PYTHON_FLAGS) python -m download.twitter_images \
		data/raw/twitter/ \
		data/raw/twitter_images/

## Download the datasets
download: data_sync_minimum_from_gcp stocks # `stocks` must be after since it depends on Twitter data

text_sentiment:
	$(PYTHON_FLAGS) python -m features.text_sentiment \
		data/processed/twitter/ \
		data/features/text_sentiment/

entity_sentiment:
	$(PYTHON_FLAGS) python -m features.entity_sentiment \
		data/processed/twitter/ \
		data/features/entity_sentiment/

image_sentiment:
	$(PYTHON_FLAGS) python -m features.image_sentiment \
		data/raw/twitter_images/ \
		data/features/image_sentiment/

preprocess:
	$(PYTHON_FLAGS) python -m preprocess.normalize \
		data/raw/twitter/ \
		data/processed/twitter/

twitter_features: image_sentiment text_sentiment

features: twitter_features

twitter_interim:
	$(PYTHON_FLAGS) python -m interim.merge_jsons \
		data/interim/twitter_and_sentiment.json \
		data/raw/twitter/ data/features/image_sentiment/ data/features/text_sentiment/

interim: twitter_interim

stocks_dataset:
	mkdir -p data/datasets/
	cp data/raw/stocks/*.json data/datasets/

twitter_dataset:
	$(PYTHON_FLAGS) python -m datasets.twitter_dataset \
		data/interim/twitter_and_sentiment.json \
		data/datasets/twitter_and_sentiment.json \
		--period 1min

datasets: twitter_dataset stocks_dataset

all: download interim datasets

build: twitter_sync_from_scraper twitter_images preprocess features interim datasets

post_build: twitter_sync_to_scraper data_sync_to_gcp

## Delete all compiled Python files and datasets
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf data/*

## Create Conda/Python environment
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
else
		@echo ">>> conda not installed, please install at https://conda.io/"
		exit 1
endif
	conda env create -f "$(PROJECT_DIR)/$(PROJECT_NAME).yml"
	@echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

## Update Conda/Python environment
update_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
else
		@echo ">>> conda not installed, please install at https://conda.io/"
		exit 1
endif
	conda env update -f "$(PROJECT_DIR)/$(PROJECT_NAME).yml"
	@echo ">>> Conda env updated. Activate with:\nconda activate $(PROJECT_NAME)"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
