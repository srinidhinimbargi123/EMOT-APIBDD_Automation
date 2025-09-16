from multiprocessing import context
import sys
import os
import requests
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from TmsCaseManager.utils.common.api_helper import *
from TmsCaseManager.utils.common.login_helper import *
from TmsCaseManager.utils.common.api_helper import ApiHelper
import json

from behave import *



ENV_NAME = ApiHelper._load_env_name()
@given("the user is logged in to TMS-CaseManager")
def step_impl1(context): 
    context.token = loginHelper.TMS_CaseManagerLogin()
    assert context.token is not None, "Login token is None"

@when('the user navigates to the Common Queue')
def step_impl2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    endpoint = context.api.get_EndPoints("casemanager", "commonQueuealerts")
    payload = context.api.get_Payload("casemanager", "alertfilter")

    context.response = context.api.TestApi("POST", context.token, endpoint, payload=payload)

@then("the system should display all alerts with Alert ID and Transaction Type")
def step_impl3(context):
    ApiHelper.validateStatusCode(context.response, 200)
    json_data = context.response.json()
    assert "results" in json_data or "data" in json_data, "Response does not contain results"
    ApiHelper.print_response(context.response)

@then("Investigate one of the case")
def step_impl4(context):
    api = ApiHelper(ENV_NAME)
    # updated_endpoint=context.api.update_Endpoint("investigatecase","16564","16550")
    # payload = context.api.get_Payload("casemanager", "investigatecase")
    endpoint = context.api.get_EndPoints("casemanager", "commonqueuecases")
    context.response =api.TestApi("get",context.token,endpoint)
    ApiHelper.validateStatusCode(context.response, 300)
    ApiHelper.print_response(context.response)
    context.api.output_Payload_Assert(context.response,"alerts") 
    
    



