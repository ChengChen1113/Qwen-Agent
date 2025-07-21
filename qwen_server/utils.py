# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
import os
from pathlib import Path

from qwen_agent.utils.utils import get_basename_from_url
from qwen_server.schema import GlobalConfig


def load_config(config_path: str | Path | None = None) -> GlobalConfig:
    """Load ``server_config.json`` and return a :class:`GlobalConfig` instance."""
    if config_path is None:
        config_path = Path(__file__).resolve().parent / 'server_config.json'
    else:
        config_path = Path(config_path)

    with open(config_path, 'r') as f:
        cfg = json.load(f)
        cfg = GlobalConfig(**cfg)

    return cfg


def get_llm_config(cfg: GlobalConfig) -> dict | None:
    """Extract the LLM related configuration from ``cfg`` if available."""
    if hasattr(cfg.server, 'llm'):
        return {
            'model': cfg.server.llm,
            'api_key': cfg.server.api_key,
            'model_server': cfg.server.model_server,
        }
    return None


def save_browsing_meta_data(url: str, title: str, meta_file: str):
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as file:
            meta_info = json.load(file)
    else:
        meta_info = {}
    now_time = str(datetime.date.today())
    meta_info[url] = {
        'url': url,
        'time': now_time,
        'title': title,
        'checked': True,
    }

    with open(meta_file, 'w', encoding='utf-8') as file:
        json.dump(meta_info, file, indent=4)


def rm_browsing_meta_data(url: str, meta_file: str):
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as file:
            meta_info = json.load(file)
    else:
        meta_info = {}

    if url in meta_info:
        meta_info.pop(url)
        with open(meta_file, 'w', encoding='utf-8') as file:
            json.dump(meta_info, file, indent=4)


def read_meta_data_by_condition(meta_file: str, **kwargs):
    if os.path.exists(meta_file):
        with open(meta_file, 'r', encoding='utf-8') as file:
            meta_info = json.load(file)
    else:
        meta_info = {}
        return []

    if 'url' in kwargs:
        if kwargs['url'] in meta_info:
            return meta_info[kwargs['url']]
        else:
            return ''

    records = meta_info.values()

    if 'time_limit' in kwargs:
        filter_records = []
        for x in records:
            if kwargs['time_limit'][0] <= x['time'] <= kwargs['time_limit'][1]:
                filter_records.append(x)
        records = filter_records
    if 'checked' in kwargs:
        filter_records = []
        for x in records:
            if x['checked']:
                filter_records.append(x)
        records = filter_records

    return records


def save_history(history, url, history_dir):
    history = history or []
    history_file = os.path.join(history_dir, get_basename_from_url(url) + '.json')
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)


def read_history(url, history_dir):
    history_file = os.path.join(history_dir, get_basename_from_url(url) + '.json')
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data:
                return data
            else:
                return []
    return []
