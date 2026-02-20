# constants.py

from datetime import datetime

#LOG_FILE = datetime.now().strftime("%Y-%m-%d") + "_dss_child_health_integration_missing_patient.log"
#OG_FILE = datetime.now().strftime("%Y-%m-%d") + "_dataValueSet_post.log"
#LOG_FILE = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_accuity_to_dhis2_integration.log"
LOG_FILE = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_dhis2_to_dhis2_orgunit_sync.log"
LOG_FILE_TEI_ATTRIBUTE_VALUE_ERROR_LOG = datetime.now().strftime("%Y-%m-%d") + "_tei_update_error_log.txt"