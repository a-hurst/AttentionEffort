### Klibs Parameter overrides ###

#########################################
# Runtime Settings
#########################################
collect_demographics = True
manual_demographics_collection = False
manual_trial_generation = False
run_practice_blocks = True
multi_user = True
view_distance = 57 # in centimeters, 57cm = 1 deg of visual angle per cm of screen

#########################################
# Available Hardware
#########################################
eye_tracker_available = False
eye_tracking = False

#########################################
# Environment Aesthetic Defaults
#########################################
default_fill_color = (65, 65, 65, 255)
default_color = (255, 255, 255, 255)
default_font_size = 0.6
default_font_unit = 'deg'
default_font_name = 'Hind-Medium'

#########################################
# EyeLink Settings
#########################################
manual_eyelink_setup = False
manual_eyelink_recording = False

saccadic_velocity_threshold = 20
saccadic_acceleration_threshold = 5000
saccadic_motion_threshold = 0.15

#########################################
# Experiment Structure
#########################################
multi_session_project = False
trials_per_block = 9
blocks_per_experiment = 132
table_defaults = {}
conditions = []
default_condition = None

#########################################
# Development Mode Settings
#########################################
dm_auto_threshold = True
dm_trial_show_mouse = False
dm_ignore_local_overrides = False
dm_show_gaze_dot = True

#########################################
# Data Export Settings
#########################################
primary_table = "trials"
unique_identifier = "userhash"
exclude_data_cols = ["created"]
append_info_cols = ["random_seed"]
datafile_ext = ".txt"

#########################################
# PROJECT-SPECIFIC VARS
#########################################
stim_duration = 250 # ms
trial_duration = 1150 # ms
target = 3

# trials_per_block should be a multiple of probe_span + noprobe_span
probe_span = 48 # 48 now
noprobe_span = 18 # minimum trials between probes

#########################################
# Thought Probe Settings
#########################################
probe_question = "Were you performing the task attentively just now?"
probe_responses = {
    'attending': "Yes, I was focused on performing the task.",
    'unintentional_mw': "No, my thoughts had unintentionally wandered from the task.",
    'intentional_mw': "No, I was intentionally thinking about other things.",
    'distracted': "No, I was distracted by something else around me.",
    'blanking': "No, my mind had gone temporarily blank."
}
probe_order = ['attending', 'unintentional_mw', 'intentional_mw', 'distracted', 'blanking']
