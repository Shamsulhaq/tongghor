import random
import string

def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_username_generator(instance):
    Klass = instance.__class__
    if len(instance.first_name) <6:
        name = f"{instance.first_name}{instance.last_name}"
    else:
        name = instance.first_name
    u_name = name.lower().replace(" ", "0").replace(".","0")
    qs_exists = Klass.objects.filter(username=u_name).exists()
    if qs_exists:
        return f"{u_name}{random_string_generator(4)}"
    return u_name