# listenerclass.py
from behave.model_core import Status
import traceback
import allure
from allure_commons.types import AttachmentType

class CustomListener:
    def before_all(self, context):
        print("\n[Listener] Test execution started.")

    def after_all(self, context):
        print("[Listener] Test execution finished.")

    def before_feature(self, context, feature):
        print(f"\n[Listener] Starting Feature: {feature.name}")

    def after_feature(self, context, feature):
        print(f"[Listener] Finished Feature: {feature.name}")

    def before_scenario(self, context, scenario):
        print(f"\n[Listener] Starting Scenario: {scenario.name}")
        allure.dynamic.title(scenario.name)
        if hasattr(scenario, "tags"):
            allure.dynamic.description(f"Tags: {scenario.tags}")

    def after_scenario(self, context, scenario):
        if scenario.status == Status.passed:
            print(f"[Listener] Scenario Passed: {scenario.name}")

        elif scenario.status == Status.failed:
            print(f"[Listener] Scenario Failed: {scenario.name}")
            for step in scenario.steps:
                if step.status == Status.failed and step.exception:
                    allure.attach(
                        f"Step: {step.name}\nError: {step.exception}",
                        name=f"Failure in step: {step.name}",
                        attachment_type=AttachmentType.TEXT
                    )
                    print(f"Failure in Step: {step.name}")
                    traceback.print_exception(
                        type(step.exception), step.exception, step.exception.__traceback__
                    )

        elif scenario.status == Status.skipped:
            print(f"[Listener] Scenario Skipped: {scenario.name}")
            if hasattr(scenario, "skip_reason") and scenario.skip_reason:
                print(f"   ↪ Reason: {scenario.skip_reason}")

        elif scenario.status == Status.untested:
            print(f"[Listener] Scenario Not Implemented: {scenario.name}")

        else:
            print(f"[Listener] Scenario Finished with status {scenario.status}: {scenario.name}")

    def before_step(self, context, step):
        print(f"[Listener] Step Started: {step.name}")
        step.allure_context = allure.step(step.name)
        step.allure_context.__enter__()

    def after_step(self, context, step):
        try:
            if step.status == Status.passed:
                print(f"[Listener] Step Passed: {step.name}")
            elif step.status == Status.failed:
                print(f"[Listener] Step Failed: {step.name}")
                if step.exception:
                    allure.attach(
                        f"Error: {step.exception}",
                        name=f"Error in step: {step.name}",
                        attachment_type=AttachmentType.TEXT
                    )
        finally:
            if hasattr(step, "allure_context"):
                step.allure_context.__exit__(
                    type(step.exception) if step.exception else None,
                    step.exception,
                    step.exception.__traceback__ if step.exception else None
                )

    def scenario_not_found(self, scenario_name):
        print(f"[Listener] No matching scenario found with name: {scenario_name}")
        allure.attach(
            f"No scenario found with name: {scenario_name}",
            name="Scenario Not Found",
            attachment_type=AttachmentType.TEXT
        )
