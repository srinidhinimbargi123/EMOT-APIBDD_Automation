# endpoints_Location/case_manager_endpoints.py
EndPointsCaseManager={
    "commonqueuealerts" : "/api/v1/qa/atoms/case-manager/filters/data/?page=1&page_size=5",
    "commonqueuealertswithfilters" : "/api/v1/qa/atoms/case-manager/filters/data/?page=1&page_size=5&team_id=65",
    "commonqueuecases":"/api/v1/qa/atoms/case-manager/cases?page=1&page_size=5&common_queue=true",
    "commonqueuecasesfilter":"/api/v1/qa/atoms/case-manager/cases?page=1&page_size=5&common_queue=true&team_id=53&team_level_order=1",
    "casesassign":"/api/v1/qa/atoms/case-manager/cases/bulk-update/",
    "casedocuments":"/api/v1/qa/atoms/case-manager/case-documents",
    "investigatecase":"/api/v1/qa/atoms/case-manager/cases/16564/"
} 

EndPointsTMS={
    "add-data-start":"/api/v1/qa/atoms/data_manager/file-upload/start/",
    "add-data-part":"/api/v1/qa/atoms/data_manager/file-upload/part-url/",
    "add-data-complete":"/api/v1/qa/atoms/data_manager/file-upload/complete/",
    "add-data-ingestion":"/api/v1/qa/atoms/data_manager/ingestion/"
} 