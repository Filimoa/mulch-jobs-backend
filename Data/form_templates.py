mulch_form_template = [
    {
        "id": "address",
        "type": "dropdown",
        "text": "Address (critical to get this right)",
        "options": [],
    },
    {
        "id": "crew_lead",
        "type": "dropdown",
        "text": "Crew Lead",
        "options": ["sergey", "drew"],
    },
    {"id": "time_start", "type": "time", "text": "Time Started"},
    {"id": "time_end", "type": "time", "text": "Time Ended"},
    {
        "id": "num_ppls",
        "text": "Number of Guys (including managers)",
        "type": "input",
    },
    {
        "id": "work_completed",
        "text": "Work Completed",
        "type": "dropdown",
        "options": ["mulching", "edging"],
    },
    {"id": "time_prepping", "text": "Time Spent Prepping (hours)", "type": "input"},
    {"id": "sprinklers_hit", "text": "Sprinklers Hit", "type": "input"},
    {"id": "sprinklers_unfixed", "text": "Sprinklers left to fix", "type": "input"},
    {"id": "is_cable_cut", "text": "Was cable line cut?", "type": "input"},
    {"id": "wheelbarrows", "text": "Wheelbarrows of mulch used", "type": "input"},
    {"id": "job_difficulty", "text": "Job Difficulty (1 is easy)", "type": "input"},
    {
        "id": "future_notes",
        "text": "Anything you want next years crew to know",
        "type": "input",
    },
    {
        "id": "job_completed",
        "text": "Job completed? (skip rest of questions if No)",
        "type": "dropdown",
        "options": ["true", "false"],
    },
]


edge_form_template = [
    {
        "id": "address",
        "type": "dropdown",
        "text": "Address (critical to get this right)",
        "options": ["123 Chittenden", "1188 N High St"],
    },
    {
        "id": "crew_lead",
        "type": "dropdown",
        "text": "Crew Lead",
        "options": ["sergey", "drew"],
    },
    {"id": "time_started", "type": "time", "text": "Time Started"},
    {"id": "time_ended", "type": "time", "text": "Time Ended"},
    {
        "id": "num_guys",
        "text": "Number of Guys (including managers)",
        "type": "input",
    },
    {
        "id": "work_completed",
        "text": "Work Completed",
        "type": "dropdown",
        "options": ["edging", "edging and prepping"],
    },
    {"id": "time_prepping", "text": "Time Spent Prepping (hours)", "type": "input"},
    {"id": "job_difficulty", "text": "Job Difficulty (1 is easy)", "type": "input"},
    {
        "id": "future_notes",
        "text": "Anything you want next years crew to know",
        "type": "input",
    },
    {
        "id": "job_completed",
        "text": "Job completed? (skip rest of questions if No)",
        "type": "dropdown",
        "options": ["true", "false"],
    },
]
