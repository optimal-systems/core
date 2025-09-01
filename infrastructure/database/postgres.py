import logging

from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from config.vars import POSTGRES_CONFIG

_LOG = logging.getLogger(__name__)
_POSTGRES_POOL: SimpleConnectionPool | None = None


def get_postgres_pool() -> SimpleConnectionPool:
    global _POSTGRES_POOL
    if _POSTGRES_POOL is None:
        cfg = POSTGRES_CONFIG
        _POSTGRES_POOL = SimpleConnectionPool(
            minconn=cfg["minconn"],
            maxconn=cfg["maxconn"],
            host=cfg["host"],
            port=cfg["port"],
            database=cfg["database"],
            user=cfg["user"],
            password=cfg["password"],
        )
        _LOG.info("Postgres pool initialized (%s@%s:%s)", cfg["database"], cfg["host"], cfg["port"])
    return _POSTGRES_POOL


def get_conn():
    return get_postgres_pool().getconn()


def put_conn(conn):
    get_postgres_pool().putconn(conn)


def execute_query(query: str, params=None, fetch: bool = True):
    conn = None
    try:
        conn = get_conn()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                if cur.description:
                    return [dict(r) for r in cur.fetchall()]
                return None
            conn.commit()
            return None
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            put_conn(conn)
