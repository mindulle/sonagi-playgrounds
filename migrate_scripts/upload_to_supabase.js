/**
 * Usage: SUPABASE_URL=xxx SUPABASE_KEY=yyy node migrate_scripts/upload_to_supabase.js
 */

const fs = require('fs');
const path = require('path');

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY; // Use Service Role Key for migration

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error("Error: Please provide SUPABASE_URL and SUPABASE_KEY environment variables.");
  process.exit(1);
}

const DATA_FILE = path.join(process.cwd(), 'examples_data.json');

async function upload() {
  if (!fs.existsSync(DATA_FILE)) {
    console.error(`Error: ${DATA_FILE} not found. Run extract_examples.js first.`);
    return;
  }

  const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  console.log(`Uploading ${data.length} examples to ${SUPABASE_URL}...`);

  for (const item of data) {
    try {
      console.log(`Uploading [${item.framework}] ${item.category}/${item.name}...`);
      const response = await fetch(`${SUPABASE_URL}/rest/v1/examples`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Prefer': 'resolution=merge-duplicates' // Optional: upsert if you have a unique constraint
        },
        body: JSON.stringify({
          name: item.name,
          category: item.category,
          framework: item.framework,
          files: item.files,
          dependencies: item.dependencies,
          metadata: { original_path: item.original_path }
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`Failed to upload ${item.name}: ${response.statusText} - ${errorText}`);
      }
    } catch (err) {
      console.error(`Error during upload of ${item.name}:`, err.message);
    }
  }

  console.log("\nMigration complete!");
}

upload();
