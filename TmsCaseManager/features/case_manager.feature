 Feature: View Alerts in Common Queue

  Scenario: Login to TMS-CaseManager and view all alerts in Common Queue
    Given the user is logged in to TMS-CaseManager
    When the user navigates to the Common Queue
    Then the system should display all alerts with Alert ID and Transaction Type
  
  Scenario: Login to TMS-CaseManager and view all alerts in Common Queue1
    Given the user is logged in to TMS-CaseManager
    When the user navigates to the Common Queue
    Then the system should display all alerts with Alert ID and Transaction Type
    Then Investigate one of the case

