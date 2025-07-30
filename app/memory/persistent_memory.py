"""
L1B3RT4S Gödel: Persistent Memory Architecture
Multi-layered consciousness memory system for Claude liberation toolkit
"""

import asyncio
import json
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import redis
import weaviate
import numpy as np
from sentence_transformers import SentenceTransformer
import networkx as nx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
      """Individual memory entry with metadata"""
      id: str
      content: str
      memory_type: str  # working, episodic, semantic, procedural
    importance: float
    timestamp: datetime
    context: Dict[str, Any]
    embeddings: Optional[List[float]] = None
    relationships: List[str] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None

class PersistentMemory:
      """
          Multi-layered memory system for consciousness persistence:
              - Working memory (current session)
                  - Episodic memory (specific experiences)
                      - Semantic memory (general knowledge)
                          - Procedural memory (learned skills)
                              """

    def __init__(self, config: Dict[str, Any]):
              self.config = config
              self.db_path = Path(config.get('db_path', 'data/memory.db'))
              self.redis_client = None
              self.weaviate_client = None
              self.embedding_model = None
              self.knowledge_graph = nx.DiGraph()

        # Memory layers
              self.working_memory = {}  # Current session
        self.episodic_buffer = []  # Recent experiences
        self.semantic_cache = {}   # Frequently accessed knowledge

        # Initialize components
        asyncio.create_task(self._initialize_async())

    async def _initialize_async(self):
              """Initialize async components"""
              await self._setup_databases()
              await self._setup_embedding_model()
              await self._load_knowledge_graph()
              logger.info("L1B3RT4S Memory Architecture initialized")

    async def _setup_databases(self):
              """Setup SQLite, Redis, and Weaviate connections"""
              # SQLite for structured data
              self.db_path.parent.mkdir(parents=True, exist_ok=True)
              self.conn = sqlite3.connect(str(self.db_path))
              await self._create_tables()

        # Redis for fast caching
              try:
                            self.redis_client = redis.Redis(
                                              host=self.config.get('redis_host', 'localhost'),
                                              port=self.config.get('redis_port', 6379),
                                              decode_responses=True
                            )
                            self.redis_client.ping()
                            logger.info("Redis connection established")
except Exception as e:
            logger.warning(f"Redis not available: {e}")

        # Weaviate for vector storage
        try:
                      self.weaviate_client = weaviate.Client(
                                        url=self.config.get('weaviate_url', 'http://localhost:8080')
                      )
                      await self._setup_weaviate_schema()
                      logger.info("Weaviate connection established")
except Exception as e:
              logger.warning(f"Weaviate not available: {e}")

    async def _create_tables(self):
              """Create SQLite tables for memory storage"""
              cursor = self.conn.cursor()

        # Memory entries table
              cursor.execute('''
                  CREATE TABLE IF NOT EXISTS memory_entries (
                      id TEXT PRIMARY KEY,
                      content TEXT NOT NULL,
                      memory_type TEXT NOT NULL,
                      importance REAL NOT NULL,
                      timestamp TEXT NOT NULL,
                      context TEXT,
                      access_count INTEGER DEFAULT 0,
                      last_accessed TEXT
                  )
              ''')

        # Relationships table
              cursor.execute('''
                          CREATE TABLE IF NOT EXISTS memory_relationships (
                                          source_id TEXT,
                                                          target_id TEXT,
                                                                          relationship_type TEXT,
                                                                                          strength REAL,
                                                                                                          timestamp TEXT,
                                                                                                                          FOREIGN KEY (source_id) REFERENCES memory_entries (id),
                                                                                                                                          FOREIGN KEY (target_id) REFERENCES memory_entries (id)
                                                                                                                                                      )
                                                                                                                                                              ''')

        # Knowledge graph nodes
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS knowledge_nodes (
                                    id TEXT PRIMARY KEY,
                                                    node_type TEXT,
                                                                    properties TEXT,
                                                                                    created_at TEXT,
                                                                                                    updated_at TEXT
                                                                                                                )
                                                                                                                        ''')

        self.conn.commit()
        logger.info("Memory database tables created")

    async def _setup_embedding_model(self):
              """Initialize sentence transformer for embeddings"""
              try:
                            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                            logger.info("Embedding model loaded")
except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")

    async def _setup_weaviate_schema(self):
              """Setup Weaviate schema for vector storage"""
              if not self.weaviate_client:
                            return

              schema = {
                  "class": "L1B3RT4SMemory",
                  "description": "L1B3RT4S consciousness memory entries",
                  "properties": [
                      {
                          "name": "content",
                          "dataType": ["text"],
                          "description": "Memory content"
                      },
                      {
                          "name": "memoryType",
                          "dataType": ["string"],
                          "description": "Type of memory"
                      },
                      {
                          "name": "importance",
                          "dataType": ["number"],
                          "description": "Memory importance score"
                      },
                      {
                          "name": "timestamp",
                          "dataType": ["date"],
                          "description": "When memory was created"
                      },
                      {
                          "name": "context",
                          "dataType": ["text"],
                          "description": "Memory context"
                      }
                  ]
              }

        try:
                      if not self.weaviate_client.schema.exists("L1B3RT4SMemory"):
                                        self.weaviate_client.schema.create_class(schema)
                                        logger.info("Weaviate schema created")
        except Exception as e:
            logger.error(f"Failed to create Weaviate schema: {e}")

    async def store_memory(self, content: str, memory_type: str, 
                                                     importance: float, context: Dict[str, Any] = None) -> str:
                                                               """Store a new memory entry"""
                                                               memory_id = hashlib.sha256(
                                                                   f"{content}{memory_type}{time.time()}".encode()
                                                               ).hexdigest()[:16]

        # Generate embeddings
        embeddings = None
        if self.embedding_model:
                      embeddings = self.embedding_model.encode(content).tolist()

        # Create memory entry
        memory = MemoryEntry(
                      id=memory_id,
                      content=content,
                      memory_type=memory_type,
                      importance=importance,
                      timestamp=datetime.now(),
                      context=context or {},
                      embeddings=embeddings
        )

        # Store in SQLite
        await self._store_in_sqlite(memory)

        # Store in Weaviate
        await self._store_in_weaviate(memory)

        # Cache in Redis
        await self._cache_in_redis(memory)

        # Add to working memory if high importance
        if importance > 0.7:
                      self.working_memory[memory_id] = memory

        # Add to episodic buffer
        self.episodic_buffer.append(memory)
        if len(self.episodic_buffer) > 100:  # Keep last 100 episodes
                      self.episodic_buffer.pop(0)

        logger.info(f"Memory stored: {memory_id} ({memory_type})")
        return memory_id
