from util import query_vision, download_file, upload_file
import json
import numpy as np
from PIL import Image


def segment(img_path):
    download_file(img_path)
    nparr = np.asarray(Image.open("temp.jpg"))
    resp = json.loads(query_vision("temp.jpg"))

    print(resp)

    items = {"Pants", "Outerwear", "Shoe", "Shirt", "Clothing", "Top"}

    current_items = set()
    for objs in resp["responses"][0]["localizedObjectAnnotations"]:
        if objs["name"] in items and objs["score"] > 0.5 and objs["name"] not in current_items:
            current_items.add(objs["name"])
            vertices = objs["boundingPoly"]["normalizedVertices"]
            tl, br = vertices[0], vertices[2]
            x_size, y_size = nparr.shape[0], nparr.shape[1]

            x1, x2 = int(tl["y"] * x_size), int(br["y"] * x_size)
            y1, y2 = int(tl["x"] * y_size), int(br["x"] * y_size)
            cropped_im = nparr[x1: x2, y1: y2, :]

            fname = objs["name"] + ".jpg"
            Image.fromarray(cropped_im).save(fname)
            upload_file(fname, "segments/"+fname)


def lambda_handler(event, context):
    image_path = event["path"]
    segment(image_path)


lambda_handler({"path":"test.jpg"}, None)
