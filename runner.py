"""
This script is meant to be run from the command line
to run pipeline to Vertex AI Pipelines

Example:
    python runner.py
"""

import subprocess as sp

from google.cloud import aiplatform
from google.oauth2.credentials import Credentials

AUTHENTICATION_TOKEN = (
    sp.check_output("gcloud auth print-access-token", shell=True)
    .decode("utf-8")
    .rstrip()
)


creds = Credentials(AUTHENTICATION_TOKEN)


PROJECT = "mlops-explorations"

aiplatform.init(project=PROJECT, credentials=creds)


job = aiplatform.PipelineJob(
    display_name="sample",
    template_path="pipeline.yaml",
    # pipeline_root=PIPELINE_ROOT,
    credentials=creds,
    enable_caching=False,
    project=PROJECT,
    parameter_values={
        "another_json_file": "gs://mlops-explorations-vertex-pipelines-us-central1/one_file.json",
        "one_json_file": "gs://mlops-explorations-vertex-pipelines-us-central1/two_file.json",
    },
    location="us-central1",
)

job.submit()
