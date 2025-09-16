from multiprocessing import context
import sys
import os
import requests

from TmsCaseManager.utils.common.api_helper import *
from TmsCaseManager.utils.common.login_helper import *
from TmsCaseManager.utils.common.api_helper import ApiHelper
import json
from TmsCaseManager.utils.common.AlertGeneration import AlertGeneration

from behave import *


ENV_NAME = ApiHelper._load_env_name()
@given("Alert Queue Module - User Logged in TmsCaseManager")
def step_implementAlertQueue1(context):
    context.token = loginHelper.TMS_CaseManagerLogin()
    assert context.token is not None, "Login token is None"

@when('Alert Queue Module - User Generates Alerts for a Team')
def step_implementAlertQueue2(context):
    context.api = ApiHelper(ENV_NAME)   
    payload = context.api.get_Payload("casemanager", "transactionscreening")
    AlertGeneration.generate_Alerts(payload)
