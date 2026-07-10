-- Atlas Database Schema
-- Phase 0: Core tables for research runs and evidence

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Research runs table
CREATE TABLE runs (
    run_id UUID PRIMARY KEY,
    company_id VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    ticker VARCHAR(20),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    error TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_runs_company ON runs(company_id);
CREATE INDEX idx_runs_status ON runs(status);
CREATE INDEX idx_runs_started_at ON runs(started_at DESC);

-- Agent reports table
CREATE TABLE agent_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    agent VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    summary TEXT,
    signals JSONB DEFAULT '{}'::jsonb,
    error TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_agent_reports_run ON agent_reports(run_id);
CREATE INDEX idx_agent_reports_agent ON agent_reports(agent);

-- Evidence table
CREATE TABLE evidence (
    id UUID PRIMARY KEY,
    agent_report_id UUID NOT NULL REFERENCES agent_reports(id) ON DELETE CASCADE,
    agent VARCHAR(100) NOT NULL,
    claim TEXT NOT NULL,
    source_url TEXT,
    source_type VARCHAR(50) NOT NULL,
    retrieved_at TIMESTAMP NOT NULL,
    confidence FLOAT NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    raw_excerpt TEXT NOT NULL
);

CREATE INDEX idx_evidence_agent_report ON evidence(agent_report_id);
CREATE INDEX idx_evidence_source_type ON evidence(source_type);
CREATE INDEX idx_evidence_confidence ON evidence(confidence DESC);

-- API cost tracking table
CREATE TABLE api_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES runs(run_id) ON DELETE CASCADE,
    agent VARCHAR(100),
    provider VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    tokens_in INTEGER NOT NULL,
    tokens_out INTEGER NOT NULL,
    cost_usd DECIMAL(10, 6) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_costs_run ON api_costs(run_id);
CREATE INDEX idx_costs_provider ON api_costs(provider);
CREATE INDEX idx_costs_created_at ON api_costs(created_at DESC);

-- Company profiles table (for Phase 1+)
CREATE TABLE company_profiles (
    company_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ticker VARCHAR(20),
    website TEXT,
    last_updated TIMESTAMP NOT NULL DEFAULT NOW(),
    narrative JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_company_ticker ON company_profiles(ticker);

-- Debate results table (for Phase 3)
CREATE TABLE debates (
    debate_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID REFERENCES runs(run_id) ON DELETE CASCADE,
    claim TEXT NOT NULL,
    consensus_reached BOOLEAN NOT NULL DEFAULT FALSE,
    final_verdict VARCHAR(50),
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    summary TEXT,
    turns JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_debates_run ON debates(run_id);

-- Predictions table (for Phase 4)
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    prediction TEXT NOT NULL,
    confidence FLOAT NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    reasoning TEXT,
    evidence_ids JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolve_by TIMESTAMP,
    resolved BOOLEAN NOT NULL DEFAULT FALSE,
    actual_outcome TEXT
);

CREATE INDEX idx_predictions_company ON predictions(company_id);
CREATE INDEX idx_predictions_resolved ON predictions(resolved);

-- Create a view for run statistics
CREATE VIEW run_stats AS
SELECT
    r.run_id,
    r.company_name,
    r.status,
    r.started_at,
    r.completed_at,
    COUNT(DISTINCT ar.id) as agent_count,
    COUNT(DISTINCT e.id) as evidence_count,
    AVG(e.confidence) as avg_confidence,
    COALESCE(SUM(ac.cost_usd), 0) as total_cost_usd
FROM runs r
LEFT JOIN agent_reports ar ON r.run_id = ar.run_id
LEFT JOIN evidence e ON ar.id = e.agent_report_id
LEFT JOIN api_costs ac ON r.run_id = ac.run_id
GROUP BY r.run_id, r.company_name, r.status, r.started_at, r.completed_at;

-- Insert sample data for testing (optional)
-- Uncomment to pre-populate with test data
/*
INSERT INTO runs (run_id, company_id, company_name, status, started_at)
VALUES (uuid_generate_v4(), 'anthropic', 'Anthropic', 'completed', NOW() - INTERVAL '1 hour');
*/
