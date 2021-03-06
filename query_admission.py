from query_common import (
    filter_records,
    ProjectMixins,
)
from redcap import Project  # note this is from PyCap.redcap
from typing import List


class admission_project(ProjectMixins):
    """
    One baby can have many admissions CaseIDs.
    One hospital record can have many CaseIDs.
    One baby has only one hospital record number.
    """

    def __init__(
        self, Token, URL, get_all_field=False,
    ):
        """
        Create a project using PyCap
        :param Token:
        :param URL:
        :return:
        """
        # Several key properties we'll use throughout
        self.project = Project(URL, Token)
        fields_keyid = ["caseid", "cnbpid", "babyid"]

        # For now, make sure to onyl get the data related to these key ids to reduce load time
        self.data = self.get_fields(fields_keyid)

        # if specified, get all the records.
        if get_all_field:
            self.data = self.project.export_records()

    def get_recordfields(self, field_data: str, field_filter: str, filter_value: str):
        """
        Wrap around teh common get record fields, tailer it to the current project.
        :param field_data:
        :param field_filter:
        :param filter_value:
        :return:
        """
        self.data = self.get_recordfields_common(field_data, field_filter, filter_value)

    def get_caseIDwithCNBPID(self, CNBPID: str or List[str]):
        """
        Get a list of CaseD using data provided list of CNBPIDs.
        :param dataset: the indexing list of dictionary showing correspondence
        :param list_CNBPID:
        :return:
        """
        list_filtered_dict = self.filter_with_CNBPID(CNBPID)
        list_caseID = []
        for case in list_filtered_dict:
            list_caseID.append(case["caseid"])

        if list_caseID == []:
            raise ValueError("No case found.")
        return list_caseID

    def filter_with_CNBPID(self, CNBPID: str or List[str]):
        """
        Check the list, only retain the relevant CNBPIDs interested.
        :param dataset: CNBPIDs & record ID correspondence list.
        :param CNBPID:
        :return:
        """
        list_filtered = None

        filtered_field = "cnbpid"
        # Hnadling when CNBPIDs is string instead of list (allowing batch function).
        if type(CNBPID) is str:
            CNBPID = [CNBPID]

        list_filtered = filter_records(self.data, filtered_field, CNBPID)

        return list_filtered

    def get_babyIDwithCNBPID(self, CNBPID: str or List[str]):
        """
        Get a list of CaseD using data provided list of CNBPIDs.
        :param dataset: the indexing list of dictionary showing correspondence
        :param list_CNBPID:
        :return:
        """
        list_filtered_dict = self.filter_with_CNBPID(CNBPID)
        list_caseID = []
        for case in list_filtered_dict:
            list_caseID.append(case["babyid"])
        return list_caseID

    def get_all_CNBPIDs(self):
        """
        Obtain all the CNBPIDs from the RedCap database.
        :return: CNBPIDs & record ID correspondence list.
        """
        subset = self.project.export_records(fields=["cnbpid"])
        # @todo strip this into more easily digestable format
        return subset

    def get_records_admission(self, cases: List[int]):
        """
        Retrieve the cases based on their INDEX which is the
        :param cases:
        :return:
        """
        cases_data = self.project.export_records(records=cases)
        return cases_data
