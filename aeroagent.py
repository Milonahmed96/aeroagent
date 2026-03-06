"""
AeroAgent — Autonomous AOG Quoting Engine
AI-powered aviation parts pipeline using Claude + SQLite + Gradio
"""

import sqlite3
import json
import os
import anthropic
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
DB = "aeroagent.db"
MODEL = "claude-sonnet-4-5"
api_key = os.environ.get("ANTHROPIC_API_KEY")

# ── Database ──────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT UNIQUE, description TEXT, aircraft_type TEXT,
            condition TEXT, quantity INTEGER DEFAULT 0,
            price REAL, cert TEXT, alternate_pn TEXT
        );
    """)
    data = [
        ('AV-29341-A','Hydraulic Actuator Flap','Boeing 737-800','Serviceable',3,18750,'FAA 8130-3','AV-29341-B'),
        ('AV-29341-B','Hydraulic Actuator Alt','Boeing 737-800','Serviceable',1,17200,'EASA Form 1',None),
        ('GE-CF56-7B','CFM56-7B Fan Blade','Boeing 737 NG','Overhauled',0,94500,'FAA 8130-3','GE-CF56-7B-ALT'),
        ('GE-CF56-7B-ALT','CFM56-7B Fan Blade Exchange','Boeing 737 NG','Serviceable',2,88000,'FAA 8130-3',None),
        ('AIR-A320-BLV','Bleed Air Valve A320','Airbus A320','New',5,6200,'EASA Form 1',None),
        ('NGS-777-STR','Nose Gear Steering Actuator','Boeing 777','Serviceable',1,31400,'FAA 8130-3',None),
    ]
    for p in data:
        conn.execute('INSERT OR IGNORE INTO parts VALUES (NULL,?,?,?,?,?,?,?,?)', p)
    conn.commit()
    conn.close()
    print(f"DB ready: {len(data)} parts loaded")

# ── Pipeline Functions ─────────────────────────────────────────────────────────
def extract_from_email(email_text):
    """Extract structured AOG request data from unstructured email text."""
    client = anthropic.Anthropic(api_key=api_key)
    r = client.messages.create(
        model=MODEL, max_tokens=512,
        system='Extract AOG request data. Return ONLY JSON with no markdown, no backticks, no explanation: {"part_number":null,"description":null,"aircraft_type":null,"quantity":1,"airline":null,"contact":null,"urgency":"ROUTINE"}',
        messages=[{'role': 'user', 'content': f'Extract from this email:\n{email_text}'}]
    )
    raw = r.content[0].text.strip()
    if raw.startswith('```'):
        raw = raw.split('```')[1]
        if raw.startswith('json'):
            raw = raw[4:]
        raw = raw.strip()
    return json.loads(raw)

def query_db(pn, desc=None):
    """Look up part by part number, fall back to description search."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    part = conn.execute('SELECT * FROM parts WHERE UPPER(part_number)=UPPER(?)', (pn,)).fetchone()
    if not part and desc:
        part = conn.execute('SELECT * FROM parts WHERE description LIKE ?', (f'%{desc.split()[0]}%',)).fetchone()
    if not part:
        conn.close()
        return None, None
    part = dict(part)
    alt = None
    if part['quantity'] == 0 and part['alternate_pn']:
        a = conn.execute('SELECT * FROM parts WHERE part_number=?', (part['alternate_pn'],)).fetchone()
        if a:
            alt = dict(a)
    conn.close()
    return part, alt

def generate_quote(ext, part, alt):
    """Generate a professional AOG quote email using Claude."""
    active = alt if (part['quantity'] == 0 and alt) else part
    is_alt = part['quantity'] == 0 and alt is not None
    ctx = f'ALTERNATE {active["part_number"]}' if is_alt else f'IN STOCK: {active["part_number"]}'
    client = anthropic.Anthropic(api_key=api_key)
    r = client.messages.create(
        model=MODEL, max_tokens=512,
        system='You are a senior sales specialist at Eagle Jet Solutions, global AOG parts supplier.',
        messages=[{'role': 'user', 'content': f'Write professional AOG quote. Customer: {ext.get("airline","Valued Customer")}. Urgency: {ext.get("urgency")}. Part: {ctx}, Price: ${active["price"]:,.0f}, Cert: {active["cert"]}. Under 150 words.'}]
    )
    return r.content[0].text

# ── Gradio Pipeline ────────────────────────────────────────────────────────────
SAMPLES = {
    'AOG 737 Actuator': 'URGENT AOG at JFK. Need P/N AV-29341-A hydraulic actuator. Boeing 737-800. 1 unit. FAA docs. Aircraft grounded. - Mike Chen, Pacific Air',
    'OOS Engine Part':  'Emergency: GE-CF56-7B fan blade. Boeing 737 NG. Overhauled. Aircraft on ground ATL. - Sarah Johnson, Delta Ops',
    'Routine A320':     'Please quote AIR-A320-BLV x2 units. A320. New, EASA docs. Not AOG. Klaus Muller, EuroJet',
}

def pipeline(email):
    if not email.strip():
        return 'Enter email', '', '', ''
    try:
        ext = extract_from_email(email)
        part, alt = query_db(ext.get('part_number', ''), ext.get('description', ''))
        if not part:
            return json.dumps(ext, indent=2), 'Part not found in DB', 'Manual sourcing needed', 'Not Found'
        is_oos = part['quantity'] == 0
        inv = json.dumps({'primary': part, 'alternate': alt}, indent=2)
        quote = generate_quote(ext, part, alt)
        status = 'OOS + Alternate Offered' if is_oos and alt else 'OOS' if is_oos else f'In Stock ({part["quantity"]} units)'
        return json.dumps(ext, indent=2), inv, quote, status
    except Exception as e:
        import traceback
        return f'Error: {traceback.format_exc()}', '', '', 'Error'

# ── UI ─────────────────────────────────────────────────────────────────────────
def build_ui():
    with gr.Blocks(theme=gr.themes.Soft(), title='AeroAgent') as demo:
        gr.Markdown('# ✈️ AeroAgent — Autonomous AOG Quoting Engine\nAI-powered aviation parts pipeline')
        with gr.Row():
            with gr.Column():
                sample = gr.Dropdown(list(SAMPLES.keys()), label='Load Sample Email')
                email_in = gr.Textbox(label='Email Input', lines=6)
                btn = gr.Button('Run Pipeline', variant='primary')
                status = gr.Textbox(label='Status')
            with gr.Column():
                extracted = gr.Code(label='Extracted JSON', language='json')
                inventory = gr.Code(label='Inventory Result', language='json')
        quote = gr.Textbox(label='Generated Quote Email', lines=10)
        sample.change(lambda s: SAMPLES.get(s, ''), sample, email_in)
        btn.click(pipeline, email_in, [extracted, inventory, quote, status])
    return demo

# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    demo = build_ui()
    demo.launch(share=True)
