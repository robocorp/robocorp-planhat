import json
import pytest
import requests
from planhat.types import Company, PlanhatObjectList, PlanhatObject, Enduser, Asset


class TestPlanhatObject:
    def test_initialization(self):
        obj = PlanhatObject()
        assert obj.id is ""
        assert obj.source_id is ""
        assert obj.external_id is ""
        assert obj.to_serializable_json() == {}

    def test_initialization_with_kwargs(self):
        obj = PlanhatObject(id="1", source_id="2", external_id="3")
        assert obj.id == "1"
        assert obj.source_id == "2"
        assert obj.external_id == "3"

    def test_to_serializable_json(self):
        obj = PlanhatObject(id="1", source_id="2", external_id="3")
        json_obj = obj.to_serializable_json()
        assert json_obj == {
            "_id": "1",
            "sourceId": "2",
            "externalId": "3",
        }

    def test_from_response(self):
        data = {
            "_id": "1",
            "sourceId": "2",
            "externalId": "3",
        }
        response = requests.Response()
        response._content = bytes(json.dumps(data), "utf-8")
        response.url = "https://api.planhat.com/companies/1"
        response.request = requests.Request(
            "GET", "https://api.planhat.com/companies/1"
        ).prepare()
        response.headers["Content-Type"] = "application/json"
        obj = PlanhatObject.from_response(response)
        assert obj.id == "1"
        assert obj.source_id == "2"
        assert obj.external_id == "3"

    def test_get_urlpath(self):
        obj = Enduser(id="1")
        assert obj.get_urlpath() == "/endusers/1"

    def test_from_list(self):
        data = [
            {"_id": "1", "sourceId": "2", "externalId": "3"},
            {"_id": "4", "sourceId": "5", "externalId": "6"},
        ]
        objs = Enduser.from_list(data)
        assert len(objs) == 2
        assert all(isinstance(obj, Enduser) for obj in objs)
        assert objs[0].id == "1"
        assert objs[0].source_id == "2"
        assert objs[0].external_id == "3"
        assert objs[1].id == "4"
        assert objs[1].source_id == "5"
        assert objs[1].external_id == "6"


class TestPlanhatObjectList:
    def test_initialization(self):
        obj_list = PlanhatObjectList()
        assert len(obj_list) == 0

    def test_append(self):
        obj_list = PlanhatObjectList()
        obj = PlanhatObject()
        obj_list.append(obj)
        assert len(obj_list) == 1
        assert obj_list[0] == obj

    def test_extend(self):
        obj_list = PlanhatObjectList()
        objs = [PlanhatObject(), PlanhatObject()]
        obj_list.extend(objs)
        assert len(obj_list) == 2
        assert obj_list[0] == objs[0]
        assert obj_list[1] == objs[1]

    def test_getitem(self):
        obj_list = PlanhatObjectList([PlanhatObject(), PlanhatObject()])
        assert obj_list[0] == obj_list.__getitem__(0)
        assert obj_list[1] == obj_list.__getitem__(1)

    def test_setitem(self):
        obj_list = PlanhatObjectList([PlanhatObject(), PlanhatObject()])
        obj = PlanhatObject()
        obj_list[0] = obj
        assert obj_list[0] == obj

    def test_insert(self):
        obj_list = PlanhatObjectList([PlanhatObject(), PlanhatObject()])
        obj = PlanhatObject()
        obj_list.insert(1, obj)
        assert len(obj_list) == 3
        assert obj_list[1] == obj

    def test_remove(self):
        obj_list = PlanhatObjectList([PlanhatObject(id="1"), PlanhatObject(id="2")])
        obj = obj_list[0]
        obj_list.remove(obj)
        assert len(obj_list) == 1
        assert obj not in obj_list

    def test_find_by_id(self):
        obj_list = PlanhatObjectList([PlanhatObject(id="1"), PlanhatObject(id="2")])
        obj = obj_list.find_by_id("1")
        assert obj.id == "1"

    def test_find_by_source_id(self):
        obj_list = PlanhatObjectList(
            [PlanhatObject(source_id="1"), PlanhatObject(source_id="2")]
        )
        obj = obj_list.find_by_source_id("1")
        assert obj.source_id == "1"

    def test_find_by_external_id(self):
        obj_list = PlanhatObjectList(
            [PlanhatObject(external_id="1"), PlanhatObject(external_id="2")]
        )
        obj = obj_list.find_by_external_id("1")
        assert obj.external_id == "1"

    def test_find_by_company_id(self):
        obj_list = PlanhatObjectList(
            [
                Enduser(company_id="1"),
                Enduser(company_id="1"),
                Enduser(company_id="2"),
            ]
        )
        objs = obj_list.find_by_company_id("1")
        assert len(objs) == 2
        assert all(obj.company_id == "1" for obj in objs)

    def test_to_serializable_json(self):
        obj_list = PlanhatObjectList([PlanhatObject(), PlanhatObject()])
        json_list = obj_list.to_serializable_json()
        assert isinstance(json_list, list)
        assert len(json_list) == 2
        assert all(isinstance(obj, dict) for obj in json_list)

    def test_get_urlpath(self):
        obj_list = PlanhatObjectList()
        with pytest.raises(ValueError):
            obj_list.get_urlpath()


class TestCompany:
    def test_initialization(self):
        company = Company()
        assert company.id is ""
        assert company.source_id is ""
        assert company.external_id is ""
        assert company.name is ""
        assert company.to_serializable_json() == {}

    def test_initialization_with_kwargs(self):
        company = Company(id="1", source_id="2", external_id="3", name="Test Company")
        assert company.id == "1"
        assert company.source_id == "2"
        assert company.external_id == "3"
        assert company.name == "Test Company"
        assert company.to_serializable_json() == {
            "_id": "1",
            "sourceId": "2",
            "externalId": "3",
            "name": "Test Company",
        }


class TestAsset:
    def test_initialization(self):
        asset = Asset()
        assert asset.id is ""
        assert asset.source_id is ""
        assert asset.external_id is ""
        assert asset.company_id is ""
        assert asset.company_name is ""
        assert asset.to_serializable_json() == {}

    def test_initialization_with_kwargs(self):
        asset = Asset(
            id="1",
            source_id="2",
            external_id="3",
            company_id="4",
            company_name="Test Company",
        )
        assert asset.id == "1"
        assert asset.source_id == "2"
        assert asset.external_id == "3"
        assert asset.company_id == "4"
        assert asset.company_name == "Test Company"
        assert asset.to_serializable_json() == {
            "_id": "1",
            "sourceId": "2",
            "externalId": "3",
            "companyId": "4",
            "companyName": "Test Company",
        }
