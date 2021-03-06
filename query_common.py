from redcap import Project  # note this is from PyCap.redcap
from typing import List


class ProjectMixins:
    """
    These functions serves as the basis function used to query the variety of table groups in RedCap. It takes care of basic communications etc.
    """

    project: Project = None  # Mixin require this object to work effectively

    def get_records(self):
        """
        Obtain all data from a project
        :param project:
        :return:
        """
        all_data = self.project.export_records()
        return all_data

    def get_fields(self, fields: List[str]):
        """
        A generalized function to get all records from certain fields.
        :param project:
        :param fields:
        :return:
        """
        list_dict = self.project.export_records(fields=fields)
        return list_dict

    def get_recordfields_common(
        self, field_data: str, field_filter: str, filter_value: str
    ) -> List[dict]:
        """
        This is a lighter query used to only retrieve partial information to minimize the download time
        :param targetted_project:
        :param field_data: the field name fo the data field.
        :param field_filter: the field used to filter the the entire database.
        :param filter_value: the values checked in field_filter used to remove the not needed records.
        :return: field_value: str,
        """

        # Get all records only containing the two fields needed.
        list_dict = self.project.export_records(fields=[field_data, field_filter])

        # Filter the list of dict to include ONLY records matching the filtered valuse in the filter field.
        list_filtered_dict = filter_records(list_dict, field_filter, filter_value)
        return list_filtered_dict


"""
These functions serves as the basis function used to query the variety of table groups in RedCap. It takes care of basic communications etc. 
"""


def createProject(Token, URL):
    """
    Create a project using PyCap
    :param Token:
    :param URL:
    :return:
    """

    # Two constants we'll use throughout
    project_admission = Project(URL, Token)
    return project_admission


def filter_records(
    dataset: List[dict], filter_field: str, list_filtered_value: str or List[str]
):
    """
    Generic filtering method, by checking the list, only retain the relevant CNBPIDs interested.
    :param list_filtered_value & record ID correspondence list.
    :param CNBPIDs:
    :return:
    """
    if type(list_filtered_value) is str:
        list_filtered_value = [list_filtered_value]

    list_filtered = list(
        filter(lambda person: person[filter_field] in list_filtered_value, dataset)
    )
    return list_filtered


def get_records(project) -> List[dict]:
    """
    Obtain all data from a project
    :param project:
    :return:
    """
    all_data = project.export_records()
    return all_data
