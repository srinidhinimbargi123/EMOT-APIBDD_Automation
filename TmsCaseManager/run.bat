cd ..
@REM Run Behave with Allure formatter
behave -f allure_behave.formatter:AllureFormatter -o Reports TmsCaseManager\features

@REM Generate Allure static HTML report
allure generate Reports -o allure-report --clean

@REM Open the generated report
allure open allure-report

pause
