-- Create the examples table
CREATE TABLE IF NOT EXISTS examples (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  framework TEXT NOT NULL,
  files JSONB NOT NULL DEFAULT '{}',
  dependencies JSONB NOT NULL DEFAULT '{}',
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE examples ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access
CREATE POLICY "Allow public read access" ON examples FOR SELECT USING (true);

-- Create policy for authenticated insert/update (if needed)
-- CREATE POLICY "Allow authenticated insert" ON examples FOR INSERT WITH CHECK (auth.role() = 'authenticated');
