# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from airflowTeamsHook.operator import MSTeamsWebhookOperator

def make_notification(log_url, teams_msg):
    return MSTeamsWebhookOperator(
        task_id="ms_teams_callback",
        trigger_rule="all_done",
        message=teams_msg,
        button_text="View log",
        button_url=log_url,
        theme_color="FF0000",
        http_conn_id='msteams-webhook')

def success_callback(context):
    log_url = context.get('task_instance').log_url
    teams_msg = f"""
            Task has succeeded.
            Task: {context.get('task_instance').task_id}
            Dag: {context.get('task_instance').dag_id}
            Execution Time: {context.get('execution_date')}
            """
    teams_notification = make_notification(log_url, teams_msg)
    return teams_notification.execute(context)

def failure_callback(context):
    log_url = context.get('task_instance').log_url
    teams_msg = f"""
            Task has failed.
            Task: {context.get('task_instance').task_id}
            Dag: {context.get('task_instance').dag_id}
            Execution Time: {context.get('execution_date')}
            """
    teams_notification = make_notification(log_url, teams_msg)
    return teams_notification.execute(context)

def retry_callback(context):
    log_url = context.get('task_instance').log_url
    teams_msg = f"""
            Task is up for retry.
            Task: {context.get('task_instance').task_id}
            Dag: {context.get('task_instance').dag_id}
            Execution Time: {context.get('execution_date')}
            """
    teams_notification = make_notification(log_url, teams_msg)
    return teams_notification.execute(context)
