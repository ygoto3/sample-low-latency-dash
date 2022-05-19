import os.path
import argparse
import sys
import time
from datetime import datetime as dt
from enum import Enum
from flask import Flask
from flask import Response
from flask_cors import CORS


parser = argparse.ArgumentParser()
parser.add_argument("--port", help="specify a port number", type=int, default=8000)
args = parser.parse_args()

class SegmentStatus(Enum):
    ENCODING = 1
    ENCODED = 2
    NOT_FOUND = 3


def segment_status(filepath: str) -> SegmentStatus: 
    growing_filepath = get_growing_segment_filepath(filepath)
    if os.path.exists(growing_filepath):
        return SegmentStatus.ENCODING
    elif os.path.exists(filepath):
        return SegmentStatus.ENCODED
    else:
        return SegmentStatus.NOT_FOUND
        

def get_growing_segment_filepath(filepath: str) -> str:
    return "{}.tmp".format(filepath)


def growing_segment(filepath: str) -> bytes:
    growing_filepath = get_growing_segment_filepath(filepath)

    try:
        last_timestamp = os.stat(growing_filepath).st_mtime
    except Exception as e:
        print(e.message)
        return

    with open(growing_filepath, "rb") as f:
        data = f.read()
        yield data

    last_size = len(data)
    encoded = False
    
    while not encoded:
        if os.path.exists(growing_filepath):
            stat = os.stat(growing_filepath)
            timestamp = stat.st_mtime
            if dt.fromtimestamp(last_timestamp) != dt.fromtimestamp(timestamp):
                with open(growing_filepath, "rb") as f:
                    f.seek(last_size)
                    data = f.read()
                    last_size += len(data)
                yield data
        elif os.path.exists(filepath):
            encoded = True
            with open(filepath, "rb") as f:
                f.seek(last_size)
                data = f.read()
            yield data
        if not encoded:
            time.sleep(0.1)


app = Flask(__name__, static_folder='./package', static_url_path='')
CORS(app, supports_credentials=True)
# app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/<representation_id>/<segment>')
def get_segment(representation_id: str, segment: str) -> Response:

    if representation_id != "0" and representation_id != "1" and representation_id != "2":
        return Response("NOT FOUND"), 404

    filepath = os.path.abspath('./package/{}/{}'.format(representation_id, segment))
    status = segment_status(filepath)

    if status == SegmentStatus.ENCODING:
        return Response(growing_segment(filepath))
    elif status == SegmentStatus.ENCODED:
        with open(filepath, "rb") as f:
            data = f.read()
        return Response(data)
    else:
        return Response("NOT FOUND"), 404


if __name__ == "__main__":
    sys.exit(app.run(port=args.port))
