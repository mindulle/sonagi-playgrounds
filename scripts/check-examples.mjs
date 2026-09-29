import fs from 'fs';
import path from 'path';

const examplesDir = path.join(process.cwd(), 'examples');
let hasError = false;

function traverse(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (['node_modules', 'dist', '.git', '__pycache__'].includes(entry.name)) continue;
      const fullPath = path.join(dir, entry.name);
      
      const hasPackageJson = fs.existsSync(path.join(fullPath, 'package.json'));
      const hasIndexHtml = fs.existsSync(path.join(fullPath, 'index.html'));
      
      // We consider it an "example project" if it has either package.json or index.html
      // (Ignoring the root of examples/ or mid-level folders that don't have them)
      if (hasPackageJson || hasIndexHtml) {
        if (!hasPackageJson) {
          console.error(`❌ Missing package.json in ${fullPath}`);
          hasError = true;
        } else {
          try {
            JSON.parse(fs.readFileSync(path.join(fullPath, 'package.json'), 'utf-8'));
          } catch (e) {
            console.error(`❌ Invalid package.json in ${fullPath}: ${e.message}`);
            hasError = true;
          }
        }
        
        if (!hasIndexHtml) {
          console.error(`❌ Missing index.html in ${fullPath}`);
          hasError = true;
        }
        
        if (hasPackageJson && hasIndexHtml) {
          console.log(`✅ Validated: ${fullPath}`);
        }
      } else {
        // Traverse deeper to find actual example projects
        traverse(fullPath);
      }
    }
  }
}

console.log('🔍 Starting Sanity Check for examples...');
if (fs.existsSync(examplesDir)) {
  traverse(examplesDir);
} else {
  console.log('No examples directory found.');
}

if (hasError) {
  console.error('💥 Sanity check failed! AI bot might have generated invalid examples.');
  process.exit(1);
} else {
  console.log('🎉 All examples passed sanity check!');
}
