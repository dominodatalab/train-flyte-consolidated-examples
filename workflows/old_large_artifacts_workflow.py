"""
Author(s): ddl-ebrown, ddl-rliu

The workflow returns 100+ artifacts outputs and regular outputs. It does not use the newer train-flyte-library Artifact annotations.
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
DataArtifact0csv = Artifact(name="data0.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0docx = Artifact(name="data0.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0html = Artifact(name="data0.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0pdf = Artifact(name="data0.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0rtf = Artifact(name="data0.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0sas7bdat = Artifact(name="data0.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact0xlsx = Artifact(name="data0.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1csv = Artifact(name="data1.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1docx = Artifact(name="data1.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1html = Artifact(name="data1.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1pdf = Artifact(name="data1.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1rtf = Artifact(name="data1.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1sas7bdat = Artifact(name="data1.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact1xlsx = Artifact(name="data1.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2csv = Artifact(name="data2.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2docx = Artifact(name="data2.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2html = Artifact(name="data2.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2pdf = Artifact(name="data2.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2rtf = Artifact(name="data2.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2sas7bdat = Artifact(name="data2.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact2xlsx = Artifact(name="data2.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3csv = Artifact(name="data3.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3docx = Artifact(name="data3.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3html = Artifact(name="data3.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3pdf = Artifact(name="data3.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3rtf = Artifact(name="data3.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3sas7bdat = Artifact(name="data3.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact3xlsx = Artifact(name="data3.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4csv = Artifact(name="data4.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4docx = Artifact(name="data4.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4html = Artifact(name="data4.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4pdf = Artifact(name="data4.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4rtf = Artifact(name="data4.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4sas7bdat = Artifact(name="data4.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact4xlsx = Artifact(name="data4.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5csv = Artifact(name="data5.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5docx = Artifact(name="data5.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5html = Artifact(name="data5.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5pdf = Artifact(name="data5.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5rtf = Artifact(name="data5.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5sas7bdat = Artifact(name="data5.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact5xlsx = Artifact(name="data5.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6csv = Artifact(name="data6.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6docx = Artifact(name="data6.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6html = Artifact(name="data6.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6pdf = Artifact(name="data6.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6rtf = Artifact(name="data6.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6sas7bdat = Artifact(name="data6.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact6xlsx = Artifact(name="data6.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7csv = Artifact(name="data7.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7docx = Artifact(name="data7.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7html = Artifact(name="data7.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7pdf = Artifact(name="data7.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7rtf = Artifact(name="data7.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7sas7bdat = Artifact(name="data7.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact7xlsx = Artifact(name="data7.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8csv = Artifact(name="data8.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8docx = Artifact(name="data8.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8html = Artifact(name="data8.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8pdf = Artifact(name="data8.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8rtf = Artifact(name="data8.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8sas7bdat = Artifact(name="data8.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact8xlsx = Artifact(name="data8.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9csv = Artifact(name="data9.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9docx = Artifact(name="data9.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9html = Artifact(name="data9.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9pdf = Artifact(name="data9.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9rtf = Artifact(name="data9.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9sas7bdat = Artifact(name="data9.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact9xlsx = Artifact(name="data9.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10csv = Artifact(name="data10.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10docx = Artifact(name="data10.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10html = Artifact(name="data10.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10pdf = Artifact(name="data10.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10rtf = Artifact(name="data10.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10sas7bdat = Artifact(name="data10.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact10xlsx = Artifact(name="data10.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11csv = Artifact(name="data11.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11docx = Artifact(name="data11.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11html = Artifact(name="data11.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11pdf = Artifact(name="data11.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11rtf = Artifact(name="data11.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11sas7bdat = Artifact(name="data11.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact11xlsx = Artifact(name="data11.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12csv = Artifact(name="data12.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12docx = Artifact(name="data12.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12html = Artifact(name="data12.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12pdf = Artifact(name="data12.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12rtf = Artifact(name="data12.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12sas7bdat = Artifact(name="data12.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact12xlsx = Artifact(name="data12.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13csv = Artifact(name="data13.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13docx = Artifact(name="data13.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13html = Artifact(name="data13.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13pdf = Artifact(name="data13.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13rtf = Artifact(name="data13.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13sas7bdat = Artifact(name="data13.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact13xlsx = Artifact(name="data13.xlsx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14csv = Artifact(name="data14.csv", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14docx = Artifact(name="data14.docx", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14html = Artifact(name="data14.html", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14pdf = Artifact(name="data14.pdf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14rtf = Artifact(name="data14.rtf", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14sas7bdat = Artifact(name="data14.sas7bdat", partition_keys=["artifact_type", "artifact_name"])
DataArtifact14xlsx = Artifact(name="data14.xlsx", partition_keys=["artifact_type", "artifact_name"])

@workflow
def wf() -> Tuple[
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact(artifact_type="report", artifact_name="report_foo")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact2(artifact_type="report", artifact_name="report_foo")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact3(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact4(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact5(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("pdf")], ReportArtifact6(artifact_type="report", artifact_name="report_bar")], 
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact0csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact0docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact0html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact0pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact0rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact0sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact0xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact1csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact1docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact1html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact1pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact1rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact1sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact1xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact2csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact2docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact2html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact2pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact2rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact2sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact2xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact3csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact3docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact3html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact3pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact3rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact3sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact3xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact4csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact4docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact4html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact4pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact4rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact4sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact4xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact5csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact5docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact5html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact5pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact5rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact5sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact5xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact6csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact6docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact6html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact6pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact6rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact6sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact6xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact7csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact7docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact7html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact7pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact7rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact7sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact7xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact8csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact8docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact8html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact8pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact8rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact8sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact8xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact9csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact9docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact9html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact9pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact9rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact9sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact9xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact10csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact10docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact10html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact10pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact10rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact10sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact10xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact11csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact11docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact11html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact11pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact11rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact11sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact11xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact12csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact12docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact12html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact12pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact12rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact12sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact12xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact13csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact13docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact13html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact13pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact13rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact13sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact13xlsx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("csv")], DataArtifact14csv(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("docx")], DataArtifact14docx(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("html")], DataArtifact14html(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("pdf")], DataArtifact14pdf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("rtf")], DataArtifact14rtf(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("sas7bdat")], DataArtifact14sas7bdat(artifact_type="data", artifact_name="data_group")],
    Annotated[FlyteFile[TypeVar("xlsx")], DataArtifact14xlsx(artifact_type="data", artifact_name="data_group")],

    # normal workflow output with no annotations
    FlyteFile
    ]: 
    """py
    pyflyte run --remote old_large_artifacts_workflow.py wf
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
            # NOTE: Flyte normally suppports this -- but notice there are no partitions, which make them useless to Domino
            # this output is consumed by a subsequent task but also marked as an artifact
            "processed_data": Annotated[FlyteFile, Artifact(name="processed.sas7bdat", version=str(uuid.uuid4()))],
            # no downstream consumers -- simply an artifact output from an intermediate node in the graph
            "processed_data2": Annotated[FlyteFile, Artifact(name="processed2.sas7bdat", version=str(uuid.uuid4()))],
        },
        use_latest=True,
    )(data_path="/mnt/train-flyte-consolidated-examples/data/data.csv")

    training_results = DominoJobTask(
        name="Train model1 v4",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "data0pdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results2 = DominoJobTask(
        name="Train model2 v4",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "data0pdf": FlyteFile[TypeVar("pdf")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    training_results3 = DominoJobTask(
        name="Train model3 v3",
        domino_job_config=DominoJobConfig(            
            Command="python /mnt/train-flyte-consolidated-examples/data/prep-data.py",
        ),
        inputs={
            "processed_data_in": FlyteFile,
            "epochs": int,
            "batch_size": int,
        },
        outputs={
            "data0csv": FlyteFile[TypeVar("csv")],
            "data0docx": FlyteFile[TypeVar("docx")],
            "data0html": FlyteFile[TypeVar("html")],
            "data0pdf": FlyteFile[TypeVar("pdf")],
            "data0rtf": FlyteFile[TypeVar("rtf")],
            "data0sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data0xlsx": FlyteFile[TypeVar("xlsx")],
            "data1csv": FlyteFile[TypeVar("csv")],
            "data1docx": FlyteFile[TypeVar("docx")],
            "data1html": FlyteFile[TypeVar("html")],
            "data1pdf": FlyteFile[TypeVar("pdf")],
            "data1rtf": FlyteFile[TypeVar("rtf")],
            "data1sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data1xlsx": FlyteFile[TypeVar("xlsx")],
            "data2csv": FlyteFile[TypeVar("csv")],
            "data2docx": FlyteFile[TypeVar("docx")],
            "data2html": FlyteFile[TypeVar("html")],
            "data2pdf": FlyteFile[TypeVar("pdf")],
            "data2rtf": FlyteFile[TypeVar("rtf")],
            "data2sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data2xlsx": FlyteFile[TypeVar("xlsx")],
            "data3csv": FlyteFile[TypeVar("csv")],
            "data3docx": FlyteFile[TypeVar("docx")],
            "data3html": FlyteFile[TypeVar("html")],
            "data3pdf": FlyteFile[TypeVar("pdf")],
            "data3rtf": FlyteFile[TypeVar("rtf")],
            "data3sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data3xlsx": FlyteFile[TypeVar("xlsx")],
            "data4csv": FlyteFile[TypeVar("csv")],
            "data4docx": FlyteFile[TypeVar("docx")],
            "data4html": FlyteFile[TypeVar("html")],
            "data4pdf": FlyteFile[TypeVar("pdf")],
            "data4rtf": FlyteFile[TypeVar("rtf")],
            "data4sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data4xlsx": FlyteFile[TypeVar("xlsx")],
            "data5csv": FlyteFile[TypeVar("csv")],
            "data5docx": FlyteFile[TypeVar("docx")],
            "data5html": FlyteFile[TypeVar("html")],
            "data5pdf": FlyteFile[TypeVar("pdf")],
            "data5rtf": FlyteFile[TypeVar("rtf")],
            "data5sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data5xlsx": FlyteFile[TypeVar("xlsx")],
            "data6csv": FlyteFile[TypeVar("csv")],
            "data6docx": FlyteFile[TypeVar("docx")],
            "data6html": FlyteFile[TypeVar("html")],
            "data6pdf": FlyteFile[TypeVar("pdf")],
            "data6rtf": FlyteFile[TypeVar("rtf")],
            "data6sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data6xlsx": FlyteFile[TypeVar("xlsx")],
            "data7csv": FlyteFile[TypeVar("csv")],
            "data7docx": FlyteFile[TypeVar("docx")],
            "data7html": FlyteFile[TypeVar("html")],
            "data7pdf": FlyteFile[TypeVar("pdf")],
            "data7rtf": FlyteFile[TypeVar("rtf")],
            "data7sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data7xlsx": FlyteFile[TypeVar("xlsx")],
            "data8csv": FlyteFile[TypeVar("csv")],
            "data8docx": FlyteFile[TypeVar("docx")],
            "data8html": FlyteFile[TypeVar("html")],
            "data8pdf": FlyteFile[TypeVar("pdf")],
            "data8rtf": FlyteFile[TypeVar("rtf")],
            "data8sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data8xlsx": FlyteFile[TypeVar("xlsx")],
            "data9csv": FlyteFile[TypeVar("csv")],
            "data9docx": FlyteFile[TypeVar("docx")],
            "data9html": FlyteFile[TypeVar("html")],
            "data9pdf": FlyteFile[TypeVar("pdf")],
            "data9rtf": FlyteFile[TypeVar("rtf")],
            "data9sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data9xlsx": FlyteFile[TypeVar("xlsx")],
            "data10csv": FlyteFile[TypeVar("csv")],
            "data10docx": FlyteFile[TypeVar("docx")],
            "data10html": FlyteFile[TypeVar("html")],
            "data10pdf": FlyteFile[TypeVar("pdf")],
            "data10rtf": FlyteFile[TypeVar("rtf")],
            "data10sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data10xlsx": FlyteFile[TypeVar("xlsx")],
            "data11csv": FlyteFile[TypeVar("csv")],
            "data11docx": FlyteFile[TypeVar("docx")],
            "data11html": FlyteFile[TypeVar("html")],
            "data11pdf": FlyteFile[TypeVar("pdf")],
            "data11rtf": FlyteFile[TypeVar("rtf")],
            "data11sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data11xlsx": FlyteFile[TypeVar("xlsx")],
            "data12csv": FlyteFile[TypeVar("csv")],
            "data12docx": FlyteFile[TypeVar("docx")],
            "data12html": FlyteFile[TypeVar("html")],
            "data12pdf": FlyteFile[TypeVar("pdf")],
            "data12rtf": FlyteFile[TypeVar("rtf")],
            "data12sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data12xlsx": FlyteFile[TypeVar("xlsx")],
            "data13csv": FlyteFile[TypeVar("csv")],
            "data13docx": FlyteFile[TypeVar("docx")],
            "data13html": FlyteFile[TypeVar("html")],
            "data13pdf": FlyteFile[TypeVar("pdf")],
            "data13rtf": FlyteFile[TypeVar("rtf")],
            "data13sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data13xlsx": FlyteFile[TypeVar("xlsx")],
            "data14csv": FlyteFile[TypeVar("csv")],
            "data14docx": FlyteFile[TypeVar("docx")],
            "data14html": FlyteFile[TypeVar("html")],
            "data14pdf": FlyteFile[TypeVar("pdf")],
            "data14rtf": FlyteFile[TypeVar("rtf")],
            "data14sas7bdat": FlyteFile[TypeVar("sas7bdat")],
            "data14xlsx": FlyteFile[TypeVar("xlsx")],
        },
        use_latest=True,
    )(processed_data_in=data_prep_results.processed_data,epochs=10,batch_size=32)

    # return the result from 2nd node to the workflow annotated in different ways
    model = training_results.datapdf
    model2 = training_results2.datapdf
    model3 = training_results3.data0pdf
    return model, model2, model, model, model2, model3, \
        training_results3.data0csv, \
        training_results3.data0docx, \
        training_results3.data0html, \
        training_results3.data0pdf, \
        training_results3.data0rtf, \
        training_results3.data0sas7bdat, \
        training_results3.data0xlsx, \
        training_results3.data1csv, \
        training_results3.data1docx, \
        training_results3.data1html, \
        training_results3.data1pdf, \
        training_results3.data1rtf, \
        training_results3.data1sas7bdat, \
        training_results3.data1xlsx, \
        training_results3.data2csv, \
        training_results3.data2docx, \
        training_results3.data2html, \
        training_results3.data2pdf, \
        training_results3.data2rtf, \
        training_results3.data2sas7bdat, \
        training_results3.data2xlsx, \
        training_results3.data3csv, \
        training_results3.data3docx, \
        training_results3.data3html, \
        training_results3.data3pdf, \
        training_results3.data3rtf, \
        training_results3.data3sas7bdat, \
        training_results3.data3xlsx, \
        training_results3.data4csv, \
        training_results3.data4docx, \
        training_results3.data4html, \
        training_results3.data4pdf, \
        training_results3.data4rtf, \
        training_results3.data4sas7bdat, \
        training_results3.data4xlsx, \
        training_results3.data5csv, \
        training_results3.data5docx, \
        training_results3.data5html, \
        training_results3.data5pdf, \
        training_results3.data5rtf, \
        training_results3.data5sas7bdat, \
        training_results3.data5xlsx, \
        training_results3.data6csv, \
        training_results3.data6docx, \
        training_results3.data6html, \
        training_results3.data6pdf, \
        training_results3.data6rtf, \
        training_results3.data6sas7bdat, \
        training_results3.data6xlsx, \
        training_results3.data7csv, \
        training_results3.data7docx, \
        training_results3.data7html, \
        training_results3.data7pdf, \
        training_results3.data7rtf, \
        training_results3.data7sas7bdat, \
        training_results3.data7xlsx, \
        training_results3.data8csv, \
        training_results3.data8docx, \
        training_results3.data8html, \
        training_results3.data8pdf, \
        training_results3.data8rtf, \
        training_results3.data8sas7bdat, \
        training_results3.data8xlsx, \
        training_results3.data9csv, \
        training_results3.data9docx, \
        training_results3.data9html, \
        training_results3.data9pdf, \
        training_results3.data9rtf, \
        training_results3.data9sas7bdat, \
        training_results3.data9xlsx, \
        training_results3.data10csv, \
        training_results3.data10docx, \
        training_results3.data10html, \
        training_results3.data10pdf, \
        training_results3.data10rtf, \
        training_results3.data10sas7bdat, \
        training_results3.data10xlsx, \
        training_results3.data11csv, \
        training_results3.data11docx, \
        training_results3.data11html, \
        training_results3.data11pdf, \
        training_results3.data11rtf, \
        training_results3.data11sas7bdat, \
        training_results3.data11xlsx, \
        training_results3.data12csv, \
        training_results3.data12docx, \
        training_results3.data12html, \
        training_results3.data12pdf, \
        training_results3.data12rtf, \
        training_results3.data12sas7bdat, \
        training_results3.data12xlsx, \
        training_results3.data13csv, \
        training_results3.data13docx, \
        training_results3.data13html, \
        training_results3.data13pdf, \
        training_results3.data13rtf, \
        training_results3.data13sas7bdat, \
        training_results3.data13xlsx, \
        training_results3.data14csv, \
        training_results3.data14docx, \
        training_results3.data14html, \
        training_results3.data14pdf, \
        training_results3.data14rtf, \
        training_results3.data14sas7bdat, \
        training_results3.data14xlsx, \
        model
