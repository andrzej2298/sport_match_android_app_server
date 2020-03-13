from .base import TestBase
from .data import *


class TokenTest(TestBase):
    def setUp(self) -> None:
        self.create_user()
        self.authenticate_user()
        self.add_sport(FOOTBALL)
        self.reset_authentication()

    def test_permissions(self) -> None:
        # first try without permissions
        self.add_user_sport(JOHNS_FOOTBALL, success=False)

        # try with permissions
        self.authenticate_user()
        self.add_user_sport(JOHNS_FOOTBALL, success=True)
        self.reset_authentication()

        # again without permissions
        self.add_workout(MIM_WORKOUT, success=False)

        # again with permissions
        self.authenticate_user()
        self.add_workout(MIM_WORKOUT, success=True)
        self.reset_authentication()
