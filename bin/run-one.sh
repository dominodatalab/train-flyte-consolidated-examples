TFCE_LOG="flyte-workflows.log"
echo "" > $TFCE_LOG

TFCE_WORKFLOWS="./train-flyte-consolidated-examples/workflows"
TFCE_RUN="pyflyte run --remote"
$TFCE_RUN $TFCE_WORKFLOWS/invalid_wf_level_artifacts_workflow.py wf &>> $TFCE_LOG
$TFCE_RUN $TFCE_WORKFLOWS/invalid_task_level_artifacts_workflow.py wf &>> $TFCE_LOG
# $TFCE_RUN $TFCE_WORKFLOWS/artifacts_workflow.py wf &>> $TFCE_LOG
# $TFCE_RUN $TFCE_WORKFLOWS/old_artifacts_workflow.py wf &>> $TFCE_LOG