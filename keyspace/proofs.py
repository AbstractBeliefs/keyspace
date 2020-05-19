from . import db
from collections import defaultdict

def get_proofs_for_user(userid):
    db_veris = db.query_db(
        """
            SELECT
                keys.fingerprint,
                verifications.driver,
                verifications.data,
                verifications.valid
            FROM
                keys
            LEFT JOIN
                verifications
            ON
                verifications.key = keys.id
            WHERE owner = ?
        """,
        (userid,)
    )

    key_tree = defaultdict(list)
    for veri in db_veris:
        key_tree[veri["fingerprint"]].append({"driver": veri["driver"], "data": veri["data"], "valid": veri["valid"]})

    return key_tree
