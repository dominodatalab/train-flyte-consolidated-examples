"""
Author: ddl-ebrown

The workflow returns many artifacts outputs and regular outputs. It does not use the newer train-flyte-library Artifact annotations.
"""

from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
from flytekit import Artifact
import uuid

ReportArtifact = Artifact(name="report.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact2 = Artifact(name="report2.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact3 = Artifact(name="report3.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact4 = Artifact(name="report4.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact5 = Artifact(name="report5.pdf", partition_keys=["artifact_type", "artifact_name"])
ReportArtifact6 = Artifact(name="report6.pdf", partition_keys=["artifact_type", "artifact_name"])

DataArtifact1 = Artifact(name="data.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2 = Artifact(name="data.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3 = Artifact(name="data.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4 = Artifact(name="data.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5 = Artifact(name="data.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6 = Artifact(name="data.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7 = Artifact(name="data.xlsx", partition_keys=["artifact_type", "artifact_name"])

ModelArtifact1 = Artifact(name="conda.yaml", partition_keys=["artifact_type", "artifact_name"])
ModelArtifact2 = Artifact(name="MLmodel", partition_keys=["artifact_type", "artifact_name"])
ModelArtifact3 = Artifact(name="model.pkl", partition_keys=["artifact_type", "artifact_name"])
ModelArtifact4 = Artifact(name="python_env.yaml", partition_keys=["artifact_type", "artifact_name"])
ModelArtifact5 = Artifact(name="requirements.txt", partition_keys=["artifact_type", "artifact_name"])

@workflow
def wf() -> Tuple[
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact(artifact_type="report", artifact_name="report_foo")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact2(artifact_type="report", artifact_name="report_foo")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact3(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact4(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact5(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact6(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact1(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact2(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact3(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact4(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact5(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact6(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact7(artifact_type="data", artifact_name="data_group")],

    Annotated[FlyteFile[TypeVar("yaml")], ModelArtifact1(artifact_type="model", artifact_name="model_group")],
    Annotated[FlyteFile[TypeVar("yaml")], ModelArtifact2(artifact_type="model", artifact_name="model_group")],
    Annotated[FlyteFile[TypeVar("pkl")], ModelArtifact3(artifact_type="model", artifact_name="model_group")],
    Annotated[FlyteFile[TypeVar("yaml")], ModelArtifact4(artifact_type="model", artifact_name="model_group")],
    Annotated[FlyteFile[TypeVar("txt")], ModelArtifact5(artifact_type="model", artifact_name="model_group")],

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote old_artifacts_workflow.py wf
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
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
        name="Train model1 v1",
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
        name="Train model2 v1",
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
        name="Train model3 v2",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "datacsv": FlyteFile[TypeVar("csv")],
            "datadocx": FlyteFile[TypeVar("docx")],
            "datahtml": FlyteFile[TypeVar("html")],
            "datapdf": FlyteFile[TypeVar("pdf")],
            "datartf": FlyteFile[TypeVar("rtf")],
            "datasas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "dataxlsx": FlyteFile[TypeVar("xlsx")],
            "modelcondayaml": FlyteFile[TypeVar("yaml")],
            "modelMLmodel": FlyteFile[TypeVar("yaml")],
            "modelmodelpkl": FlyteFile[TypeVar("pkl")],
            "modelpythonenvyaml": FlyteFile[TypeVar("yaml")],
            "modelrequirementstxt": FlyteFile[TypeVar("txt")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results.datapdf
    model2 = training_results2.datapdf
    model3 = training_results3.datapdf
    return model, model2, model, model, model2, model3, \
        training_results3.datacsv, \
        training_results3.datadocx, \
        training_results3.datahtml, \
        training_results3.datapdf, \
        training_results3.datartf, \
        training_results3.datasas7bdat, \
        training_results3.dataxlsx, \
        training_results3.modelcondayaml, \
        training_results3.modelMLmodel, \
        training_results3.modelmodelpkl, \
        training_results3.modelpythonenvyaml, \
        training_results3.modelrequirementstxt, \
        model
