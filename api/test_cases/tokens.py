from .base import TestBase
from .data import *


class TokenTest(TestBase):
    def setUp(self) -> None:
        self.create_user()

    def test_permissions(self) -> None:
        # first try without permissions
        self.add_user_sport(JOHNS_RUNNING, success=False)

        # try with permissions
        self.authenticate_user()
        self.add_user_sport(JOHNS_RUNNING, success=True)
        self.reset_authentication()

        # again without permissions
        self.add_workout(MIM_WORKOUT, success=False)

        # again with permissions
        self.authenticate_user()
        self.add_workout(MIM_WORKOUT, success=True)
        self.reset_authentication()
