"""
Multi-bundle file attachment demo.

This workflow produces four artifacts and attaches them to governance
bundles on run completion. Each ExportArtifactFilesToBundleSpec maps
one or more artifact files to one or more bundles:

  Bundle Alpha  ← model.pkl, metrics.json
  Bundle Beta   ← model.pkl, metrics.json, report.html
  Bundle Gamma  ← report.html, training_data.csv

Prerequisites:
  - Bundles named "Test Bundle Alpha", "Test Bundle Beta", and
    "Test Bundle Gamma" must exist in the same project.
  - The project must have a Flows environment configured.

Run from a Domino workspace:
  pyflyte run --remote multi_bundle_attach.py multi_bundle_demo
"""

from flytekit import task, workflow
from flytekit.types.file import FlyteFile

from flytekitplugins.domino.artifact import (
    DATA,
    MODEL,
    REPORT,
    Artifact,
    ExportArtifactFilesToBundleSpec,
    run_launch_export_artifacts_task,
)

# ── Artifact definitions ─────────────────────────────────────────────
ModelArtifact = Artifact(name="risk-model", type=MODEL)
ReportArtifact = Artifact(name="risk-report", type=REPORT)
DataArtifact = Artifact(name="training-data", type=DATA)

ModelFile = ModelArtifact.File(name="model.pkl")
ReportFile = ReportArtifact.File(name="report.html")
DataFile = DataArtifact.File(name="training_data.csv")
MetricsFile = ModelArtifact.File(name="metrics.json")


# ── Tasks ────────────────────────────────────────────────────────────
@task
def produce_model() -> ModelFile:  # type: ignore[valid-type]
    path = "/tmp/model.pkl"
    with open(path, "wb") as f:
        f.write(b"mock model bytes")
    return FlyteFile(path)


@task
def produce_report() -> ReportFile:  # type: ignore[valid-type]
    path = "/tmp/report.html"
    with open(path, "w") as f:
        f.write("<html><body><h1>Risk Assessment Report</h1></body></html>")
    return FlyteFile(path)


@task
def produce_data() -> DataFile:  # type: ignore[valid-type]
    path = "/tmp/training_data.csv"
    with open(path, "w") as f:
        f.write("feature_a,feature_b,label\n1,2,0\n3,4,1\n")
    return FlyteFile(path)


@task
def produce_metrics() -> MetricsFile:  # type: ignore[valid-type]
    path = "/tmp/metrics.json"
    with open(path, "w") as f:
        f.write('{"accuracy": 0.97, "auc": 0.99}')
    return FlyteFile(path)


# ── Workflow ─────────────────────────────────────────────────────────
@workflow
def multi_bundle_demo():
    produce_model()
    produce_report()
    produce_data()
    produce_metrics()

    run_launch_export_artifacts_task(
        spec_list=[
            # model.pkl + metrics.json → Alpha and Beta
            ExportArtifactFilesToBundleSpec(
                files=[ModelFile, MetricsFile],
                bundles=["Test Bundle Alpha", "Test Bundle Beta"],
            ),
            # report.html → Beta and Gamma
            ExportArtifactFilesToBundleSpec(
                files=[ReportFile],
                bundles=["Test Bundle Beta", "Test Bundle Gamma"],
            ),
            # training_data.csv → Gamma only
            ExportArtifactFilesToBundleSpec(
                files=[DataFile],
                bundles=["Test Bundle Gamma"],
            ),
        ],
        use_project_defaults_for_omitted=True,
    )
