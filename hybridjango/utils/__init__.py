ISO_8601 = '%Y-%m-%d %H:%M'


def group_test(group_name):
    # test for user_passes_test decorator or mixin
    # checks if user is part of group
    def test(user):
        return user.groups.filter(name=group_name).exists()
    return test
