"""
Author: ddl-ebrown, ddl-rliu

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

ReportArtifactTFL = Artifact("TFL Reports", REPORT)
DataArtifactADaM = Artifact("ADaM Datasets", DATA)

@workflow
def ADaM_TFL() -> Tuple[
    ReportArtifactTFL.File(name="report.pdf", type="pdf"),
    ReportArtifactTFL.File(name="report2.pdf", type="pdf"),
    ReportArtifactTFL.File(name="report3.pdf", type="pdf"),
    ReportArtifactTFL.File(name="report4.pdf", type="pdf"),
    ReportArtifactTFL.File(name="report5.pdf", type="pdf"),
    ReportArtifactTFL.File(name="report6.pdf", type="pdf"),
    DataArtifactADaM.File(name="data.csv", type="csv"),
    DataArtifactADaM.File(name="data.docx", type="docx"),
    DataArtifactADaM.File(name="data.html", type="html"),
    DataArtifactADaM.File(name="data.pdf", type="pdf"),
    DataArtifactADaM.File(name="data.rtf", type="rtf"),
    DataArtifactADaM.File(name="data.sas7bdat", type="sas7bdat"),
    DataArtifactADaM.File(name="data.xlsx", type="xlsx"),

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote lifescience_workflow.py ADaM_TFL
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
            "processed_data": DataArtifactADaM.File(name="processed.csv", type="csv"),
            "processed_data2": DataArtifactADaM.File(name="processed2.csv", type="csv"),
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")

    training_results = DominoJobTask(
        name="Create ADSL Dataset",
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
        name="Create ADAE Dataset",
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
        name="Create ADVS Dataset",
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
            "data1sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data2sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data3sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data4sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data5sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data6sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data7sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data8sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data9sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data10sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data11sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data12sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data13sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data14sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data15sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data16sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data17sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data18sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data19sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data20sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data21sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data22sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data23sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data24sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data25sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data26sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data27sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data28sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data29sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data30sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data31sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data32sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data33sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data34sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data35sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data36sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data37sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data38sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data39sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data40sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data41sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data42sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data43sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data44sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data45sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data46sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data47sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data48sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data49sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data50sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data51sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data52sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data53sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data54sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data55sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data56sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data57sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data58sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data59sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data60sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data61sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data62sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data63sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data64sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data65sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data66sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data67sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data68sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data69sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data70sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data71sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data72sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data73sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data74sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data75sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data76sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data77sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data78sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data79sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data80sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data81sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data82sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data83sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data84sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data85sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data86sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data87sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data88sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data89sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data90sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data91sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data92sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data93sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data94sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data95sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data96sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data97sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data98sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data99sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "dataxlsx": FlyteFile[TypeVar("xlsx")],
            "modelcondayaml": FlyteFile[TypeVar("yaml")],
            "modelMLmodel": FlyteFile[TypeVar("yaml")],
            "modelmodelpkl": FlyteFile[TypeVar("pkl")],
            "modelpythonenvyaml": FlyteFile[TypeVar("yaml")],
            "modelrequirementstxt": FlyteFile[TypeVar("txt")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    from flytekitplugins.domino.artifact import Artifact, DATA, ExportArtifactToDatasetsSpec, ExportArtifactToNetAppVolumesSpec, MODEL, REPORT, run_launch_export_artifacts_task
    # Programmatic export is enabled here
    run_launch_export_artifacts_task(
        spec_list=[
            ExportArtifactToDatasetsSpec(
                artifact=DataArtifactADaM,
                dataset_id="69efcdd7ecd36f1f61da97cf",
            ),
            # ExportArtifactToNetAppVolumesSpec(
            #     artifact=DataArtifactADaM,
            #     netapp_volume_id="63ea5468-592f-4d24-8685-c55b2929cf8a",
            #     target_relative_path="mydata",
            # ),
            # ... More exports can be defined in this list, if needed.
        ],
        environment_name="Domino Standard Environment Py3.10 R4.5",
        hardware_tier_id="small-k8s",
        use_project_defaults_for_omitted=True,
    )

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
        model
