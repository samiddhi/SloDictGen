from utils.json_utils import read_json, extend_json_array
from utils.sqlite_utils import sskj_entries_db
from common.imports import *

import sqlite3
import tqdm

conn = sqlite3.connect(sskj_entries_db)
cursor = conn.cursor()

cursor.execute("SELECT id FROM sskj_entries")
ids: List = [row[0] for row in cursor.fetchall()]

# path declarations
trans_dir = os.path.abspath(os.path.join(
    proj_dir, 'data', 'translations'))
mac_trans_dir = os.path.abspath(os.path.join(
    trans_dir, 'mac_station'))
win_trans_dir = os.path.abspath(os.path.join(
    trans_dir, 'win_station'))
merged_trans_dir = os.path.abspath(os.path.join(
    trans_dir, 'merged_station'))

for filename in ['insoluble.json', 'std_log.json', 'translated_en.json']:
    win_path = os.path.abspath(os.path.join(
        win_trans_dir, filename))
    mac_path = os.path.abspath(os.path.join(
        mac_trans_dir, filename))
    merged_path = os.path.abspath(os.path.join(
        merged_trans_dir, filename))

    win: List = read_json(win_path)
    mac: List = read_json(mac_path)
    mac.reverse()
    merge = win+mac

    extend_json_array(merged_path, merge)
