"""
Author(s): ddl-ebrown, ddl-galias, ddl-rliu

The workflow returns many artifacts outputs and regular outputs, and calls nested workflows which
also return artifacts outputs. It does not use the newer train-flyte-library Artifact annotations.
"""

from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact
import uuid

# to use partition_keys (necessary for Domino), we have to define this type up front -- this entire definition should be eliminated
ReportArtifact = Artifact(name="report.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact2 = Artifact(name="report2.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact3 = Artifact(name="report3.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact4 = Artifact(name="report4.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact5 = Artifact(name="report5.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact6 = Artifact(name="report6.pdf", partition_keys=["artifact_type", "artifact_name"])

@workflow
def nested_wf() -> Tuple[
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact3(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact4(artifact_type="report", artifact_name="report_bar")], 
]:

    data_prep_results = DominoJobTask(    
        name="Prepare data 1",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat", version=str(uuid.uuid4()))],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat", version=str(uuid.uuid4()))],
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")

    training_results = DominoJobTask(
        name="Train model 2",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results2 = DominoJobTask(
        name="Train model 3",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    model = training_results['model']
    model2 = training_results2['model']
    return model, model2

@workflow
def nested_wf_dupe() -> Tuple[
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact5(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact6(artifact_type="report", artifact_name="report_bar")], 
]:

    data_prep_results = DominoJobTask(    
        name="Prepare data 4",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat", version=str(uuid.uuid4()))],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat", version=str(uuid.uuid4()))],
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")

    training_results = DominoJobTask(
        name="Train model 5",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results2 = DominoJobTask(
        name="Train model 6",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    model = training_results['datapdf']
    model2 = training_results2['datapdf']
    return model, model2

@workflow
def wf() -> Tuple[
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact(artifact_type="report", artifact_name="report_foo")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact2(artifact_type="report", artifact_name="report_foo")], 

    # ideally the definition looks more like this:
    # Annotated[FlyteFile, Artifact(name="report.pdf", Group=ReportGroup)], 
    # this could be further simplified in the programming model if we know that these artifacts are only a single file like
    # ArtifactFile(name="report.pdf", Group=ReportGroup)

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote old_nested_artifacts_workflow.py wf
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data 7",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat", version=str(uuid.uuid4()))],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat", version=str(uuid.uuid4()))],
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")
    nested_wf()
    nested_wf_dupe()

    training_results = DominoJobTask(
        name="Train model 8",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results2 = DominoJobTask(
        name="Train model 9",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results3 = DominoJobTask(
        name="Train model 10",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datapdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results['datapdf']
    model2 = training_results2['datapdf']
    model3 = training_results3['datapdf']
    return model, model2, model3
