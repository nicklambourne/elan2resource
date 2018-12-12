import logging, logging.handlers
import os
import pydub
import sys
from pathlib import Path
from PyQt5.QtCore import QSettings
from datatypes import AppSettings, AUDIO_QUALITY, AUDIO_QUALITY_REV, OutputMode, OUTPUT_MODE_NAMES


def get_settings() -> QSettings:
    return QSettings('CoEDL', 'Language Resource Creator')


def system_settings_exist() -> bool:
    if os.path.exists(get_settings().fileName()):
        LOG_SETTINGS.debug(f"System settings @ {get_settings().fileName()}")
        return True
    else:
        return False


def print_system_settings() -> None:
    system_settings = get_settings()
    print(f'Audio Quality: {system_settings.value("Audio Quality")}\n'
          f'Output Format: {OUTPUT_MODE_NAMES[system_settings.value("Output Format")]}\n'
          f'Microphone: {system_settings.value("Microphone")}\n'
          f'Projects Directory: {system_settings.value("Project Root Dir")}'
          )


def load_system_settings() -> AppSettings:
    app_settings = AppSettings()
    system_settings = get_settings()
    app_settings.audio_quality = AUDIO_QUALITY[system_settings.value('Audio Quality')]
    app_settings.output_format = list(OutputMode)[int(system_settings.value('Output Format'))]
    app_settings.microphone = system_settings.value('Microphone')
    app_settings.project_root_dir = system_settings.value('Project Root Dir')
    if system_settings.contains('FFMPEG Location'):
        location = system_settings.value('FFMPEG Location')
        if location == 'None':
            app_settings.ffmpeg_location = None
        else:
            # Test if exists?
            app_settings.ffmpeg_location = location
    return app_settings


def save_system_settings(app_settings: AppSettings) -> None:
    system_settings = get_settings()
    system_settings.setValue('Audio Quality', AUDIO_QUALITY_REV[app_settings.audio_quality])
    system_settings.setValue('Output Format', app_settings.output_format.value)
    system_settings.setValue('Microphone', app_settings.microphone)
    system_settings.setValue('FFMPEG Location', str(app_settings.ffmpeg_location))
    system_settings.setValue('Project Root Dir', str(app_settings.project_root_dir))
    system_settings.sync()
    print_system_settings()


def set_ffmpeg_location(app_settings: AppSettings, path: str) -> None:
    app_settings.ffmpeg_location = path
    save_system_settings(app_settings)
    pydub.AudioSegment.converter = path


def setup_custom_logger(name):
    app_settings = AppSettings()
    log_path = Path(app_settings.default_project_dir).parent
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_name = os.path.join(log_path, "log_hermes.log")
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-s [%(name)-s] '
                                      '%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.handlers.TimedRotatingFileHandler(log_name, when="d", interval=1, backupCount=90)
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger


LOG_SETTINGS = setup_custom_logger("SettingsUtil")
