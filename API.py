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
import os
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
        self, CNBPID: str or List[str], Tokens=None, url=None,
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
        if url is None:
            url = "https://redcap.cnbp.ca/api/"

        if url[-1] != "/":
            url = url + "/"

        # Initialize the CNBPID and then create the respective projects using default credentials (without retrieving bulk of the data)
        self.CNBPIDs = CNBPID
        self.admission_project = admission_project(Token=Tokens["admission"], URL=url)
        self.baby_project = baby_project(Token=Tokens["baby"], URL=url)
        self.mother_project = mother_project(Token=Tokens["mother"], URL=url)
        self.CNFUN_project = CNFUN_project(Token=Tokens["cnfun"], URL=url)

        # Use CNBPID to retrieve the other two key IDs.
        try:
            self.caseIDs = self.admission_project.get_caseIDwithCNBPID(CNBPID)
        except ValueError as e:
            print(e)
            sys.exit(1)
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

        self.write_out_all_records("CNN_Admission.csv", list_case)
        self.write_out_all_records("CNN_babies.csv", list_baby)
        self.write_out_all_records("CNN_mothers.csv", list_mother)
        self.write_out_all_records("CNFUN.csv", list_cnfun)

        from zipfile import ZipFile

        zipObj = ZipFile("RetrievalResults.zip", "w")
        zipObj.write("CNN_Admission.csv")
        zipObj.write("CNN_babies.csv")
        zipObj.write("CNN_mothers.csv")
        zipObj.write("CNFUN.csv")
        zipObj.close()

        # Now the CSV files are zipped, can delete the others.
        os.remove("CNN_Admission.csv")
        os.remove("CNN_babies.csv")
        os.remove("CNN_mothers.csv")
        os.remove("CNFUN.csv")

    def write_out_all_records(self, path_file: str, list_case):
        # Open the file for writing.
        with open(path_file, "a", newline="") as file_case:
            write_header = True

            # Loop through the cases from the table with relevant ID columns
            for index, dict_case in enumerate(list_case):

                # Instantiate writer for the file, per the dict keys for alignment.
                writer = csv.DictWriter(file_case, dict_case.keys())

                # Write header only for the first time.
                if write_header:
                    writer.writeheader()
                    write_header = False

                # Write the main data block.
                writer.writerow(dict_case)


def test_CNNCNFUN_data_retrieval():
    retrieval = CNNCNFUN_data_retrieval("VXS0000007", url="https://redcap.cnbp.ca/api")
    retrieval.write_all_csv()
