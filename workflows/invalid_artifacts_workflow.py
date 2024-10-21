"""
Author: ddl-ebrown

The workflow returns many artifacts outputs and regular outputs. It uses the newer train-flyte-library Artifact annotations.
"""

from flytekitplugins.domino.artifact import (
    Artifact,
    DATA,
    MODEL,
    REPORT,
)
from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from typing import TypeVar, Optional, List, Dict, Annotated, Tuple, NamedTuple
import uuid

ReportArtifactFoo = Artifact("report_foo", REPORT)
ReportArtifactBar = Artifact("", REPORT)
DataArtifact = Artifact("data_group", DATA)
ModelArtifact = Artifact("model_group", MODEL)

@workflow
def wf() -> Tuple[
    ReportArtifactFoo.File(name="report.pdf", type="pdf"),
    ReportArtifactFoo.File(name="report2.pdf", type="pdf"),
    ReportArtifactBar.File(name="report3.pdf", type="pdf"),
    ReportArtifactBar.File(name="report4.pdf", type="pdf"),
    ReportArtifactBar.File(name="report5.pdf", type="pdf"),
    ReportArtifactBar.File(name="report6.pdf", type="pdf"),
    DataArtifact.File(name="data.csv", type="csv"),
    DataArtifact.File(name="data.docx", type="docx"),
    DataArtifact.File(name="data.html", type="html"),
    DataArtifact.File(name="data.pdf", type="pdf"),
    DataArtifact.File(name="data.rtf", type="rtf"),
    DataArtifact.File(name="data.sas7bdat", type="sas7bdat"),
    DataArtifact.File(name="data.xlsx", type="xlsx"),

    ModelArtifact.File(name="conda.yaml", type="yaml"),
    ModelArtifact.File(name="MLModel", type="yaml"),
    ModelArtifact.File(name="model.pkl", type="pkl"),
    ModelArtifact.File(name="python_env.yaml", type="yaml"),
    ModelArtifact.File(name="requirements.txt", type="txt"),

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote artifacts_workflow.py wf
    """

    data_prep_results = DominoJobTask(    
        name="Prepare data",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            "processed_data": DataArtifact.File(name="processed.csv", type="csv"),
            "processed_data2": DataArtifact.File(name="processed2.csv", type="csv"),
        },
        use_latest=True,
    )(data_path="/mnt/train-flyte-consolidated-examples/data/data.csv")

    training_results = DominoJobTask(
        name="Train model1 v1",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
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
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
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
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
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
