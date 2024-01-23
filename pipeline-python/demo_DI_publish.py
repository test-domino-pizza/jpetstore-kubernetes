import random, uuid, requests, argparse, datetime, time, os
import logging
import subprocess

from common_utils import DependencyLicenseTemplate,  sanitazeTenantUrl, make_web_request, LICENSES, nanoseconds_to_seconds, nanoseconds_to_microseconds

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('vra_di_publisher')

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--tenant", dest = "tenantApiUrl", default = "mcmp-learn-api.multilcoud-ibm.com", help="Tenant API base url\nEx: mcmp-learn-api.multilcoud-ibm.com")

parser.add_argument("-BT", "--build_token", dest = "buildToken", default = "", help="DevOps intelligence Build token")
# parser.add_argument("-DT", "--deploy_token", dest = "deployToken", default = "", help="DevOps intelligence Deploy token")
# parser.add_argument("-TT", "--test_token", dest = "testToken", default = "", help="DevOps intelligence test token")
# parser.add_argument("-ST", "--secure_token", dest = "secureToken", default = "", help="DevOps intelligence Secure token")

args = parser.parse_args()

# def post_secure_licenses( tenantUrl, secureToken, technicalService="vra_demo", date=datetime.datetime.utcnow().isoformat("T")+"Z" ):


#     try:

#         tenantUrl = sanitazeTenantUrl(tenantUrl)
#         licenseTool = random.choice( [ "pipLicense", "licenseFinder",  ] )
#         ENDPOINT = f"{tenantUrl}dash/api/dev_secops/v3/technical-services/license-scan?scannedBy={licenseTool}&scannedTime={date}"
#         scan = {"dependency_licenses": []}

#         for _ in range(random.randint(1,2)):

#             license = DependencyLicenseTemplate()
            
#             licenseData = random.choice( LICENSES )
#             license.dependency_name =  licenseData['Package Name']
#             license.dependency_version = "v{0}.{1}.{2}".format(random.randint(0,16),random.randint(0,16),random.randint(0,16))
#             license.dependency_homepage = "https://www.github.com/{0}".format(licenseData["License Name"].replace(" ", ""))
#             license.dependency_install_path = "/src/node_modules/{0}".format(licenseData["License Name"].replace(" ", ""))
#             license.dependency_package_manager = "node"
#             license.license_name = licenseData['License Name']
#             license.license_link = "https://www.{0}.com/{1}".format(licenseData["License Name"].replace(" ", ""),str(uuid.uuid4()))
#             license.status = licenseData["Status"]
#             license.provider_href = "https://pypi.org/"
#             license.technical_service_name = technicalService
#             license.technicalserviceoverride = True

#             scan["dependency_licenses"].append( license.__dict__ )


#         payload = scan
#         payload["technical_service_name"] = technicalService
#         payload["technicalserviceoverride"] = True

#         headers = { 'Authorization': 'TOKEN ' + secureToken, 'Content-Type': 'application/json', 'accept': 'application/json' }
        
#         LOGGER.info( f"Dependency licenses sample payload: {payload}" )

#         response, successfullyPosted, errorMessage = make_web_request(url=ENDPOINT, requestMethod=requests.post, payload=payload, headers=headers, logToIBM=True)

#         LOGGER.info( f"Dependency licenses: {response.status_code if response else 'None'}" )
        

#     except Exception as e:

#         LOGGER.error(str(e))
#         return False, str(e)

#     return successfullyPosted


# def post_sample_deploy_data(   tenantUrl:str, deployToken: str, deployDate=datetime.datetime.utcnow().isoformat("T") + "Z", technicalService="sample_data", release=f'release-{time.strftime("%Y.%m.%d")}', status=random.choice(['Failed','Deployed']) ):
#     tenantUrl = sanitazeTenantUrl(tenantUrl)
#     endpointUrl = f"{tenantUrl}dash/api/deployments/v4/technical-services/deployments"

#     payload = {
#                 'creation_date': deployDate, 
#                'deploymentid': "VRA_" + str(uuid.uuid4()), 
#                'duration': nanoseconds_to_microseconds( int( os.getenv( "elapsed_time", random.randint(6005720000,900572000000) ) ) ), 
#                'endpoint_hostname': 'Do not apply', 
#                'endpoint_technical_service_id': os.getenv("BUILD_URL", 'http://13.82.103.214:8080'), 
#                'name': f'VRA_deployment_{release}', 
#                'provider': os.getenv("DI_PROVIDER" ,"VRA"),
#                'providerhref': os.getenv("BUILD_URL", 'http://13.82.103.214:8080'), 
#                'technical_service_name': technicalService, 
#                'technicalserviceoverride': True, 
#                'status': status, 
#                'tool': 'Jenkins', 
#                'release': release, 
#                'environment': 'production', 
#                'isproduction': True
#             }
    
#     LOGGER.info(f"Deploy sample payload: {payload}")
#     headers = {
#         "Authorization": f"TOKEN {deployToken}",
#         "Content-Type": "application/json",
#         "accept": "application/json"
#     }

#     response, success, errorMessage = make_web_request(url=endpointUrl, payload=payload, headers=headers, requestMethod=requests.post)

#     LOGGER.info(
#         f"Deploy publishment status code : {response.status_code if response else 'None'}"
#     )

#     return success, errorMessage

def post_sample_test_data(  tenantUrl, testToken,  technicalServiceName="vra_demo", testEngine="ant", bugs=random.randint(0,7), codeCoverage=random.randint(30,100), codeSmells=random.randint(0,8), hostName="13.82.103.214:8080", env="production",   releaseName=f"release-{time.strftime('%Y.%m.%d')}", skipped=random.randint(0,5), status=random.choice(["passed","failed"])  ):
    
    runId = "Dynatrace_install_" + str(uuid.uuid4())
    tenantUrl = sanitazeTenantUrl(tenantUrl)
    endpoint = f"{tenantUrl}dash/api/test/v3/technical-services/tests/run/{runId}/status"
    params = {
        "technicalServiceName": technicalServiceName,
        "testEngine": testEngine,
        "technicalServiceOverride" : True,
        "runID": runId,
        "Authorization": testToken,
    }

    payload = {
        "bugs": bugs,
        "codecoverage": codeCoverage,
        "codesmells": codeSmells,
        "duration": nanoseconds_to_seconds( int( os.getenv( "elapsed_time", random.randint(6005720000,900572000000) ) ) ),
        "endpoint_hostname": os.getenv( "BUILD_URL", hostName ),
        "endpoint_service_id": os.getenv( "BUILD_URL", hostName ),
        "environmentname": env,
        "failed": 1 if status == "failed" else 0,
        "passed": 1 if status == "passed" else 0 ,
        "releasename": releaseName,
        "skipped": skipped,
        "status": status,
        "test_engine": testEngine,
        "test_type": random.choice(["function","unit"])
    }
    LOGGER.info(f"Test sample payload: {payload}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {testToken}'
    }

    response, succesfulOperation, errorMessage = make_web_request(url=endpoint, payload=payload, headers=headers, requestMethod=requests.post, params=params)
    LOGGER.info(
        f"Test publishment status code : {response.status_code if response else 'None'}"
    )
    return succesfulOperation, errorMessage


def post_sample_build_data( tenantUrl:str, buildToken: str, buildDate=datetime.datetime.utcnow().isoformat("T") + "Z", branch=f'release-{time.strftime("%Y.%m.%d")}', technicalService="petstore build on azure", status=random.choice(["failed", "passed"]),duration= int( os.getenv( "elapsed_time", random.randint(6005720000,900572000000) ) ) ):

    tenantUrl = sanitazeTenantUrl(tenantUrl)
    endpointUrl = f"{tenantUrl}dash/api/build/v3/technical-services/builds"

    payload = {
               'branch': branch, 
               'build_engine': 'Azure pipeline', 
               'build_id': str(uuid.uuid4()), 
               'build_status': status, 
               'built_at': buildDate, 
               'commit': '606b16c15ea6ade03fe70dc9a88c306a54be7a14', 
               'details': 'Sample data build', 
               'duration': duration, ## Build time has to be in nano seconds!! ## 
               'durationInNano':duration,
               'endpoint_hostname': 'dev.azure.com', 
               'endpoint_technical_service_id': technicalService, 
               'event_type': 'push', 
               'pull_request_number': '23', 
               'repo_url': 'https://github.com/bridge-demo/jpetstore-kubernetes.git', 
               'technical_service_name': technicalService, 
               'technical_service_override': True, 
               'href': os.getenv("BUILD_URL", 'https://dev.azure.com/Kyndryl/CTO%20Demo%20Environments/_build')
            }
    LOGGER.info(f"Build payload: {payload}")

    headers = {
        "Authorization": f"TOKEN {buildToken}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    response, success, errorMessage = make_web_request(url=endpointUrl, payload=payload, headers=headers, requestMethod=requests.post)
    LOGGER.info(f"Build publish status code : {response.status_code if response else 'None'} ")
    return success, errorMessage




def publish_di_data(technicalService="Petstore on Azure", status="failed"):

    tenantUrl = sanitazeTenantUrl( args.tenantApiUrl, urlType='url' )
    # post_sample_test_data(tenantUrl=tenantUrl, testToken=args.testToken, technicalServiceName=technicalService, status=status)
    post_sample_build_data( tenantUrl=tenantUrl, buildToken=args.buildToken, technicalService=technicalService, status=status )
    

    # if status == "passed":
    #     deploy_status = "Deployed"
    # else:
    #     deploy_status = "Failed"

    # post_sample_deploy_data( tenantUrl=tenantUrl, deployToken=args.deployToken, technicalService=technicalService, status=deploy_status )
    
    
    # post_secure_licenses( tenantUrl=tenantUrl, secureToken=args.secureToken, technicalService=technicalService )




def main():
    LOGGER.info("Publishing data to DI")

    publish_di_data( status=os.getenv("PIPELINE_STATUS","passed")  )

    






if __name__ == "__main__":
    main()