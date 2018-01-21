import hashlib
import struct
import contextlib
from django.db import connection

@contextlib.contextmanager
def advisory_lock(lock):
    """
    Context manager to acquire a Postgres advisory lock.

    :param lock: The lock name. Can be anything convertible to a string.
      Should be scoped to the user/org and action being taken.
    :return True/False whether lock was acquired.
    """
    hasher = hashlib.sha1()
    hasher.update('{}'.format(lock).encode('utf-8'))
    int_lock = struct.unpack('q', hasher.digest()[:8])

    cur = connection.cursor()

    try:
        cur.execute('SELECT pg_try_advisory_lock(%s);', (int_lock,))
        acquired = cur.fetchall()[0][0]
        yield acquired
    finally:
        cur.execute('SELECT pg_advisory_unlock(%s);', (int_lock,))
        cur.close()
