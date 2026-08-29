# Test Report

The suite covers database schema creation, structured diagnosis validation, category classification, duplicate IP/VLAN/interface/ACL rules, review validation, verification states, and the core end-to-end workflow.

Run with `pytest -q`. The actual pass/fail count must be taken from the local test run because it depends on the installed environment. Tests intentionally use no API key and do not call a live provider.
