import sqlite3, random, datetime

def seed():
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS patients;
    DROP TABLE IF EXISTS claims;
    DROP TABLE IF EXISTS claim_lines;
    DROP TABLE IF EXISTS payers;
    DROP TABLE IF EXISTS providers;

    CREATE TABLE patients (
        patient_id    INTEGER PRIMARY KEY,
        mrn           TEXT NOT NULL,
        first_name    TEXT,
        last_name     TEXT,
        dob           DATE,
        gender        TEXT,
        zip_code      TEXT,
        insurance_id  INTEGER,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE payers (
        payer_id      INTEGER PRIMARY KEY,
        payer_name    TEXT NOT NULL,
        payer_type    TEXT,
        npi           TEXT,
        active        INTEGER DEFAULT 1
    );
    CREATE TABLE providers (
        provider_id   INTEGER PRIMARY KEY,
        npi           TEXT UNIQUE,
        first_name    TEXT,
        last_name     TEXT,
        specialty     TEXT,
        group_npi     TEXT
    );
    CREATE TABLE claims (
        claim_id      INTEGER PRIMARY KEY,
        patient_id    INTEGER REFERENCES patients(patient_id),
        provider_id   INTEGER REFERENCES providers(provider_id),
        payer_id      INTEGER REFERENCES payers(payer_id),
        claim_date    DATE,
        total_charges REAL,
        total_paid    REAL,
        claim_status  TEXT,
        denial_reason TEXT,
        dos_from      DATE,
        dos_to        DATE
    );
    CREATE TABLE claim_lines (
        line_id       INTEGER PRIMARY KEY,
        claim_id      INTEGER REFERENCES claims(claim_id),
        cpt_code      TEXT,
        icd10_code    TEXT,
        units         INTEGER,
        charge_amount REAL,
        paid_amount   REAL,
        line_status   TEXT
    );
    """)

    payers_data = [
        (1,"UnitedHealth","Commercial","1234567890",1),
        (2,"Aetna","Commercial","0987654321",1),
        (3,"Medicare","Government","1122334455",1),
        (4,"Medicaid","Government","5544332211",1),
    ]
    cur.executemany(
        "INSERT INTO payers VALUES (?,?,?,?,?)", payers_data)

    for i in range(1, 21):
        cur.execute(
            "INSERT INTO providers VALUES (?,?,?,?,?,?)",
            (i, f"NPI{i:010d}", "Dr", f"Provider{i}",
             random.choice(["Cardiology","Radiology","Pathology"]),
             f"GRP{i%5:05d}"))

    for i in range(1, 51):
        cur.execute(
            "INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?)",
            (i, f"MRN{i:07d}", f"First{i}", f"Last{i}",
             f"198{i%10}-0{(i%9)+1}-{(i%28)+1:02d}",
             random.choice(["M","F"]),
             f"{75000+i:05d}", random.randint(1,4),
             datetime.datetime.now().isoformat()))

    statuses = ["PAID","DENIED","PENDING","PARTIAL"]
    for i in range(1, 101):
        cur.execute(
            "INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (i, random.randint(1,50), random.randint(1,20),
             random.randint(1,4),
             f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
             round(random.uniform(100,5000),2),
             round(random.uniform(50,4000),2),
             random.choice(statuses),
             random.choice([None,None,"CO-16","CO-97","PR-2"]),
             "2024-01-01","2024-01-01"))

    conn.commit(); conn.close()
    print("Demo database seeded: demo.db")

if __name__ == "__main__":
    seed()