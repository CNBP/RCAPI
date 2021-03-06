from query_common import ProjectMixins
from redcap import Project  # note this is from PyCap.redcap
from typing import List

"""
These functions are used to retrieve the data from the MOTHERS table clusters.
"""


class mother_project(ProjectMixins):
    """
    One baby can have many admissions CaseIDs.
    One hospital record can have many CaseIDs.
    One baby has only one hospital record number.
    """

    def __init__(
        self, Token, URL, get_all_field=True,
    ):
        """
        Create a project using PyCap
        :param Token:
        :param URL:
        :param get_all_field by default, get all fields since for Mothers table cluster, we do not need associative information. 
        :return:
        """
        # Several key properties we'll use throughout
        self.project = Project(URL, Token)

        # These are very important ID fields from the
        # fields_keyid = ["babyid", "motherid", "baby_patieui"]

        # For now, make sure to onyl get the data related to these key ids to reduce load time
        # self.data = get_fields(self.project, fields_keyid)

        # if specified, get all the records.
        if get_all_field:
            self.data = self.project.export_records()

    def get_records_mother(self, MotherID: str or List[str]):
        """
        Retrieve the records based on their INDEX which is the MotherID in the Mother table.
        :param MotherID:
        :return:
        """
        if type(MotherID) is str:
            MotherID = [MotherID]
        cases_data = self.project.export_records(records=MotherID)
        return cases_data
