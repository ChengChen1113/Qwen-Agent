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

"""A filesystem assistant implemented with MCP."""

import os
from typing import Optional

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

ROOT_DIR = os.path.join(os.path.dirname(__file__), 'workspace_filesystem')
os.makedirs(ROOT_DIR, exist_ok=True)


def init_agent_service():
    llm_cfg = {'model': 'qwen-max'}
    system = '你是一个文件系统助手，能够读取和写入文件。'
    tools = [{
        'mcpServers': {
            'filesystem': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-filesystem', ROOT_DIR]
            }
        }
    }]
    bot = Assistant(
        llm=llm_cfg,
        name='文件系统助手',
        description='管理文件',
        system_message=system,
        function_list=tools,
    )
    return bot


def test(query: str = '在当前目录创建一个dd.txt文件，内容为hello', file: Optional[str] = None):
    bot = init_agent_service()
    messages = []
    if not file:
        messages.append({'role': 'user', 'content': query})
    else:
        messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})
    for response in bot.run(messages):
        print('bot response:', response)


if __name__ == '__main__':
    test()
