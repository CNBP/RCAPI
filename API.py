import sys
from pathlib import Path

str_path_project = str(Path(__file__).resolve().absolute())
sys.path.append(str_path_project)

from query_admission import admission_project
from query_baby import baby_project
from query_mother import mother_project
from query_CNFUN import CNFUN_project
from typing import List
from environs import Env

import csv

"""
Higher level wrapper of query_admission for simple to use API function calls against the admission tables 
"""


class CNNCNFUN_data_retrieval:
    """
    This class attempt to retrieve everything from the RedCap based on the CNBPIDs provided.
    Upon initialization, it will then get any information based on needed.
    """

    def __init__(
        self, CNBPID: str or List[str], Tokens=None, URL=None,
    ):
        if Tokens is None:
            # If not specified, load from the environment.
            env = Env()
            env.read_env()
            Tokens = {
                "admission": env("REDCAP_TOKEN_CNN_ADMISSION"),
                "baby": env("REDCAP_TOKEN_CNN_BABY"),
                "mother": env("REDCAP_TOKEN_CNN_MOTHER"),
                "cnfun": env("REDCAP_TOKEN_CNFUN_PATIENT"),
            }
        if URL is None:
            URL = "https://redcap.cnbp.ca/api/"

        # Initialize the CNBPID and then create the respective projects using default credentials (without retrieving bulk of the data)
        self.CNBPIDs = CNBPID
        self.admission_project = admission_project(Token=Tokens["admission"], URL=URL)
        self.baby_project = baby_project(Token=Tokens["baby"], URL=URL)
        self.mother_project = mother_project(Token=Tokens["mother"], URL=URL)
        self.CNFUN_project = CNFUN_project(Token=Tokens["cnfun"], URL=URL)

        # Use CNBPID to retrieve the other two key IDs.
        self.caseIDs = self.admission_project.get_caseIDwithCNBPID(CNBPID)
        self.babyIDs = self.admission_project.get_babyIDwithCNBPID(CNBPID)

        # Use the babyIDs to help retrieve the two other IDs.
        self.motherIDs = self.baby_project.get_MotherID_with_BabyID(self.babyIDs)
        self.CNNPatientUIs = self.baby_project.get_PatientUI_with_BabyID(self.babyIDs)

        # Finally, use CNNPatientUI to get PatientIDs
        self.PatientIDs = self.CNFUN_project.get_PatientID_with_CNNPatientUI(
            self.CNNPatientUIs
        )

    def get_admission_data(self):
        """
        Use the list of CNBPIDs to obtain the necessary admission data
        :param CNBPID:
        :return:
        """
        list_case_data = self.admission_project.get_records_admission(self.caseIDs)
        return list_case_data

    def get_baby_data(self):
        """
        Use the list of CNBPIDs to obtain the necessary admission data
        :param CNBPID:
        :return:
        """
        list_case_data = self.baby_project.get_records_baby(self.babyIDs)
        return list_case_data

    def get_mother_data(self):
        """
        Use the list of CNBPIDs to obtain the necessary admission data
        :param CNBPID:
        :return:
        """
        list_case_data = self.mother_project.get_records_mother(self.motherIDs)
        return list_case_data

    def get_CNFUN_data(self):
        list_case_data = self.CNFUN_project.get_records_CNFUN(self.PatientIDs)
        return list_case_data

    def write_all_csv(self):
        list_case = self.get_admission_data()
        list_baby = self.get_baby_data()
        list_mother = self.get_baby_data()
        list_cnfun = self.get_CNFUN_data()
        with open(f"CNN_admission.csv", "w") as file_case:
            writer = csv.writer(file_case)
            writer.writerow(list_case)
        with open("CNN_babies.csv", "w") as file_case:
            writer = csv.writer(file_case)
            writer.writerow(list_baby)
        with open("CNN_mothers.csv", "w") as file_case:
            writer = csv.writer(file_case)
            writer.writerow(list_mother)
        with open("CNFUN.csv", "w") as file_case:
            writer = csv.writer(file_case)
            writer.writerow(list_cnfun)


def test_CNNCNFUN_data_retrieval():
    retrieval = CNNCNFUN_data_retrieval("VXS0000007")
    retrieval.write_all_csv()
