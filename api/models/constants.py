# User constants
MALE = 'M'
FEMALE = 'F'
EITHER = 'E'

GENDERS = [
    (MALE, 'male'),
    (FEMALE, 'female'),
]

WORKOUT_GENDER_PREFERENCES = GENDERS + [(EITHER, 'either')]


# ParticipationRequest constants
PENDING = 'P'
ACCEPTED = 'A'
REJECTED = 'R'

STATUSES = [
    (PENDING, 'pending'),
    (ACCEPTED, 'accepted'),
    (REJECTED, 'rejected'),
]
