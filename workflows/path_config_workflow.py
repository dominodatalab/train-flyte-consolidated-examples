"""
Author: ddl-rliu

The workflow uses some regular inputs and outputs. It uses the new path configuration feature.
"""

import os
from flytekit import workflow
from flytekit.types.file import FlyteFile
from typing import Annotated, TypeVar, NamedTuple, Tuple
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot, NetAppVolumeSnapshot
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT

# Default for caching, set to True or False
cache = False

# Enter the command below to run this Flow.
# pyflyte run --remote path_config_workflow.py wf

@workflow
def wf():
    generate_task = run_domino_job_task(
        flyte_task_name="Generate Data",
        command="python3 /mnt/code/scripts/generate_events.py",
        inputs=[
        ],
        output_specs=[
            Output(name="events", type=FlyteFile["csv"], path="/mnt/netapp-volumes/quick-start/events.csv")
        ],
        use_project_defaults_for_omitted=True,
    )

    process_task = run_domino_job_task(
        flyte_task_name="Process Data",
        command="python3 /mnt/code/scripts/process_events.py",
        inputs=[
            Input(name="events", type=FlyteFile["csv"], path="/mnt/netapp-volumes/quick-start/events.csv", value=generate_task["events"])
        ],
        output_specs=[
            Output(name="counts", type=FlyteFile["csv"], path="/mnt/netapp-volumes/quick-start/event_counts.csv")
        ],
        use_project_defaults_for_omitted=True,
    )

    report_task = run_domino_job_task(
        flyte_task_name="Make Report",
        command="python3 /mnt/code/scripts/make_events_report.py",
        inputs=[
            Input(name="counts", type=FlyteFile["csv"], path="/mnt/netapp-volumes/quick-start/event_counts.csv", value=process_task["data"])
        ],
        output_specs=[
            Output(name="report", type=FlyteFile["png"], path="/mnt/netapp-volumes/quick-start/event_report.png")
        ],
        use_project_defaults_for_omitted=True,
    )

    return