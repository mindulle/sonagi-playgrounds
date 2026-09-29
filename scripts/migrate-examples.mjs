import fs from 'fs';
import path from 'path';

const examplesDir = path.join(process.cwd(), 'examples');
let modifiedCount = 0;

function traverse(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (['node_modules', 'dist', '.git', '__pycache__'].includes(entry.name)) continue;
      traverse(path.join(dir, entry.name));
    } else if (entry.name === 'index.html') {
      const fullPath = path.join(dir, entry.name);
      let content = fs.readFileSync(fullPath, 'utf-8');
      
      // Simple regex to add type="module" to any <script> tag that has a src but lacks type="module"
      let updated = content;
      updated = updated.replace(/<script(?![^>]*type="module")[^>]*src=(['"])(.*?)\1[^>]*><\/script>/gi, (match) => {
        return match.replace('<script ', '<script type="module" ');
      });

      if (updated !== content) {
        fs.writeFileSync(fullPath, updated, 'utf-8');
        console.log(`✅ Patched type="module" in: ${fullPath}`);
        modifiedCount++;
      }
    }
  }
}

traverse(examplesDir);
console.log(`\n🎉 Migration complete! Modified ${modifiedCount} index.html files.`);
