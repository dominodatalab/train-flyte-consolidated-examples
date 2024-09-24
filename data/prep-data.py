import os
import shutil

try:
    named_output = "model"
    os.makedirs("/workflow/outputs/{}".format(named_output), exist_ok=True)
except:
    pass

for named_output in ["processed_data"] + [f"processed_data{i}" for i in range(2, 10)]:
    try:
        with open("/workflow/outputs/{}".format(named_output), "w") as f:
            f.write("a,b,c\n1,2,3")
    except:
        pass

for ext in ["csv", "docx", "html", "pdf", "rtf", "sas7bdat", "xlsx"]:
    try:
        with open("/workflow/outputs/data{}".format(ext), "wb") as f:
            with open("/mnt/train-flyte-consolidated-examples/data/data.{}".format(ext), "rb") as src:
                shutil.copyfileobj(src, f)
    except:
        pass