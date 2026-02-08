"""
Database Query Optimization Utilities

Analyzes slow queries, creates indexes, and optimizes query plans.
"""

import psycopg2
from psycopg2 import sql
from typing import List, Dict, Any, Optional
import structlog
from datetime import datetime
import json

logger = structlog.get_logger()


class QueryOptimizer:
    """Analyze and optimize database queries"""

    def __init__(self, db_url: str):
        """
        Initialize query optimizer

        Args:
            db_url: PostgreSQL connection string
        """
        self.db_url = db_url
        self.slow_query_threshold_ms = 100

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.db_url)

    def analyze_slow_queries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Find slow queries from pg_stat_statements

        Args:
            limit: Maximum number of queries to return

        Returns:
            List of slow queries with execution stats
        """
        query = """
        SELECT
            query,
            calls,
            total_exec_time,
            mean_exec_time,
            max_exec_time,
            stddev_exec_time,
            rows
        FROM pg_stat_statements
        WHERE mean_exec_time > %s
        ORDER BY mean_exec_time DESC
        LIMIT %s
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (self.slow_query_threshold_ms, limit))
                    columns = [desc[0] for desc in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]

                    logger.info(
                        "slow_queries_analyzed",
                        count=len(results),
                        threshold_ms=self.slow_query_threshold_ms
                    )

                    return results
        except psycopg2.Error as e:
            logger.error("failed_to_analyze_slow_queries", error=str(e))
            return []

    def get_missing_indexes(self) -> List[Dict[str, Any]]:
        """
        Identify missing indexes using pg_stat_user_tables

        Returns:
            List of table/column combinations that need indexes
        """
        query = """
        SELECT
            schemaname,
            tablename,
            seq_scan,
            seq_tup_read,
            idx_scan,
            seq_tup_read / NULLIF(seq_scan, 0) as avg_seq_read
        FROM pg_stat_user_tables
        WHERE seq_scan > 0
        AND schemaname = 'public'
        ORDER BY seq_tup_read DESC
        LIMIT 20
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    columns = [desc[0] for desc in cur.description]
                    results = [dict(zip(columns, row)) for row in cur.fetchall()]

                    logger.info("missing_indexes_analyzed", count=len(results))
                    return results
        except psycopg2.Error as e:
            logger.error("failed_to_get_missing_indexes", error=str(e))
            return []

    def explain_query(self, query: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Get query execution plan using EXPLAIN ANALYZE

        Args:
            query: SQL query to analyze
            params: Query parameters

        Returns:
            Query execution plan with timing
        """
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(explain_query, params)
                    result = cur.fetchone()[0]

                    plan = result[0]
                    execution_time = plan.get("Execution Time", 0)

                    logger.info(
                        "query_explained",
                        execution_time_ms=execution_time,
                        planning_time_ms=plan.get("Planning Time", 0)
                    )

                    return {
                        "plan": plan,
                        "execution_time_ms": execution_time,
                        "planning_time_ms": plan.get("Planning Time", 0),
                        "is_slow": execution_time > self.slow_query_threshold_ms
                    }
        except psycopg2.Error as e:
            logger.error("failed_to_explain_query", error=str(e))
            return {"error": str(e)}

    def create_index(
        self,
        table: str,
        columns: List[str],
        index_type: str = "btree",
        unique: bool = False,
        concurrent: bool = True
    ) -> bool:
        """
        Create database index

        Args:
            table: Table name
            columns: Column names
            index_type: Index type (btree, hash, gin, gist)
            unique: Create unique index
            concurrent: Create index without locking table

        Returns:
            True if successful
        """
        index_name = f"idx_{table}_{'_'.join(columns)}"
        columns_str = ', '.join(columns)

        query_parts = []
        if concurrent:
            query_parts.append("CREATE")
            if unique:
                query_parts.append("UNIQUE")
            query_parts.append(f"INDEX CONCURRENTLY {index_name}")
        else:
            query_parts.append("CREATE")
            if unique:
                query_parts.append("UNIQUE")
            query_parts.append(f"INDEX {index_name}")

        query_parts.append(f"ON {table}")
        query_parts.append(f"USING {index_type}")
        query_parts.append(f"({columns_str})")

        query = " ".join(query_parts)

        try:
            with self.get_connection() as conn:
                conn.autocommit = True  # Required for CREATE INDEX CONCURRENTLY
                with conn.cursor() as cur:
                    cur.execute(query)

                    logger.info(
                        "index_created",
                        table=table,
                        columns=columns,
                        index_name=index_name,
                        index_type=index_type
                    )
                    return True
        except psycopg2.Error as e:
            logger.error("failed_to_create_index", error=str(e), query=query)
            return False

    def get_table_statistics(self, table: str) -> Dict[str, Any]:
        """
        Get table statistics (size, row count, index info)

        Args:
            table: Table name

        Returns:
            Table statistics
        """
        query = """
        SELECT
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
            pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as indexes_size,
            n_live_tup as row_count,
            n_dead_tup as dead_rows,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze
        FROM pg_stat_user_tables
        WHERE tablename = %s
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (table,))
                    columns = [desc[0] for desc in cur.description]
                    result = cur.fetchone()

                    if result:
                        return dict(zip(columns, result))
                    return {}
        except psycopg2.Error as e:
            logger.error("failed_to_get_table_statistics", error=str(e), table=table)
            return {}

    def analyze_table(self, table: str) -> bool:
        """
        Run ANALYZE on table to update statistics

        Args:
            table: Table name

        Returns:
            True if successful
        """
        query = f"ANALYZE {table}"

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    logger.info("table_analyzed", table=table)
                    return True
        except psycopg2.Error as e:
            logger.error("failed_to_analyze_table", error=str(e), table=table)
            return False

    def vacuum_table(self, table: str, full: bool = False) -> bool:
        """
        Run VACUUM on table to reclaim space

        Args:
            table: Table name
            full: Run VACUUM FULL (locks table)

        Returns:
            True if successful
        """
        query = f"VACUUM {'FULL' if full else ''} {table}"

        try:
            with self.get_connection() as conn:
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(query)
                    logger.info("table_vacuumed", table=table, full=full)
                    return True
        except psycopg2.Error as e:
            logger.error("failed_to_vacuum_table", error=str(e), table=table)
            return False

    def create_view(self, view_name: str, query: str, materialized: bool = False) -> bool:
        """
        Create database view for complex queries

        Args:
            view_name: View name
            query: SELECT query
            materialized: Create materialized view

        Returns:
            True if successful
        """
        drop_query = f"DROP {'MATERIALIZED ' if materialized else ''}VIEW IF EXISTS {view_name}"
        create_query = f"CREATE {'MATERIALIZED ' if materialized else ''}VIEW {view_name} AS {query}"

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(drop_query)
                    cur.execute(create_query)
                    conn.commit()

                    logger.info(
                        "view_created",
                        view_name=view_name,
                        materialized=materialized
                    )
                    return True
        except psycopg2.Error as e:
            logger.error("failed_to_create_view", error=str(e), view_name=view_name)
            return False

    def generate_optimization_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive optimization report

        Returns:
            Report with slow queries, missing indexes, table stats
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "slow_queries": self.analyze_slow_queries(limit=20),
            "tables_needing_indexes": self.get_missing_indexes(),
            "recommendations": []
        }

        # Add recommendations based on analysis
        for table_stat in report["tables_needing_indexes"]:
            if table_stat.get("seq_scan", 0) > 1000:
                report["recommendations"].append({
                    "type": "index",
                    "priority": "high",
                    "table": table_stat["tablename"],
                    "reason": f"High sequential scans ({table_stat['seq_scan']})",
                    "action": f"Consider adding indexes to frequently queried columns"
                })

        for query in report["slow_queries"]:
            if query.get("mean_exec_time", 0) > 500:
                report["recommendations"].append({
                    "type": "query",
                    "priority": "high",
                    "query": query["query"][:100] + "...",
                    "mean_time_ms": query["mean_exec_time"],
                    "action": "Investigate and optimize slow query"
                })

        return report


def apply_recommended_indexes(db_url: str) -> None:
    """
    Apply recommended indexes for apartment transaction tables

    Args:
        db_url: Database connection string
    """
    optimizer = QueryOptimizer(db_url)

    # Recommended indexes based on common queries
    indexes = [
        # Transaction filtering
        ("transactions", ["region_code"], "btree", False),
        ("transactions", ["deal_year", "deal_month"], "btree", False),
        ("transactions", ["deal_date"], "btree", False),

        # Regional analysis
        ("transactions", ["region_code", "deal_date"], "btree", False),

        # Price queries
        ("transactions", ["deal_amount"], "btree", False),

        # Apartment search
        ("transactions", ["apt_name"], "btree", False),
        ("transactions", ["apt_name", "region_code"], "btree", False),

        # Area filtering
        ("transactions", ["exclusive_area"], "btree", False),

        # Composite for common filters
        ("transactions", ["region_code", "deal_date", "deal_amount"], "btree", False),

        # User queries (if auth enabled)
        ("users", ["email"], "btree", True),
        ("api_usage", ["user_id", "timestamp"], "btree", False),
    ]

    logger.info("applying_recommended_indexes", count=len(indexes))

    for table, columns, index_type, unique in indexes:
        success = optimizer.create_index(
            table=table,
            columns=columns,
            index_type=index_type,
            unique=unique,
            concurrent=True
        )

        if success:
            logger.info("index_applied", table=table, columns=columns)
        else:
            logger.warning("index_failed", table=table, columns=columns)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not set")
        exit(1)

    optimizer = QueryOptimizer(db_url)

    print("\n" + "="*60)
    print("DATABASE OPTIMIZATION REPORT")
    print("="*60)

    report = optimizer.generate_optimization_report()

    print(f"\nTimestamp: {report['timestamp']}")
    print(f"\nSlow Queries Found: {len(report['slow_queries'])}")
    print(f"Tables Needing Indexes: {len(report['tables_needing_indexes'])}")
    print(f"Recommendations: {len(report['recommendations'])}")

    if report['slow_queries']:
        print("\n" + "-"*60)
        print("TOP 10 SLOW QUERIES")
        print("-"*60)
        for i, query in enumerate(report['slow_queries'][:10], 1):
            print(f"\n{i}. Mean Time: {query['mean_exec_time']:.2f}ms")
            print(f"   Calls: {query['calls']}")
            print(f"   Query: {query['query'][:100]}...")

    if report['recommendations']:
        print("\n" + "-"*60)
        print("OPTIMIZATION RECOMMENDATIONS")
        print("-"*60)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"\n{i}. [{rec['priority'].upper()}] {rec['type'].upper()}")
            print(f"   {rec['reason']}")
            print(f"   Action: {rec['action']}")

    # Save report to file
    report_file = f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n\nFull report saved to: {report_file}")
