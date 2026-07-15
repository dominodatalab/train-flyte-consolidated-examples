"""
Author: ddl-rliu

The workflow uses some Netapp Volume inputs. It uses the new data configuration UI feature.
"""

import os
from flytekit import workflow
from flytekit.types.file import FlyteFile
from typing import Annotated, TypeVar, NamedTuple, Tuple
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, GitRef, EnvironmentRevisionSpecification, EnvironmentRevisionType, DatasetSnapshot, NetAppVolumeSnapshot
from flytekitplugins.domino.artifact import Artifact, DATA, MODEL, REPORT

# This workflow uses the "data config UI" feature.
# Pre-requisite: A netapp volume in this project with at least two snapshots containing data files.
# (Check this using `ls /mnt/netapp-volumes/snapshots/quick-start/2`)

# Enter the command below to run this Flow.
# VOL_JSON_FIELD='"volumeId": "7e14f077-24b9-4bba-b1c2-c82a57bc3169"'; pyflyte run --remote data_config_ui_workflow.py wf --data_snapshot_reference "{$VOL_JSON_FIELD, \"snapshotVersion\": 1}" --data_snapshot_latest "{$VOL_JSON_FIELD, \"snapshotVersion\": 2}"

@workflow
def wf(data_snapshot_reference: NetAppVolumeSnapshot, data_snapshot_latest: NetAppVolumeSnapshot):
    # generate_task = run_domino_job_task(
    #     flyte_task_name="Generate Data",
    #     command="sleep 300",
    #     inputs=[
    #         Input(name="data_snapshot_reference", type=NetAppVolumeSnapshot, value=data_snapshot_reference)
    #     ],
    #     output_specs=[
    #         Output(name="events", type=FlyteFile["csv"], path="/mnt/netapp-volumes/quick-start/events.csv")
    #     ],
    #     use_project_defaults_for_omitted=True,
    # )
    foo = DominoJobTask(
        name='Generate Data',
        domino_job_config=DominoJobConfig(Command="sleep 300"),
        inputs={'data_snapshot_reference': NetAppVolumeSnapshot},
        outputs={'events': FlyteFile["csv"]},
        use_latest=True
    )
    generate_task = foo(data_snapshot_reference=data_snapshot_reference)

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