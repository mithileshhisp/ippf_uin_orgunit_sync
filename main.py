## install
#pip install python-dotenv
#pip install psycopg2-binary
#pip install clickhouse-connect
#pip install --upgrade certifi
#pip install --upgrade requests certifi urllib3 ## for post data in hmis production certificate issue

import urllib3 ## for disable warning of Certificate
urllib3.disable_warnings() ## for disable warning of Certificate

import ssl
#import requests

from concurrent.futures import ThreadPoolExecutor
import requests
import certifi  ## for post data in hmis production certificate issue
import json
from datetime import datetime,date
#import nepali_datetime
# main.py
from dotenv import load_dotenv
import os
import time

load_dotenv()

from utils import (
    configure_logging,get_tei_details,get_orgunit_details, get_single_orgunit_details,
    log_info,log_error,get_org_and_child_uid,get_org_and_child_attribute_value,
    push_orgunit_in_dhis2,update_orgunit_in_dhis2,push_dataStore_event_in_dhis2
)

#print("OpenSSL version:", ssl.OPENSSL_VERSION)
#print("Certifi CA bundle:", requests.certs.where())

DHIS2_GET_API_URL = os.getenv("DHIS2_GET_API_URL")
DHIS2_GET_USER = os.getenv("DHIS2_GET_USER")
DHIS2_GET_PASSWORD = os.getenv("DHIS2_GET_PASSWORD")

DHIS2_POST_API_URL = os.getenv("DHIS2_POST_API_URL")
DHIS2_POST_USER = os.getenv("DHIS2_POST_USER")
DHIS2_POST_PASSWORD = os.getenv("DHIS2_POST_PASSWORD")


PROGRAM_UID = os.getenv("PROGRAM_UID")
PROGRAM_STAGE_UID = os.getenv("PROGRAM_STAGE_UID")
SEARCH_TEI_ATTRIBUTE_UID = os.getenv("SEARCH_TEI_ATTRIBUTE_UID")

UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID = os.getenv("UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID")
REGION_NAME_ATTRIBUTE_UID = os.getenv("REGION_NAME_ATTRIBUTE_UID")
LEGAL_NAME_ATTRIBUTE_UID = os.getenv("LEGAL_NAME_ATTRIBUTE_UID")



SEARCH_VALUE = os.getenv("SEARCH_VALUE")
ORGUNIT_UID = os.getenv("ORGUNIT_UID")

ORG_UNIT_META_ATTRIBUTE = os.getenv("ORG_UNIT_META_ATTRIBUTE")
orgunit_post_url = f"{DHIS2_POST_API_URL}organisationUnits"
tei_get_url = f"{DHIS2_GET_API_URL}trackedEntityInstances"

dataValueSet_endPoint = f"{DHIS2_POST_API_URL}dataValueSets"

namespace_url = f"{DHIS2_GET_API_URL}dataStore/accuityResponse/"
ACCUITY_FLOW_URL = os.getenv("ACCUITY_FLOW_URL_NEW")
#print( f" DHIS2_GET_USER. { DHIS2_GET_USER }, DHIS2_GET_PASSWORD  { DHIS2_GET_PASSWORD} " )

#DHIS2_AUTH_POST = ("hispdev", "Devhisp@1")
#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

# Create a session object for persistent connection
#session_get = requests.Session()
#session_get.auth = DHIS2_AUTH_GET

raw_auth = os.getenv("DHIS2_AUTH")

if raw_auth is None:
    raise ValueError("DHIS2_AUTH is missing in .env")

if ":" not in raw_auth:
    raise ValueError("DHIS2_AUTH must be in user:password format")

user, pwd = raw_auth.split(":", 1)
#session_get.auth = (user, pwd)
'''
session_get = requests.Session()
session_get.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)

session_post = requests.Session()
session_post.auth = (DHIS2_POST_USER, DHIS2_POST_PASSWORD)
'''

#session_get.verify = False

RPA_DELAY = 10

def main_with_logger():

    configure_logging()

    current_time_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print( f"Syncing of OrgUnit process start . { current_time_start }" )
    log_info(f"Syncing of OrgUnit process start  . { current_time_start }")

    session_get = requests.Session()
    session_get.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)

    session_post = requests.Session()
    session_post.auth = (DHIS2_POST_USER, DHIS2_POST_PASSWORD)

    #session = requests.Session()
    #session_post.verify = certifi.where()

    orgunit_list_map = get_orgunit_details( orgunit_post_url, session_post )
    tei_list = get_tei_details( tei_get_url, session_get, ORGUNIT_UID, PROGRAM_UID, SEARCH_TEI_ATTRIBUTE_UID, SEARCH_VALUE, UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID, LEGAL_NAME_ATTRIBUTE_UID )
    
    print(f"trackedEntityInstances list Size {len(tei_list) }")
    log_info(f"trackedEntityInstances list Size {len(tei_list) } ")

    if tei_list:

        for tei in tei_list:
            tei_uid = tei["trackedEntityInstance"]
            org_unit = tei["orgUnit"]

            # Convert attributes list into dictionary
            attributes_dict = {
                #attr["displayName"]: attr.get("value", "")
                attr["attribute"]: attr.get("value", "")
                for attr in tei.get("attributes", [])
            }

            print("TEI UID:", tei_uid)
            print("Org Unit:", org_unit)
            #print("Legal Name:", attributes_dict.get("Legal Name"))
            print("UIN Code: ", attributes_dict.get(SEARCH_TEI_ATTRIBUTE_UID))
            print("Region: ", attributes_dict.get(REGION_NAME_ATTRIBUTE_UID))
            print("Legal Name: ", attributes_dict.get(LEGAL_NAME_ATTRIBUTE_UID))
            
            #if not attributes_dict.get(UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID) and attributes_dict.get(LEGAL_NAME_ATTRIBUTE_UID) and attributes_dict.get(SEARCH_TEI_ATTRIBUTE_UID):
            if (
                not attributes_dict.get(UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID) and 
                attributes_dict.get(LEGAL_NAME_ATTRIBUTE_UID) and 
                attributes_dict.get(SEARCH_TEI_ATTRIBUTE_UID)
            ):
                print("UIN Code :", attributes_dict.get(SEARCH_TEI_ATTRIBUTE_UID))
                print("Region:", attributes_dict.get(REGION_NAME_ATTRIBUTE_UID))
                print("Legal Name:", attributes_dict.get(LEGAL_NAME_ATTRIBUTE_UID))
                uin_code = attributes_dict.get(SEARCH_TEI_ATTRIBUTE_UID)
                region_code = attributes_dict.get(REGION_NAME_ATTRIBUTE_UID)
                legal_name = attributes_dict.get(LEGAL_NAME_ATTRIBUTE_UID)
                '''
                orgunit_parent = orgunit_list_map.get(region_code)
                print("orgunit_parent:", orgunit_parent)

                if orgunit_parent:
                    print("OrgUnit UID:", orgunit_parent["orgUnitUID"])

                    for child in orgunit_parent["children"]:
                        print("Child Name:", child["name"])
                        print("Child UID:", child["id"])
                '''
                #parent_org_uid, orguit_uid = get_org_and_child_uid(orgunit_list_map,region_code,legal_name)
                parent_org_uid, orguit_uid, orguit_attribute_value = get_org_and_child_attribute_value(orgunit_list_map, region_code, ORG_UNIT_META_ATTRIBUTE)
                #orguit_attribute_value = None
                if parent_org_uid:
                    print(f"Parent Org UID:, {parent_org_uid}, orguit_uid Org UID:, {orguit_uid}.  OrgUnit orguit_attribute_value:, {orguit_attribute_value}")
                    #if orguit_attribute_value != uin_code:
                    #if orguit_attribute_value and orguit_attribute_value != uin_code:
                    #if not orguit_attribute_value:
                    if orguit_attribute_value is not None and orguit_attribute_value != uin_code:
                        #print("new orgunit created")
                        print(f"OrgUnit orguit_attribute_value inside new: , {orguit_attribute_value}")
                        orgUnit_post_payload = {
                            "name": legal_name,
                            "shortName": legal_name,
                            "parent":{ "id" : parent_org_uid},
                            "openingDate": "1990-01-01",
                            "attributeValues":[{
                                "value":uin_code,
                                "attribute":{"id":ORG_UNIT_META_ATTRIBUTE}
                            }]
                        }
                        push_orgunit_in_dhis2(orgunit_post_url, session_post, orgUnit_post_payload, region_code, legal_name, uin_code, tei, tei_get_url, session_get, UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID )
                    else:
                        print("OrgUnit orguit_attribute_value inside update :", orguit_attribute_value)
                        orgunit_response_data = get_single_orgunit_details( orgunit_post_url, session_post, orguit_uid )
                        if orgunit_response_data:
                            attributeValues = [{
                                "value":uin_code,
                                "attribute":{"id":ORG_UNIT_META_ATTRIBUTE}
                            }]
                            
                            orgunit_response_data["attributeValues"] = attributeValues
                            
                            update_orgunit_in_dhis2(orgunit_post_url, session_post, orgunit_response_data, orguit_uid, region_code, legal_name, uin_code, tei, tei_get_url, session_get, UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID )
                            

                '''
                attr1 = "UkQI1dWzZOv"
                attr2 = "qsASQ0NRTVA"
                combined_key_attr = f"{attr1}_{attr2}"
                new_object = {
                    "date": datetime.now().isoformat() + "Z",
                    "tei_uid": tei_uid,
                    attr1: attributes_dict.get("UkQI1dWzZOv"),
                    attr2: attributes_dict.get("qsASQ0NRTVA"),
                    combined_key_attr: accuity_search_response_tei_attribute
                }

                push_dataStore_tei_in_dhis2( session_get, namespace_url, tei_uid,  combined_key_attr, new_object )
                '''

            print("-" * 50)
            log_info("-" * 50)

        #print( f"dataValueSet_payload . { dataValueSet_payload }" )
        #push_dataValueSet_in_dhis2( dataValueSet_endPoint, session_post, dataValueSet_payload )
    
if __name__ == "__main__":

    #main()
    main_with_logger()
    current_time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print( f"Syncing of OrgUnit process finished . { current_time_end }" )
    log_info(f"Syncing of OrgUnit process finished . { current_time_end }")

    try:
        #sendEmail()
        print( f"Syncing of OrgUnit process finished . { current_time_end }" )
    except Exception as e:
        log_error(f"Email failed: {e}")


    #sendEmail()
    #print(f"total_patient_count. {total_patient_count}, null_patient_id_count. {null_patient_id_count}, event_push_count {event_push_count}")
    #log_info(f"total_patient_count. {total_patient_count}, null_patient_id_count. {null_patient_id_count}, event_push_count {event_push_count}")
    