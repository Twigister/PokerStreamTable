-- Adding extension for 
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nickname TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tables (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  config JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_id UUID NOT NULL REFERENCES tables(id),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  ended_at TIMESTAMPTZ
);

CREATE INDEX idx_sessions_table_id ON sessions(table_id);

CREATE TABLE hands (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id),
  hand_number INT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  ended_at TIMESTAMPTZ,
  hand_hash TEXT,
  UNIQUE(session_id, hand_number)
);

CREATE TABLE hand_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hand_id UUID NOT NULL REFERENCES hands(id) ON DELETE CASCADE,
    sequence_number INT NOT NULL,
    event_type TEXT NOT NULL,
    player_id UUID REFERENCES players(id),
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(hand_id, sequence_number)
);

CREATE INDEX idx_hand_events_hand_id 
ON hand_events(hand_id);

CREATE INDEX idx_hand_events_player_id 
ON hand_events(player_id);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players(id),
    session_id UUID NOT NULL REFERENCES sessions(id),
    type TEXT NOT NULL,
    amount BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_transactions_player_session
ON transactions(player_id, session_id);

CREATE TABLE player_balances (
    player_id UUID NOT NULL REFERENCES players(id),
    session_id UUID NOT NULL REFERENCES sessions(id),
    current_stack BIGINT NOT NULL DEFAULT 0,
    version INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (player_id, session_id)
);