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

"""A file system assistant demo using MCP servers.

This example shows how to leverage the filesystem MCP server for local file
operations and the fetch MCP server for downloading online resources. The
assistant will only have access to files under ``ROOT_RESOURCE``.
"""

import os

from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


def init_agent_service():
    llm_cfg = {'model': 'qwen-max'}
    system = (
        '你扮演一个文件系统助手，你具有读取和写入指定目录中文件的能力，'
        '同时能够抓取互联网上的内容'
    )
    tools = [{
        'mcpServers': {
            'filesystem': {
                'command': 'npx',
                'args': ['-y', '@modelcontextprotocol/server-filesystem', ROOT_RESOURCE]
            },
            'fetch': {
                'command': 'uvx',
                'args': ['mcp-server-fetch']
            }
        }
    }]
    bot = Assistant(
        llm=llm_cfg,
        name='文件系统助手',
        description='文件管理',
        system_message=system,
        function_list=tools,
    )

    return bot


def test(query: str = '列出目录中的文件'):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = [{'role': 'user', 'content': query}]
    for response in bot.run(messages):
        print('bot response:', response)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        query = input('user question: ')
        if not query:
            print('user question cannot be empty！')
            continue
        messages.append({'role': 'user', 'content': query})

        response = []
        for resp in bot.run(messages):
            print('bot response:', resp)
        messages.extend(response)


def app_gui():
    # Define the agent
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [
            '列出目录中的文件',
            '读取 doc.pdf 的第一页',
            '抓取 https://www.example.com 的前 100 个字符',
        ]
    }
    WebUI(
        bot,
        chatbot_config=chatbot_config,
    ).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()
