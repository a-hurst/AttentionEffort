# AttentionEffort

AttentionEffort is the experiment program for a study exploring how reported effort to stay on-task during a simple attention task relates to reports of intentional and unintentional mind-wandering. Specifically, the study is interested in how often participants report intentional mind-wandering while also reporting a non-zero level of effort to stay on-task.

![Task animation](attention_effort.gif)

## Requirements

AttentionEffort is programmed in Python 3.7 (likely backwards-compatible with 3.5+) using the [KLibs framework](https://github.com/a-hurst/klibs). It has been developed and tested on macOS and Windows 10, but should also work on [Ubuntu](https://www.ubuntu.com/download/desktop) or [Debian](https://www.debian.org/distrib/) Linux with minimal effort provided that SDL2, SDL2\_ttf, and SDL2\_mixer are installed.

## Getting Started

### Installation

First, you will need to install the KLibs framework by following the instructions [here](https://github.com/a-hurst/klibs).

Then, you can then download and install the experiment program with the following commands (replacing `~/Downloads` with the path to the folder where you would like to put the program folder):

```bash
cd ~/Downloads
git clone https://github.com/a-hurst/AttentionEffort.git
```

You can also install and run the experiment in a self-contained Python virtual environment using [Pipenv](https://pipenv.kennethreitz.org/en/latest/), by installing Pipenv and then running `pipenv install` within the experiment folder. You can then run KLibs within the virtual environment by prefixing all commands with `pipenv run` (e.g. `pipenv run klibs export`).


### Running the Experiment

AttentionEffort is a KLibs experiment, meaning that it is run using the `klibs` command at the terminal (running the 'experiment.py' file using Python directly will not work).

To run the experiment, navigate to the AttentionEffort folder in a terminal window and run `klibs run [screensize]`,
replacing `[screensize]` with the diagonal size of your display in inches (e.g. `klibs run 24` for a 24-inch monitor). If you just want to test the program out for yourself and skip demographics collection, you can add the `-d` flag to the end of the command to launch the experiment in development mode.


### Exporting Data

To export data from AttentionEffort, simply run 

```
klibs export
```

while in the AttentionEffort directory. This will export the trial data for each participant into individual tab-separated text files in the project's `ExpAssets/Data` subfolder.
