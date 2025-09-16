from multiprocessing import context
import sys
import os
import requests
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from TmsCaseManager.utils.common import TeamCreation
from TmsCaseManager.utils.common.ScenarioCreation import ScenarioCreation
from TmsCaseManager.utils.common.api_helper import *
from TmsCaseManager.utils.common.login_helper import *
from TmsCaseManager.utils.common.api_helper import ApiHelper
import json

from behave import *


caseManagerRole=None
tmsRole=None
TeamID=None
ScenarioID=None

ENV_NAME = ApiHelper._load_env_name()
@given("the user is logged in to TMS-CaseManager1")
def step_impls1(context): 
    context.token = loginHelper.TMS_CaseManagerLogin()
    assert context.token is not None, "Login token is None"

@when('the user creates the role and assign to the user')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    payload = context.api.get_Payload("casemanager", "casemanagerolecreationdev")
    team1 = TeamCreation.TeamCreation(ENV_NAME)
    context.response = team1.role_Create(payload, context.token)
    context.caseManagerRole=context.api.extract_data_from_response(context.response,"id")
    # print("Role ID:", caseManagerRole)
    print(context.response)
    payload3 = context.api.get_Payload("casemanager", "tmsrolecreationdev")
    context.response1 = team1.role_Create(payload3, context.token)
    context.tmsRole=context.api.extract_data_from_response(context.response1,"id")
    # print("Role ID:", tmsRole)
    print(context.response1)

@when('assign role to the user')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    payload1 = context.api.get_Payload("casemanager", "roleassignment")
    updatedpayload=context.api.update_key_in_payload(payload1,"role_ids",[context.caseManagerRole])
    print(updatedpayload)
    team1 = TeamCreation.TeamCreation(ENV_NAME)
    context.response2 = team1.role_Assign(updatedpayload, context.token)
    print(context.response2)
    payload2 = context.api.get_Payload("casemanager", "roleassignment")
    updatedpayload1=context.api.update_key_in_payload(payload2,"role_ids",[context.tmsRole])
    print(updatedpayload1)
    context.response3 = team1.role_Assign(updatedpayload1, context.token)
    print(context.response3)

@when('User Creates a team')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    Teampayload = context.api.get_Payload("casemanager", "teamcreation")
    updatedteampayload=context.api.update_key_in_payload(Teampayload,"roles",context.caseManagerRole)
    teamcre = TeamCreation.TeamCreation(ENV_NAME)
    context.response6 = teamcre.team_Create(updatedteampayload, context.token)
    print(context.response6)
    context.response7=teamcre.get_team(context.token)
    context.TeamID=context.api.extract_data_from_response(context.response7,"id")
    print(context.TeamID)

@when('User Creates a Scenario')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    Scenariopayload = context.api.get_Payload("casemanager", "scenariocreation")
    updatedteampayloadscenario=context.api.update_key_in_payload(Scenariopayload,"team",context.TeamID)
    scenario =ScenarioCreation(ENV_NAME)
    context.response10 = scenario.senario_Creation(updatedteampayloadscenario, context.token)
    print(context.response10)
    context.ScenarioID=context.api.extract_data_from_response(context.response10,"id")
    print(context.ScenarioID)
    metricpayload = context.api.get_Payload("casemanager", "metricsetter")
    context.response11=scenario.metric_Setter(metricpayload, context.token,context.ScenarioID)
    print(context.response11)

@when('User activates the Scenario')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    Scenariopayload1 = context.api.get_Payload("casemanager", "scenarioactivation")
    scenario =ScenarioCreation(ENV_NAME)
    context.response15 = scenario.activate_Scenario(Scenariopayload1, context.token,context.ScenarioID)
    print(context.response15)

@when('User deactivates the Scenario')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)  # or "dev" as per your env
    Scenariopayload1 = context.api.get_Payload("casemanager", "scenariodeactivation")
    scenario =ScenarioCreation(ENV_NAME)
    context.response15 = scenario.activate_Scenario(Scenariopayload1, context.token,context.ScenarioID)
    print(context.response15)

@when('User deletes the role,team,scenario')
def step_impls2(context):
    context.api = ApiHelper(ENV_NAME)
    teamcre = TeamCreation.TeamCreation(ENV_NAME)
    response17=teamcre.role_Delete(context.token,context.caseManagerRole)
    print(response17)
    response19=teamcre.role_Delete(context.token,context.tmsRole)
    print(response19)
    response18=teamcre.team_Delete(context.token,context.TeamID)
    print(response18)
    scenario =ScenarioCreation(ENV_NAME)
    response20=scenario.scenario_Delete( context.token, context.ScenarioID)
    print(response20)



