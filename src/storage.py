from collections import defaultdict
from typing import Dict, List

# In-memory storage for incident transcripts
# Each incident_id maps to a dictionary with lists for partial and final results
IncidentTranscripts = Dict[str, Dict[str, List[str]]]

incident_transcripts: IncidentTranscripts = defaultdict(lambda: {"partial": [], "final": []})
