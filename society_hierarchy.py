from __future__ import annotations
from typing import List, Optional, TextIO, Any


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Preconditions:
    - <lst1>> is sorted and <lst2> is sorted.
    - All of the elements of <lst1> and <lst2> are of the same type, and they
      are comparable (i.e. their type implements __lt__).

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """

    i1 = 0
    i2 = 0
    new_list = []

    while i1 < len(lst1) and i2 < len(lst2):
        if lst1[i1] < lst2[i2]:
            new_list.append(lst1[i1])
            i1 += 1
        else:
            new_list.append(lst2[i2])
            i2 += 1

    new_list.extend(lst1[i1:])
    new_list.extend(lst2[i2:])

    return new_list


###########################################################################
###########################################################################
class Citizen:
    """A Citizen: a citizen in a Society.

    === Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - cid > 0
    - 0 <= rating <= 100
    - self._subordinates is in ascending order by the subordinates' IDs
    - If _superior is a Citizen, this Citizen is part of its _subordinates list
    - Each Citizen in _subordinates has this Citizen as its _superior
    """
    cid: int
    manufacturer: str
    model_year: int
    job: str
    rating: int
    _superior: Optional[Citizen]
    _subordinates: List[Citizen]

    def __init__(self, cid: int, name: str, model_year: int,
                 job: str, rating: int) -> None:
        """Initialize this Citizen with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, and rating <rating>.

        A Citizen initially has no superior and no subordinates.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c1.cid
        1
        >>> c1.rating
        50
        """
        self.cid = cid
        self.manufacturer = name
        self.model_year = model_year
        self.job = job
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Any) -> bool:
        """Return True if <other> is a Citizen and this Citizen's cid is less
        than <other>'s cid.

        If other is not a Citizen, raise a TypeError.

        >>> c1 = Citizen(1, "Starky Industries", 3042, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3042, "Manager", 30)
        >>> c1 < c2
        True
        """
        if not isinstance(other, Citizen):
            raise TypeError

        return self.cid < other.cid

    def __str__(self) -> str:
        """Return a string representation of the tree rooted at this Citizen.
        """
        return self._str_indented().strip()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        me = f'{str(self.cid)} (rating = {self.rating})'
        if isinstance(self, DistrictLeader):
            me += f' --> District Leader for {self._district_name}'
        s = '  ' * depth + me + '\n'
        for subordinate in self.get_direct_subordinates():
            # Note that the ‘depth’ argument to the recursive call is
            # modified.
            s += subordinate._str_indented(depth + 1)
        return s

    def get_superior(self) -> Optional[Citizen]:
        """Return the superior of this Citizen or None if no superior exists.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c1.get_superior() is None
        True
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_superior().cid
        2
        """
        return self._superior

    def set_superior(self, new_superior: Optional[Citizen]) -> None:
        """Update the superior of this Citizen to <new_superior>

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.set_superior(c2)
        >>> c1.get_superior().cid
        2
        """
        self._superior = new_superior
        # QUESTION: this does not maintain the representation invariant
        # since new_superior does not have self in new_superior._subordinates

    def get_direct_subordinates(self) -> List[Citizen]:
        """Return a new list containing the direct subordinates of this Citizen.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_direct_subordinates()[0].cid
        2
        """
        return self._subordinates[:]

    ###########################################################################
    # While not called by the client code, these methods may be helpful to
    # you and will be tested. You can (and should) call them in the other
    # methods that you implement when appropriate.
    ###########################################################################

    def add_subordinate(self, subordinate: Citizen) -> None:
        """Add <subordinate> to this Citizen's list of direct subordinates,
        keeping the list of subordinates in ascending order by their ID.

        Update the new subordinate's superior to be this Citizen.

        Pre-condition: subordinate._superior is None

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c2.add_subordinate(c1)
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c1.get_superior() is c2
        True
        """
        # This is a function I wrote
        self._subordinates = merge(self._subordinates, [subordinate])
        subordinate.set_superior(self)

    def remove_subordinate(self, cid: int) -> None:
        """Remove the direct subordinate with the ID <cid> from this Citizen's
        list of subordinates.

        Furthermore, remove that (former) subordinate from the hierarchy by
        setting its superior to None.

        Precondition: This Citizen has a subordinate with ID <cid>.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c2.remove_subordinate(1)
        >>> c2.get_direct_subordinates()
        []
        >>> c1.get_superior() is None
        True
        """
        # This is a function I wrote :)
        # Needs testing
        for subordinate in self._subordinates:
            if subordinate.cid == cid:
                self._subordinates.remove(subordinate)
                subordinate.set_superior(None)
                return None
        return None

    def become_subordinate_to(self, superior: Optional[Citizen]) -> None:
        """Make this Citizen a direct subordinate of <superior>.

        If this Citizen already had a superior, remove this Citizen from the
        old superior's list of subordinates.

        If <superior> is None, just set this Citizen's superior to None.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_superior().cid
        2
        >>> c2.get_direct_subordinates()[0].cid
        1
        >>> c1.become_subordinate_to(None)
        >>> c1.get_superior() is None
        True
        >>> c2.get_direct_subordinates()
        []
        """
        # This is a function I wrote :)

        # Removing self from its superior's subordinates, if not None
        if self._superior is not None:
            self._superior.remove_subordinate(self.cid)

        # Adding self to superior._subordinates and self._superior now refers
        # to superior
        if superior is None:
            self.set_superior(superior)
        else:
            superior.add_subordinate(self)

    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Check this Citizen and its subordinates to find and return the
        Citizen that has the ID <cid>.

        If neither this Citizen nor any of its subordinates (both direct and
        indirect) have the ID <cid>, return None.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_citizen(1) is c1
        True
        >>> c2.get_citizen(3) is None
        True
        """
        # Note: This method must call itself recursively
        # This is a function I wrote
        if self.cid == cid:
            return self
        else:
            for subordinate in self._subordinates:
                if subordinate.get_citizen(cid) is not None:
                    return subordinate.get_citizen(cid)
            return None

    ###########################################################################
    ###########################################################################

    def get_all_subordinates(self) -> List[Citizen]:
        """Return a new list of all of the subordinates of this Citizen in
        order of ascending IDs.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_all_subordinates()[0].cid
        1
        >>> c3.get_all_subordinates()[1].cid
        2
        """
        # Note: This method must call itself recursively

        # Hints:
        # - Recall that each Citizen's subordinates list is sorted in ascending
        #   order.
        # - Use the merge helper function.

        # This is a function I wrote :)
        # needs testing
        lst = self._subordinates[:]
        for subordinate in self._subordinates:
            lst = merge(lst, subordinate.get_all_subordinates())
        return lst

    def get_society_head(self) -> Citizen:
        """Return the head of the Society (i.e. the top-most superior Citizen,
        a.k.a. the root of the hierarchy).

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c1.get_society_head().cid
        3
        """
        # Note: This method must call itself recursively
        # This is a function I wrote :)
        # needs testing
        if self._superior is None:
            return self
        else:
            return self._superior.get_society_head()

    def get_closest_common_superior(self, cid: int) -> Citizen:
        """Return the closest common superior that this Citizen and the
        Citizen with ID <cid> share.

        If this Citizen is the superior of <cid>, return this Citizen.

        Pre-condition: a Citizen with ID <cid> exists in the hierarchy

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Commander", 60)
        >>> c4 = Citizen(4, "Starky Industries", 3022, "Manager", 55)
        >>> c5 = Citizen(5, "Hookins National Lab", 3023, "Engineer", 50)
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c4.become_subordinate_to(c3)
        >>> c5.become_subordinate_to(c4)
        >>> c3.get_closest_common_superior(1) == c3
        True
        >>> c3.get_closest_common_superior(3) == c3
        True
        >>> c1.get_closest_common_superior(5) == c3
        True
        """
        # Note: This method must call itself recursively
        # I wrote this function :)
        # Tested! :)
        lst = self.get_all_subordinates()
        lst.append(self)
        for citizen in lst:
            if citizen.cid == cid:
                return self

        return self._superior.get_closest_common_superior(cid)

    ###########################################################################
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the immediate district that the Citizen belongs to (or
        leads).

        If the Citizen is not part of any districts, return an empty string.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.get_district_name()
        ''
        >>> c1.become_subordinate_to(c2)
        >>> c1.get_district_name()
        'District A'
        """
        # Note: This method must call itself recursively
        # I wrote this function :)
        if self._superior is None:
            return ''
        else:
            return self._superior.get_district_name()

    def rename_district(self, district_name: str) -> None:
        """Rename the immediate district which this Citizen is a part of to
        <district_name>.

        If the Citizen is not part of a district, do nothing.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", \
        30, "District A")
        >>> c1.become_subordinate_to(c2)
        >>> c1.rename_district('District B')
        >>> c1.get_district_name()
        'District B'
        >>> c2.get_district_name()
        'District B'
        """
        # Note: This method must call itself recursively
        # This is a function I wrote :)
        if self._superior is None:
            return None
        else:
            return self._superior.rename_district(district_name)

    ###########################################################################
    ###########################################################################
    def get_highest_rated_subordinate(self) -> Citizen:
        """Return the direct subordinate of this Citizen with the highest
        rating.

        Precondition: This Citizen has at least one subordinate.

        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = DistrictLeader(2, "Hookins National Lab", 3024, "Manager", 30,
        ... "District A")
        >>> c3 = DistrictLeader(3, "S.T.A.R.R.Y Lab", 3000, "Commander", 60,
        ... "District X")
        >>> c1.become_subordinate_to(c2)
        >>> c2.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Hookins National Lab'
        >>> c1.become_subordinate_to(c3)
        >>> c3.get_highest_rated_subordinate().manufacturer
        'Starky Industries'
        """
        # Hint: This can be used as a helper function for `delete_citizen`
        # This is a function I wrote :)
        subs = self.get_direct_subordinates()

        highest_rating = 0
        highest_rating_sub = None

        for sub in subs:
            if sub.rating > highest_rating:
                highest_rating = sub.rating
                highest_rating_sub = sub

        return highest_rating_sub


class Society:
    """A society containing citizens in a hierarchy.

    === Private Attributes ===
    _head:
        The root of the hierarchy, which we call the "head" of the Society.
        If _head is None, this indicates that this Society is empty (there are
        no citizens in this Society).

    === Representation Invariants ===
    - No two Citizens in this Society have the same cid.
    """
    _head: Optional[Citizen]

    def __init__(self, head: Optional[Citizen] = None) -> None:
        """Initialize this Society with the head <head>.

        >>> o = Society()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def __str__(self) -> str:
        """Return a string representation of this Society's tree.

        For each node, its item is printed before any of its descendants'
        items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return str(self._head)

    ###########################################################################
    # You may use the methods below as helper methods if needed.
    ###########################################################################
    def get_head(self) -> Optional[Citizen]:
        """Return the head of this Society.
        """
        return self._head

    def set_head(self, new_head: Citizen) -> None:
        """Set the head of this Society to <new_head>.
        """
        self._head = new_head

    ###########################################################################
    ###########################################################################
    def get_citizen(self, cid: int) -> Optional[Citizen]:
        """Return the Citizen in this Society who has the ID <cid>. If no such
        Citizen exists, return None.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024,  "Labourer", 50)
        >>> o.add_citizen(c1)
        >>> o.get_citizen(1) is c1
        True
        >>> o.get_citizen(2) is None
        True
        """
        # Hint: Recall that self._head is a Citizen object, so any of Citizen's
        # methods can be used as a helper method here.
        # I wrote this method :)
        if self._head is None:
            return None
        else:
            return self._head.get_citizen(cid)

    def get_all_citizens(self) -> List[Citizen]:
        """Return a list of all citizens, in order of increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.add_citizen(c6, 2)
        >>> o.add_citizen(c1, 4)
        >>> o.add_citizen(c3, 1)
        >>> o.add_citizen(c5, 1)
        >>> o.get_all_citizens() == [c1, c2, c3, c4, c5, c6]
        True
        """
        # This is a method I wrote :)
        if self._head is None:
            return []
        else:
            return merge([self._head], self._head.get_all_subordinates())

    def add_citizen(self, citizen: Citizen, superior_id: int = None) -> None:
        """Add <citizen> to this Society as a subordinate of the Citizen with
        ID <superior_id>.

        If no <superior_id> is provided, make <citizen> the new head of this
        Society, with the original head becoming the one and only subordinate
        of <citizen>.

        Preconditions:
        - citizen.get_superior() is None.
        - if <superior_id> is not None, then the Society contains a Citizen with
          ID <superior_id>.
        - Society does not already contain any Citizen with the same ID as
          <citizen>.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Labourer", 50)
        >>> c2 = Citizen(2, "Some Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c2)
        >>> o.get_head() is c2
        True
        >>> o.add_citizen(c1, 2)
        >>> o.get_head() is c2
        True
        >>> o.get_citizen(1) is c1
        True
        >>> c1.get_superior() is c2
        True
        """
        # I wrote this function :)
        if superior_id is None:
            head_holder = self._head  # placeholder for old society head
            self._head = citizen

            # clears the subordinates of citizen
            for subordinate in citizen.get_direct_subordinates():
                citizen.remove_subordinate(subordinate.cid)

            # adds old society head as only subordinate
            if head_holder is not None:
                citizen.add_subordinate(head_holder)
        else:  # Can assume superior_id is not None
            superior = self._head.get_citizen(superior_id)
            # Note that superior is not None by assumption of pre-condition
            superior.add_subordinate(citizen)

    def get_citizens_with_job(self, job: str) -> List[Citizen]:
        """Return a list of all citizens with the job <job>, in order of
        increasing cid.

        >>> o = Society()
        >>> c1 = Citizen(1, "Starky Industries", 3024, "Manager", 50)
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Manager", 65)
        >>> c3 = Citizen(3, "Starky Industries", 3024, "Labourer", 50)
        >>> c4 = Citizen(4, "S.T.A.R.R.Y Lab", 3024, "Manager", 30)
        >>> c5 = Citizen(5, "Hookins National Lab", 3024, "Labourer", 50)
        >>> c6 = Citizen(6, "S.T.A.R.R.Y Lab", 3024, "Lawyer", 30)
        >>> o.add_citizen(c4, None)
        >>> o.add_citizen(c2, 4)
        >>> o.add_citizen(c6, 2)
        >>> o.add_citizen(c1, 4)
        >>> o.add_citizen(c3, 1)
        >>> o.add_citizen(c5, 1)
        >>> o.get_citizens_with_job('Manager') == [c1, c2, c4]
        True
        """
        # I wrote this function :)
        citizen_lst = self.get_all_citizens()
        lst = []
        for citizen in citizen_lst:
            if citizen.job == job:
                lst = merge(lst, [citizen])
        return lst

    ###########################################################################
    ###########################################################################
    def change_citizen_type(self, cid: int,
                            district_name: Optional[str] = None) -> Citizen:
        """Change the type of the Citizen with the given <cid>

        If the Citizen is currently a DistrictLeader, change them to become a
        regular Citizen (with no district name). If they are currently a regular
        Citizen, change them to become DistrictLeader for <district_name>.
        Note that this requires creating a new object of type either Citizen
        or DistrictLeader.

        The new Citizen/DistrictLeader should keep the same placement in the
        hierarchy (that is, the same superior and subordinates) that the
        original Citizen had, as well as the same ID, manufacturer, model year,
        job, and rating.

        Return the newly created Citizen/DistrictLeader.

        The original citizen that's being replaced should no longer be in the
        hierarchy (it should not be anyone's subordinate nor superior).

        Precondition:
        - If <cid> is the id of a DistrictLeader, <district_name> must be None
        """
        # I wrote this function :)
        citizen = self.get_citizen(cid)
        cit_superior = citizen.get_superior()

        if isinstance(citizen, DistrictLeader):
            # Create new Citizen object
            new_citizen = Citizen(citizen.cid, citizen.manufacturer,
                                  citizen.model_year, citizen.job,
                                  citizen.rating)
        else:  # So citizen is not a DistrictLeader
            new_citizen = DistrictLeader(citizen.cid, citizen.manufacturer,
                                         citizen.model_year, citizen.job,
                                         citizen.rating, district_name)

        # remove subordinates of citizen and add them to new_citizen
        subordinate_lst = citizen.get_direct_subordinates()
        for subordinate in subordinate_lst:
            citizen.remove_subordinate(subordinate.cid)
            new_citizen.add_subordinate(subordinate)

        # remove citizen from subordinates of cit_superior and add
        # new_citizen as a subordinate to cit_superior
        if cit_superior is not None:
            cit_superior.remove_subordinate(citizen.cid)
            cit_superior.add_subordinate(new_citizen)

        return new_citizen

    ###########################################################################
    ###########################################################################
    def _swap_up(self, citizen: Citizen) -> Citizen:
        """Swap <citizen> with their superior in this Society (they should
         swap their job, and their position in the tree, but otherwise keep
         all the same attribute data they currently have).

        If the superior is a DistrictLeader, the citizens being swapped should
        also switch their citizen type (i.e. the DistrictLeader becomes a
        regular Citizen and vice versa).

        Return the Citizen after it has been swapped up ONCE in the Society.

        Precondition:
        - <citizen> has a superior (i.e., it is not the head of this Society),
          and is not a DistrictLeader.
        """
        # Note: depending on how you implement this method, PyCharm may warn you
        # that this method 'may be static' -- feel free to ignore this
        # I wrote this function :)
        csup = citizen.get_superior()
        csupsup = csup.get_superior()

        # If csup is a district leader, then switch the types of both citizen
        # and csup, from district leader to normal citizen and vice versa
        if isinstance(csup, DistrictLeader):
            citizen = self.change_citizen_type(citizen.cid,
                                               csup.get_district_name())
            csup = self.change_citizen_type(csup.cid)

        # Disconnect csup and citizen
        csup.remove_subordinate(citizen.cid)

        # Disconnect csup from its superior
        if csupsup is not None:
            csupsup.remove_subordinate(csup.cid)

        # Disconnect csup from its subordinates and save them
        csup_subs = csup.get_direct_subordinates()
        for sub in csup_subs:
            csup.remove_subordinate(sub.cid)

        # Disconnect citizen from its subordinates and save them
        citizen_subs = citizen.get_direct_subordinates()
        for sub in citizen_subs:
            citizen.remove_subordinate(sub.cid)

        # Attach csup_subs to citizen
        for sub in csup_subs:
            citizen.add_subordinate(sub)

        # Attach citizen_subs to csup
        for sub in citizen_subs:
            csup.add_subordinate(sub)

        # Attach citizen to csupsup
        if csupsup is not None:
            citizen.become_subordinate_to(csupsup)

        # Attach csup to citizen
        csup.become_subordinate_to(citizen)

        # Change job titles
        citizen_job_holder = citizen.job
        citizen.job = csup.job
        csup.job = citizen_job_holder

        return citizen

    def promote_citizen(self, cid: int) -> None:
        """Promote the Citizen with cid <cid> until they either:
             - have a superior with a higher rating than them or,
             - become DistrictLeader for their district.
        See the Assignment 2 handout for further details.

        Precondition: There is a Citizen with the cid <cid> in this Society.
        """
        # This is a function I wrote :)
        citizen = self.get_citizen(cid)
        csup = citizen.get_superior()

        while csup is not None and csup.rating < citizen.rating and \
                not isinstance(citizen, DistrictLeader):
            citizen = self._swap_up(citizen)
            csup = citizen.get_superior()

    ###########################################################################
    ###########################################################################

    def delete_citizen(self, cid: int) -> None:
        """Remove the Citizen with ID <cid> from this Society.

        If this Citizen has subordinates, their subordinates become subordinates
        of this Citizen's superior.

        If this Citizen is the head of the Society, their most highly rated
        direct subordinate becomes the new head. If they did not have any
        subordinates, the society becomes empty (the society head becomes None).

        Precondition: There is a Citizen with the cid <cid> in this Society.
        """
        citizen = self.get_citizen(cid)
        csup = citizen.get_superior()

        if csup is None:
            if not citizen.get_direct_subordinates():
                self._head = None
            else:
                highest_rated_sub = citizen.get_highest_rated_subordinate()
                self._head = highest_rated_sub
        else:
            citizen_subs = citizen.get_direct_subordinates()

            # disconnect all subs in citizen_subs from citizen
            for sub in citizen_subs:
                citizen.remove_subordinate(sub.cid)

            # disconnect citizen from csup
            csup.remove_subordinate(citizen.cid)

            # connect all subs in citizen_subs to csup
            for sub in citizen_subs:
                csup.add_subordinate(sub)


###############################################################################
###############################################################################
class DistrictLeader(Citizen):
    """The leader of a district in a society.

    === Private Attributes ===
    _district_name:
        The name of the district that this DistrictLeader is the leader of.

    === Inherited Public Attributes ===
    cid:
        The ID number of this citizen.
    manufacturer:
        The manufacturer of this Citizen.
    model_year:
        The model year of this Citizen.
    job:
        The name of this Citizen's job within the Society.
    rating:
        The rating of this Citizen.

    === Inherited Private Attributes ===
    _superior:
        The superior of this Citizen in the society, or None if this Citizen
        does not have a superior.
    _subordinates:
        A list of this Citizen's direct subordinates (that is, Citizens that
        work directly under this Citizen).

    === Representation Invariants ===
    - All Citizen RIs are inherited.
    """
    _district_name: str

    ###########################################################################
    ###########################################################################
    def __init__(self, cid: int, manufacturer: str, model_year: int,
                 job: str, rating: int, district: str) -> None:
        """Initialize this DistrictLeader with the ID <cid>, manufacturer
        <manufacturer>, model year <model_year>, job <job>, rating <rating>, and
        district name <district>.

        >>> c2 = DistrictLeader(2, "Some Lab", 3024, "Lawyer", 30, "District A")
        >>> c2.manufacturer
        'Some Lab'
        >>> c2.get_district_name()
        'District A'
        """
        # This is a function I wrote :)
        Citizen.__init__(self, cid, manufacturer, model_year, job, rating)
        self._district_name = district

    def get_district_citizens(self) -> List[Citizen]:
        """Return a list of all citizens in this DistrictLeader's district, in
        increasing order of cid.

        Include the cid of this DistrictLeader in the list.

        >>> c1 = DistrictLeader(
        ...     1, "Hookins National Lab", 3024, "Commander", 65, "District A"
        ... )
        >>> c2 = Citizen(2, "Hookins National Lab", 3024, "Lawyer", 30)
        >>> c3 = Citizen(3, "S.T.A.R.R.Y Lab", 3010, "Labourer", 55)
        >>> c2.become_subordinate_to(c1)
        >>> c3.become_subordinate_to(c1)
        >>> c1.get_district_citizens() == [c1, c2, c3]
        True
        """
        # This is a function I wrote :)
        return merge([self], self.get_all_subordinates())

    ###########################################################################
    ###########################################################################
    def get_district_name(self) -> str:
        """Return the name of the district that this DistrictLeader leads.
        """
        # This is a function I wrote :)
        return self._district_name

    def rename_district(self, district_name: str) -> None:
        """Rename this district leader's district to the given <district_name>.
        """
        # This is a function I wrote :)
        self._district_name = district_name


###########################################################################
# ALL PROVIDED FUNCTIONS BELOW ARE COMPLETE, DO NOT CHANGE
###########################################################################
def create_society_from_file(file: TextIO) -> Society:
    """Return the Society represented by the information in file.

    >>> o = create_society_from_file(open('citizens.csv'))
    >>> o.get_head().manufacturer
    'Hookins National Lab'
    >>> len(o.get_head().get_all_subordinates())
    11
    """
    head = None
    people = {}
    for line in file:
        info: List[Any] = line.strip().split(',')
        info[0] = int(info[0])
        info[2] = int(info[2])
        info[4] = int(info[4])

        if len(info) == 7:
            inf = info[:5] + info[-1:]
            person = DistrictLeader(*inf)
        else:
            person = Citizen(*info[:5])

        superior = info[5]
        if not info[5]:
            head = person
            superior = None
        else:
            superior = int(superior)
        people[info[0]] = (person, superior)

    for key in people:
        if people[key][1] is not None:
            people[people[key][1]][0].add_subordinate(people[key][0])

    return Society(head)


###########################################################################
# Sample societies from the handout
###########################################################################
def simple_society_demo() -> Society:
    """Handout example related to a simple society.
    """
    c = Citizen(6, "Starky Industries", 3036, "Commander", 50)
    c2 = Citizen(2, "Hookins National", 3027, "Manager", 55)
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = Citizen(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17)
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def district_society_demo() -> Society:
    """Handout example related to a simple society with districts.
    """
    c = DistrictLeader(6, "Starky Industries", 3036, "Commander", 50, "Area 52")
    c2 = DistrictLeader(2, "Hookins National", 3027, "Manager", 55,
                        "Repair Support")
    c3 = Citizen(3, "Starky Industries", 3050, "Labourer", 50)
    c4 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 17, "Finance")
    c5 = Citizen(8, "Hookins National", 3024, "Cleaner", 74)
    c6 = Citizen(7, "Hookins National", 3071, "Labourer", 5)
    c7 = Citizen(9, "S.T.A.R.R.Y Lab", 3098, "Engineer", 86)

    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 6)
    s.add_citizen(c4, 6)
    s.add_citizen(c5, 6)
    s.add_citizen(c6, 5)
    s.add_citizen(c7, 5)

    return s


def promote_citizen_demo() -> Society:
    """Handout example related to promote_citizen.
    """
    c = DistrictLeader(6, "Star", 3036, "CFO", 20, "Area 52")
    c2 = DistrictLeader(5, "S.T.A.R.R.Y Lab", 3024, "Manager", 50, "Finance")
    c3 = Citizen(7, "Hookins", 3071, "Labourer", 60)
    c4 = Citizen(11, "Starky", 3036, "Repairer", 90)
    c5 = Citizen(13, "STARRY", 3098, "Eng", 86)
    s = Society()
    s.add_citizen(c)
    s.add_citizen(c2, 6)
    s.add_citizen(c3, 5)
    s.add_citizen(c4, 7)
    s.add_citizen(c5, 7)

    s.promote_citizen(11)
    return s


def create_from_file_demo() -> Society:
    """Handout example related to reading from the provided file citizens.csv.
    """
    return create_society_from_file(open("citizens.csv"))


if __name__ == "__main__":
    # As you complete your tasks, you can uncomment any of the function calls
    # and the print statement below to create and print out a sample society:
    # soc = simple_society_demo()
    # soc = district_society_demo()
    # soc = promote_citizen_demo()
    # soc = create_from_file_demo()
    # print(soc)

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['typing', '__future__',
                                   'python_ta', 'doctest'],
        'disable': ['E9998', 'R0201'],
        'max-args': 7,
        'max-module-lines': 1600
    })
