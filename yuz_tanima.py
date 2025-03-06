#|pip install deepface
# pip install deepface --no-deps
# pip3 install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.0.0-py3-none-any.whl


from deepface import DeepFace
models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace"]
DeepFace.stream ("dataset", model_name = models[1])