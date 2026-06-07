from roboflow import Roboflow
rf = Roboflow(api_key="a4WbLLErS8EsItbkrBIJ")
project = rf.workspace("evvals-workspace-cf9lw").project("uzaydan_gemi_tespit_sistemi")
version = project.version(1)
dataset = version.download("yolov8")
                