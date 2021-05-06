cashification
=============

# Quick Start

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - Run: `./google-cloud-sdk/install.sh`
   - Run:  `./google-cloud-sdk/bin/gcloud init`
1. Setup the environment locally: `make create_environment`
1. Activate the environment: `conda activate cashification`
1. Build the project: `make all`
1. Find the fully produced dataset(s) in `data/datasets/`
1. Log in `gcloud auth login`
1. Set project and account `gcloud config set project cashification` 
1. Set account (may vary) `gcloud config set account language@cashification.iam.gserviceaccount.com`
1. Set environment variable. `GOOGLE_APPLICATION_CREDENTIALS=~/Cashification-ca6444f5e291.json`
1. Install NTLK data sets:
    - In a python interpreter run 
      - import ntlk
      - ntlk.download()
    - This will launch a download utility
    - Download the following data sets: brown, names, wordnet, averaged_perceptron_tagger, universal_tagset

# Re-downloading Intermediates

If your intermediates are out of date, you can re-download them by following
these steps:

1. `make clean` to clear your `data/` folder
1. `make download` to re-download intermediates, or `make all` to both
   re-download intermediates and rebuild the project

# Building the Pipeline from Scratch

This section explains how to build the entire pipeline from scratch starting
from raw tweet data.

**You shouldn't need to do this as it is time-consuming and requires
specialized hardware.** See if you can use the standard `make all` process
first before falling back to this step.

1. Set up the Docker image in `vendor/t4sa/` by running:
    - `docker build . -t t4sa`
    - `docker run --gpus 1 -p 5000:5000 t4sa`
1. Run `make build`
1. Run `make data_sync_to_gcp`

# Secrets

Secrets (usernames, passwords) are managed in `secrets.csv`

# Using the Computer Vision Model

The computer vision sentiment model requires a NVIDIA GPU and a fairly complex
setup that is not amenable to a first-time user. It's better to just rely on
the `make all` process which downloads the inference model output.
