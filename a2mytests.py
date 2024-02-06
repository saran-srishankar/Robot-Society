from society_hierarchy import *


def test_add_subordinate() -> None:
    c6 = Citizen(6, 'Starky Industries', 3036, 'Commander', 50)
    c2 = Citizen(2, 'Hookins National', 3027, 'Manager', 55)
    c3 = Citizen(3, 'Starky Industries', 3050, 'Labourer', 50)
    c5 = Citizen(5, 'S.T.A.R.R.Y Lab', 3024, 'Manager', 17)
    c8 = Citizen(8, 'Hookins National', 3024, 'Cleaner', 74)
    c7 = Citizen(7, 'Hookins National', 3071, 'Labourer', 5)
    c9 = Citizen(9, 'S.T.A.R.R.Y Lab', 3098, 'Engineer', 86)

    c6.add_subordinate(c8)
    assert c6.get_direct_subordinates()[0] is c8
    assert c8.get_superior() is c6

    c6.add_subordinate(c3)
    assert c6.get_direct_subordinates() == [c3, c8]
    assert c3.get_superior() is c6

    c6.add_subordinate(c2)
    assert c6.get_direct_subordinates() == [c2, c3, c8]
    assert c2.get_superior() is c6


def test_get_closest_common_superior() -> None:
    c1 = Citizen(1, 'Starky Industries', 3036, 'Commander', 50)
    c2 = Citizen(2, 'Hookins National', 3027, 'Manager', 55)
    c3 = Citizen(3, 'Starky Industries', 3050, 'Labourer', 50)
    c4 = Citizen(4, 'S.T.A.R.R.Y Lab', 3024, 'Manager', 17)
    c5 = Citizen(5, 'Hookins National', 3024, 'Cleaner', 74)
    c6 = Citizen(6, 'Hookins National', 3071, 'Labourer', 5)
    c7 = Citizen(7, 'S.T.A.R.R.Y Lab', 3098, 'Engineer', 86)
    c8 = Citizen(9, 'Saran Labs', 4000, 'mathematician', 50)

    c2.become_subordinate_to(c5)
    c1.become_subordinate_to(c5)
    c5.become_subordinate_to(c7)
    c4.become_subordinate_to(c7)
    c3.become_subordinate_to(c6)
    c7.become_subordinate_to(c8)
    c6.become_subordinate_to(c8)

    assert c2.get_closest_common_superior(4) == c7
    assert c2.get_closest_common_superior(2) == c2
    assert c2.get_closest_common_superior(1) == c5
    assert c2.get_closest_common_superior(3) == c8
    assert c4.get_closest_common_superior(2) == c7
    assert c4.get_closest_common_superior(6) == c8


def test_change_citizen_type() -> None:
    o = Society()
    c1 = DistrictLeader(1, "Starky Industries", 3024, "Manager", 50, 'Food')
    c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
    c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
    c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
    c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
    c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
    o.add_citizen(c4, None)
    o.add_citizen(c2, 4)
    o.add_citizen(c6, 2)
    o.add_citizen(c1, 4)
    o.add_citizen(c3, 1)
    o.add_citizen(c5, 1)

    new_1 = o.change_citizen_type(1)
    assert isinstance(new_1, Citizen) is True
    assert isinstance(new_1, DistrictLeader) is False
    assert new_1.cid == 1
    assert new_1.manufacturer == "Starky Industries"
    assert new_1.model_year == 3024
    assert new_1.job == "Manager"
    assert new_1.rating == 50
    assert new_1.get_superior() == c4
    assert new_1.get_direct_subordinates() == [c3, c5]
    assert c1.get_superior() is None
    assert c1.get_direct_subordinates() == []

    new_2 = o.change_citizen_type(2, 'business')
    assert isinstance(new_2, DistrictLeader) is True
    assert new_2.cid == 2
    assert new_2.manufacturer == "Hookins National Lab"
    assert new_2.model_year == 3024
    assert new_2.job == "Manager"
    assert new_2.rating == 65
    assert new_2.get_district_name() == 'business'
    assert new_2.get_superior() == c4
    assert new_2.get_direct_subordinates() == [c6]
    assert c2.get_superior() is None
    assert c2.get_direct_subordinates() == []


def test_swap_up() -> None:
    c1 = DistrictLeader(1, "Starky Industries", 3024, "Manager", 50, 'Food')
    c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 5)
    c3 = DistrictLeader(3, "Starky Industries", 3024, "Labourer", 50, "Area 51")
    c4 = Citizen(4, "Saran Labs", 3025, "Boss", 49)

    o = Society(c1)
    o.add_citizen(c2, 1)
    o.add_citizen(c3, 2)
    o.add_citizen(c4, 2)

    new_c3 = o._swap_up(c3)

    assert new_c3.get_superior() == c1
    assert new_c3.cid == 3
    assert new_c3.manufacturer == "Starky Industries"
    assert new_c3.model_year == 3024
    assert new_c3.job == "Manager"
    assert new_c3.rating == 50
    assert isinstance(new_c3, DistrictLeader) is True
    assert new_c3.get_district_name() == "Area 51"

    assert len(new_c3.get_direct_subordinates()) == 2
    assert new_c3.get_direct_subordinates()[0].cid == 2
    assert new_c3.get_direct_subordinates()[0].manufacturer == \
           "Hookins National Lab"
    assert new_c3.get_direct_subordinates()[0].model_year == 3024
    assert new_c3.get_direct_subordinates()[0].job == "Labourer"
    assert new_c3.get_direct_subordinates()[0].rating == 5
    assert isinstance(new_c3.get_direct_subordinates()[0], DistrictLeader) is \
           False
    assert new_c3.get_direct_subordinates()[1] == c4


def test_promote_citizen() -> None:
    c6 = Citizen(6, 'Star', 3036, 'CFO', 20)
    c5 = DistrictLeader(5, 'S.T.A.R.R.Y Lab', 3024, 'Manager', 50, 'Finance')
    c7 = Citizen(7, 'Hookins', 3071, 'Labourer', 60)
    c11 = Citizen(11, 'Starky', 3036, 'Repairer', 90)
    c13 = Citizen(13, 'STARRY', 3098, 'Eng', 86)

    o = Society(c6)
    o.add_citizen(c5, 6)
    o.add_citizen(c7, 5)
    o.add_citizen(c11, 7)
    o.add_citizen(c13, 7)

    o.promote_citizen(11)
    new_head = o.get_head()

    assert new_head.cid == 6

    new_head_subs = new_head.get_direct_subordinates()
    new_c11 = new_head_subs[0]

    assert isinstance(new_c11, DistrictLeader)
    assert new_c11.job == 'Manager'
    assert new_c11.get_district_name() == 'Finance'


if __name__ == '__main__':
    import pytest

    pytest.main(['a2mytests.py'])
