# sample-low-latency-dash

A sample low-latency DASH environment using FFmpeg.

# Requirements

- FFmpeg
- OBS (Open Broadcaster Software)
	- to feed video to the packager via RTMP
- Python 3

# Run

Go to the repository directory.

```sh
$ cd path_to_sample-low-latency-dash
```

Use venv if you need.

```sh
$ python -m venv .venv
```

Install required Python packages.

```sh
$ pip install -r requirements.txt
```

Run the live packager script in a terminal.

```sh
$ ./package.sh
```

Run the server in another terminal.

```sh
$ python server.py
```

Open OBS and set Settings->Stream->Server to `rtmp://127.0.0.1:1935/live/ll-dash`.

Go to

- [https://reference.dashif.org/dash.js/nightly/samples/dash-if-reference-player/index.html](https://reference.dashif.org/dash.js/nightly/samples/dash-if-reference-player/index.html)

Enter "http://localhost:8000/manifest.mpd" in "Stream" input box and options.  You should at least set Live delay->Initial Live delay to a reasonably small number like `3` to get the most out of your low-latency video streaming.

Then your low-latency DASH video will be played via your webcam.
