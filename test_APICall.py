from requests import post
from redcap import Project  # note this is from PyCap.redcap
from environs import Env
from query_baby import baby_project
from query_admission import admission_project
from query_CNFUN import CNFUN_project
from query_mother import mother_project

import pytest


@pytest.fixture
def get_tokens():
    env = Env()
    env.read_env()
    tokens = {
        "admission": env("REDCAP_TOKEN_CNN_ADMISSION"),
        "baby": env("REDCAP_TOKEN_CNN_BABY"),
        "mother": env("REDCAP_TOKEN_CNN_MOTHER"),
        "cnfun": env("REDCAP_TOKEN_CNFUN_PATIENT"),
    }
    return tokens


@pytest.fixture
def get_URL():
    URL = "https://redcap.cnbp.ca/api/"
    return URL


def test_Post(get_tokens, get_URL):

    payload = {
        "token": get_tokens["admission"],
        "format": "json",
        "content": "metadata",
    }

    response = post(get_URL, data=payload)
    assert response.ok
    print(response)


def test_PyCap(get_tokens, get_URL):
    project_admission = Project(get_URL, get_tokens["admission"])
    subset = project_admission.export_records(records=["1"], format="df")
    print(subset)


def test_query_mother(get_tokens, get_URL):
    mother = mother_project(get_tokens["mother"], get_URL)
    cnbpid = "6368"
    test = mother.get_records_mother(cnbpid)
    print(test)
    cnbpid = ["6368", "7173"]
    test = mother.get_records_mother(cnbpid)
    print(test)


def test_query_admission(get_tokens, get_URL):
    # def test_get_all_CNBPIDs():
    admission = admission_project(get_URL, get_tokens["admission"])

    print(admission.get_all_CNBPIDs())
    cnbpid = "VXS0000003"
    test = admission.filter_with_CNBPID(cnbpid)
    print(test)
    test = admission.get_babyIDwithCNBPID(cnbpid)
    print(test)
    test = admission.get_caseIDwithCNBPID(cnbpid)
    print(test)

    cnbpid = ["VXS0000003", "VXS0000015"]
    test = admission.filter_with_CNBPID(cnbpid)
    print(test)
    test = admission.get_babyIDwithCNBPID(cnbpid)
    print(test)
    test = admission.get_caseIDwithCNBPID(cnbpid)
    print(test)
