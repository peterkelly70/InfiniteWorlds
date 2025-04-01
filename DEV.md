InfiniteWorlds v2.0 Development Plan

Enhanced with SQLite, WFC, and LLM Integration
1. Key Additions & Justifications
Feature	Tech Choice	Why?
Database	SQLite3	Lightweight storage for tilesets, user maps, and generation history.
Map Algorithm	Wave Function Collapse (WFC)	Generates coherent, non-random-feeling maps (e.g., realistic cities).
LLM Integration	ChatGPT API + Ollama	Dynamic storytelling (e.g., "Generate a lore description for this dungeon").
2. Updated Architecture
High-Level Structure
Copy

infiniteworlds/  
├── core/  
│   ├── generator.py       # Now includes WFC + legacy algos (Strategy Pattern)  
│   ├── llm/               # ChatGPT/Ollama integration (Bridge Pattern)  
│   └── db/                # SQLite3 for tilesets/metadata (DAO Pattern)  
├── data/                  # SQLite DB + default tilesets  
├── plugins/               # Custom WFC constraints/LLM prompts  
└── tests/  

3. SQLite3 Implementation
Use Cases

    Tileset Storage: Store biome-specific tiles (e.g., "forest", "dungeon") with metadata.

    User Maps: Save generated maps for reuse.

    Generation History: Log seeds/parameters for reproducibility.

Schema Draft
sql
Copy

-- Tilesets  
CREATE TABLE tilesets (  
  id INTEGER PRIMARY KEY,  
  name TEXT,  
  biome_type TEXT,  -- "forest", "dungeon", etc.  
  tile_blob BLOB    -- Serialized tile adjacency rules for WFC  
);  

-- Generated Maps  
CREATE TABLE maps (  
  id INTEGER PRIMARY KEY,  
  seed TEXT,  
  params JSON,      -- CLI args/generation config  
  png_path TEXT  
);  

4. Wave Function Collapse (WFC)
Implementation Notes

    Input: Tile adjacency rules (stored in SQLite as tile_blob).

    Output: Coherent maps where tiles "make sense" (e.g., roads connect to roads).

    Libraries: Use pywavecollapse or custom implementation.

Example Workflow

    Load tileset + adjacency rules from SQLite.

    Run WFC to collapse possibilities into a valid map.

    Export to PNG + store metadata in DB.

python
Copy

# Simplified WFC call  
from core.generator import WFCGenerator  

wfc = WFCGenerator(tileset_id="forest")  
grid = wfc.generate(width=50, height=50)  

5. LLM Integration (ChatGPT + Ollama)
Use Cases

    Dynamic Descriptions: "Describe this haunted castle in 2 sentences."

    Quest Hooks: "Generate a side quest for this tavern."

    Lore Generation: "Explain the history of this dungeon."

Design

    Bridge Pattern: Switch between ChatGPT (cloud) and Ollama (local) via a common LLMInterface.

    Prompt Engineering: Store reusable prompts in SQLite.

python
Copy

from core.llm import ChatGPTAdapter, OllamaAdapter  

# Configurable LLM backend  
llm = OllamaAdapter(model="llama3") if local_llm else ChatGPTAdapter()  
response = llm.generate(  
  prompt="Describe this dungeon map in a gothic tone.",  
  context=map_metadata  
)  

6. Updated Tech Stack
Category	New Additions
Database	sqlite3 (stdlib)
WFC	pywavecollapse or custom
LLM	openai (ChatGPT), ollama (local)
7. Development Adjustments
Phase 1 (Core + WFC)

    Implement SQLite storage for tilesets.

    Integrate WFC with fallback to BSP/Drunkard’s Walk.

Phase 2 (LLM)

    Add LLMInterface with ChatGPT/Ollama adapters.

    Preload prompts for map/quest descriptions.

Phase 3 (Optimization)

    Cache frequent LLM prompts in SQLite.

    Parallelize WFC for large maps.

8. Risks & Mitigation
Risk	Solution
WFC too slow for large maps	Use smaller chunks + caching.
LLM cost/latency	Rate-limit API calls; prefer local Ollama.
SQLite scalability	Rarely an issue for single-user tools.
9. Example Code

SQLite + WFC Integration
python
Copy

import sqlite3  

def load_tileset(db_path: str, biome: str) -> list:  
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()  
    cursor.execute("SELECT tile_blob FROM tilesets WHERE biome_type=?", (biome,))  
    return pickle.loads(cursor.fetchone()[0])  # Deserialize adjacency rules  

Ollama Local LLM Call
python
Copy

from ollama import Client  

client = Client(host='http://localhost:11434')  
response = client.generate(model="llama3", prompt="Describe this map: {map_context}")  

