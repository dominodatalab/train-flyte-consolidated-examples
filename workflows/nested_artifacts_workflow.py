"""
Author: ddl-galias

Workflow which calls nested workflows.
"""

from flytekitplugins.domino.artifact import (
    Artifact,
    DATA,
    MODEL,
    REPORT,
)
from flytekitplugins.domino.helpers import DominoJobTask, DominoJobConfig, Input, Output, run_domino_job_task
from flytekit import workflow

DataArtifact = Artifact("data_group", DATA)

# pyflyte run --remote nested_workflow.py echo_nested_wf_one
@workflow
def echo_nested_wf_one():
    data_prep_results = DominoJobTask(    
        name="Prepare data inner1",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            "processed_data": DataArtifact.File(name="inner_processed.csv", type="csv"),
            "processed_data2": DataArtifact.File(name="inner_processed2.csv", type="csv"),
            "processed_data3": DataArtifact.File(name="inner_processed3.csv", type="csv"),
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")
    run_domino_job_task(
        "Echo Nested 1-1", 
        "echo nested1-1",
        use_project_defaults_for_omitted=True
    )
    run_domino_job_task(
        "Echo Nested 1-2", 
        "echo nested1-2",
        use_project_defaults_for_omitted=True
    )


# pyflyte run --remote nested_workflow.py echo_nested_wf_one
@workflow
def echo_nested_wf_one_dupe():
    run_domino_job_task(
        "Echo Nested Dupe1-1", 
        "echo nestedDupe1-1",
        use_project_defaults_for_omitted=True
    )
    run_domino_job_task(
        "Echo Nested Dupe1-2", 
        "echo nestedDupe1-2",
        use_project_defaults_for_omitted=True
    )


# pyflyte run --remote nested_workflow.py echo_nested_wf_two
@workflow
def echo_nested_wf_two():
    data_prep_results = DominoJobTask(    
        name="Prepare data inner2",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            "processed_data": DataArtifact.File(name="inner2_processed.csv", type="csv"),
            "processed_data2": DataArtifact.File(name="inner2_processed2.csv", type="csv"),
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")
    run_domino_job_task(
        "Echo Nested 2-1", 
        "echo nested2-1",
        use_project_defaults_for_omitted=True
    )
    echo_nested_wf_one()
    echo_nested_wf_one_dupe()


# pyflyte run --remote nested_workflow.py nest_user
@workflow
def wf():
    data_prep_results = DominoJobTask(    
        name="Prepare data outer",    
        domino_job_config=DominoJobConfig(
            Command="python /mnt/code/data/prep-data.py",
        ),
        inputs={
            "data_path": str
        },
        outputs={
            "processed_data": DataArtifact.File(name="outer_processed.csv", type="csv"),
        },
        use_latest=True,
    )(data_path="/mnt/code/data/data.csv")
    run_domino_job_task(
        "Echo Nested 3-1", 
        "echo nested3-1",
        use_project_defaults_for_omitted=True
    )
    echo_nested_wf_two()
    return run_domino_job_task(
        "Echo Nested 3-2", 
        "echo nested3-2",
        use_project_defaults_for_omitted=True
    )
