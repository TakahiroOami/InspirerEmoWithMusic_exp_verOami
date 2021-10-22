from BioDataRecorder import BioDataRecorder
from EvaluationRecorder import EvaluationRecorder
import eel
from logging import getLogger, Formatter, NullHandler, StreamHandler, FileHandler, DEBUG
import sys
import csv
import datetime
import os

#logger's setting
logger = getLogger(__name__)
logging_format = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s "
fm = Formatter(logging_format)
sh = StreamHandler()
sh.setFormatter(fm)
sh.setLevel(DEBUG)
logger.addHandler(sh)
fh = FileHandler("log.txt", "w", encoding="utf-8")
fh.setFormatter(fm)
fh.setLevel(DEBUG)
logger.addHandler(fh)
logger.setLevel(DEBUG)
logger.propagate = False

#create and setup recorder
recorder = BioDataRecorder()
recorder.read_config("configs/exp_recorder_config.json")
recorder.set_dafault()
logger.debug(f"create recorder")

#evaluation recorder
now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d_%H%M%S')
eva_recorder = EvaluationRecorder(file_name="evaluation_data/" + now + "_eva_exp.csv")
logger.debug(f"create evaluation recorder")

#stimulation labels
DEFAULT = -3
EVALUATION = -2
REST = -1
FIRST_REST = 0
FIRST_EMO = 1
SECOND_EMO = 2
THIRD_EMO = 3
FORTH_EMO = 4
TEST_01 = 5
TEST_02 = 6
ACTUAL_PLAY = 7
recorder.set_stimu_num(DEFAULT)
logger.debug(f"recorder.set_stimu_num is called({DEFAULT})")

STIMULATION = ACTUAL_PLAY #change point

'''
FIRST_REST_TIME = 100
REST_TIME = 30
STIMU_TIME = 45
'''

FIRST_REST_TIME = 1
REST_TIME = 1
STIMU_TIME = 1

#set stimulations
'''
fp = open("stimu_database.csv", "r", encoding="utf-8", newline="")
dict_reader = csv.DictReader(fp)
stimu_list = list()
for row in dict_reader:
    stimu_list.append(row)
'''

stimu_list = None
'''
if STIMULATION == COMFORTABLE:
    stimu_list = ["w.mp3", "023.mp3", "w.mp3", "105.mp3", "w.mp3", "021.mp3","w.mp3","024.mp3","w.mp3","028.mp3","w.mp3","027.mp3"]
if STIMULATION == UNCOMFORTABLE:
    stimu_list = ["w.mp3", "070.mp3", "w.mp3", "014.mp3", "w.mp3", "015.mp3","w.mp3","069.mp3","w.mp3","011.mp3","w.mp3","010.mp3"]
'''
'''
if STIMULATION == FIRST_EMO:
    stimu_list = ["w.mp3", "022.mp3", "w.mp3", "072.mp3",
                  "w.mp3", "023.mp3", "w.mp3", "024.mp3"]
if STIMULATION == SECOND_EMO:
    stimu_list = ["w.mp3", "015.mp3", "w.mp3", "068.mp3",
                  "w.mp3", "014.mp3", "w.mp3", "011.mp3"]
if STIMULATION == THIRD_EMO:
    stimu_list = ["w.mp3", "081.mp3", "w.mp3", "031.mp3",
                  "w.mp3", "109.mp3", "w.mp3", "033.mp3"]
if STIMULATION == FORTH_EMO:
    stimu_list = ["w.mp3", "107.mp3", "w.mp3", "042.mp3",
                  "w.mp3", "106.mp3", "w.mp3", "041.mp3"]
'''
if STIMULATION == TEST_01:
    stimu_list = ["w02.mp3", "033.mp3", "w02.mp3", "011.mp3", "w02.mp3", "041.mp3", "w02.mp3", "024.mp3"]
    FIRST_REST_TIME = 15
    REST_TIME = 15
    STIMU_TIME = 15

if STIMULATION == TEST_02:
    stimu_list = ["w.mp3", "033.mp3", "w.mp3", "011.mp3",
                  "w.mp3", "041.mp3", "w.mp3", "024.mp3", "w.mp3", "024.mp3", "w.mp3", "041.mp3", "w.mp3", "011.mp3", "w.mp3", "033.mp3"]
    FIRST_REST_TIME = 180
    REST_TIME = 180
    STIMU_TIME = 60

#3,2,4,1,1,4,2,3象限の順番
if STIMULATION == ACTUAL_PLAY:
    stimu_list = ["w02.mp3", "Classic2.mp3", "w02.mp3", "J-POP2.mp3","w02.mp3", "Jazz2.mp3", "w02.mp3", "ROCK2.mp3","w02.mp3","anounce.wav"] #change point
    FIRST_REST_TIME = 60 #change point
    REST_TIME = 60 #change point
    STIMU_TIME = 60 #change point

logger.debug(f"FIRST_REST_TIME:{FIRST_REST_TIME}")
logger.debug(f"REST_TIME:{REST_TIME}")
logger.debug(f"STIMU_TIME:{STIMU_TIME}")

current_stimu_file_path = "default"
stimu_list_index = 0
stimu_file_dir = "music_dir"

#set html's turn
html_page_list = list()
html_page_list.append("SD.html") 
for i in range(len(stimu_list)):
    html_page_list.append("music_stimulation.html")
    if i % 2 != 1:
        pass
    else:
        html_page_list.append("SAM_evaluation.html") #change point
html_page_list.append("finish.html")
html_page_list_index = 0

logger.debug(f"html_page_list:\n {html_page_list}")


@eel.expose
def py_get_stimu_file_path():
    global current_stimu_file_path
    global stimu_file_dir
    global stimu_list_index

    current_stimu_file_path = stimu_file_dir + \
        "/" + stimu_list[stimu_list_index]
    logger.debug(f"get file path:{current_stimu_file_path}")
    return current_stimu_file_path


@eel.expose
def py_notice_finished_stimu():
    global current_stimu_file_path
    global stimu_list_index
    global recorder

    recorder.set_stimu_num(DEFAULT)
    logger.debug(f"recorder.set_stimu_num is called({DEFAULT})")
    logger.debug(f"notice finished stimu:{current_stimu_file_path}")


@eel.expose
def py_notice_started_stimu():
    global current_stimu_file_path
    global stimu_list_index
    global stimu_list_index

    if stimu_list_index == 0:
        recorder.set_stimu_num(FIRST_REST)
        logger.debug(f"recorder.set_stimu_num is called({FIRST_REST})")
    elif stimu_list_index % 2 == 0:
        recorder.set_stimu_num(REST)
        logger.debug(f"recorder.set_stimu_num is called({REST})")
    else:
        recorder.set_stimu_num(stimu_list_index)
        logger.debug(f"recorder.set_stimu_num is called({stimu_list_index})")

    stimu_list_index = stimu_list_index + 1
    logger.debug(f"notice started stimu:{current_stimu_file_path}")


@eel.expose
def py_get_next_page():
    global html_page_list_index
    global recorder

    next_page = html_page_list[html_page_list_index]
    html_page_list_index = html_page_list_index + 1

    if next_page == "SAM_evaluation.html":
        recorder.set_stimu_num(EVALUATION)
        logger.debug(f"recorder.set_stimu_num is called({EVALUATION})")

    logger.debug(f"get next page:{next_page}")
    return next_page


@eel.expose
def py_get_stimu_time():

    stimu_time = None
    if stimu_list_index == 0:
        stimu_time = FIRST_REST_TIME
    elif stimu_list_index % 2 == 0:
        stimu_time = REST_TIME
    else:
        stimu_time = STIMU_TIME

    logger.debug(f"set stimu time:{stimu_time}")
    return stimu_time


@eel.expose
def py_send_evaluation(evaluation_json):
    global stimu_list_index
    global eva_recorder
    global recorder

    valence = evaluation_json["valence"]
    arousal = evaluation_json["arousal"]
    eva_recorder.save_evaluation(stimu_list_index-1, valence, arousal)
    logger.debug(f"send evaluation:{evaluation_json}")

    recorder.set_stimu_num(DEFAULT)
    logger.debug(f"recorder.set_stimu_num is called({DEFAULT})")

    #return evaluation_json


@eel.expose
def py_exit_system():
    logger.debug(f"exit python")

    '''
    import pyautogui
    import win32gui
    #click close button
    try:
        parent_handle = win32gui.FindWindow(None, "finish__542054245")
        left_up_x, left_up_y, right_down_x, right_down_y = win32gui.GetWindowRect(
            parent_handle)
        pyautogui.click(right_down_x - 13, left_up_y + 5)
    except Exception:
        logger.error(f"error is occured on py_exit_system")
    '''

if __name__ == "__main__":

    recorder.start()
    eel.init("web")
    eel.start("start.html", block=False)

    try:
        while True:
            eel.sleep(1)
            #logger.debug("running")

            current_data = recorder.get_current_data_from_parent_process()
            #print(f"current_data:{ins.get_current_data_from_parent_process()}")
            if current_data:
                print(
                    f"poor_signal:{current_data['poor_signal']}, attention:{ current_data['attention'] }, IBI:{current_data['IBI']}, BPM:{current_data['BPM']}, pNN50:{current_data['pNN50']},LF:{current_data['LF']}, HF:{current_data['HF']}")
            else :
                print('no data')

    except KeyboardInterrupt:
        logger.debug("ctrl+c")
    except Exception:
        logger.debug("unexpected error is occured", exc_info=True)
        
    finally:
        recorder.stop()
