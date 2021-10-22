from BioDataRecorder import BioDataRecorder
from EvaluationRecorder import EvaluationRecorder
import eel
from logging import getLogger, Formatter, NullHandler, StreamHandler, FileHandler, DEBUG
import sys
import csv

#logger's setting
logger = getLogger(__name__)
#logging_format = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s "
logging_format = "%(asctime)s - %(message)s"
fm = Formatter(logging_format)
sh = StreamHandler()
sh.setFormatter(fm)
sh.setLevel(DEBUG)
logger.addHandler(sh)
'''
fh = FileHandler("log.txt", "w", encoding="utf-8")
fh.setFormatter(fm)
fh.setLevel(DEBUG)
logger.addHandler(fh)
'''
logger.setLevel(DEBUG)
logger.propagate = False

#create and setup recorder
recorder = BioDataRecorder()
recorder.read_config("configs/pre_exp_recorder_config.json")
recorder.set_dafault()
logger.debug(f"create recorder")


if __name__ == "__main__":

    recorder.start()

    try:
        while True:
            eel.sleep(1)
            #logger.debug("running")

            current_data = recorder.get_current_data_from_parent_process()
            #print(f"current_data:{ins.get_current_data_from_parent_process()}")
            if current_data:
                logger.debug(
                    f"poor_signal:{current_data['poor_signal']}, attention:{ current_data['attention'] }, IBI:{current_data['IBI']}, BPM:{current_data['BPM']}, pNN50:{current_data['pNN50']},LF:{current_data['LF']}, HF:{current_data['HF']}")
            else:
                logger.debug(f'no data')

    except KeyboardInterrupt:
        logger.debug("ctrl+c")
    except Exception:
        logger.debug("unexpected error is occured", exc_info=True)
    finally:
        recorder.stop()
