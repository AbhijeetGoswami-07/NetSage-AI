CREATE TABLE IF NOT EXISTS cases (
 case_id TEXT PRIMARY KEY, title TEXT NOT NULL, symptom TEXT NOT NULL, topology TEXT NOT NULL,
 show_output TEXT NOT NULL, expected_fault TEXT, osi_layer TEXT, concept TEXT, severity TEXT,
 category TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS diagnoses (
 diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(case_id),
 root_cause TEXT NOT NULL, osi_layer TEXT NOT NULL, confidence INTEGER NOT NULL, evidence TEXT NOT NULL,
 next_command TEXT NOT NULL, fix_steps TEXT NOT NULL, category TEXT NOT NULL, severity TEXT NOT NULL,
 ai_mode TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rule_results (
 rule_result_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(case_id),
 rule_name TEXT NOT NULL, status TEXT NOT NULL, severity TEXT NOT NULL, finding TEXT NOT NULL,
 evidence TEXT NOT NULL, recommendation TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reviews (
 review_id INTEGER PRIMARY KEY AUTOINCREMENT, diagnosis_id INTEGER NOT NULL REFERENCES diagnoses(diagnosis_id),
 decision TEXT NOT NULL, edited_diagnosis TEXT, reviewer_comment TEXT NOT NULL, reviewed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS verifications (
 verification_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL REFERENCES cases(case_id),
 status TEXT NOT NULL, before_result TEXT NOT NULL, after_result TEXT NOT NULL, verification_notes TEXT NOT NULL,
 verified_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS responsible_ai_logs (
 log_id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL, diagnosis_id INTEGER,
 ai_diagnosis TEXT NOT NULL, human_decision TEXT NOT NULL, corrected_diagnosis TEXT NOT NULL,
 reason_for_correction TEXT NOT NULL, lesson TEXT NOT NULL, created_at TEXT NOT NULL
);
