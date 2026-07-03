const fs = require('fs');
const path = require('path');

const ROOT_DIR = process.cwd();
const OUTPUT_FILE = path.join(ROOT_DIR, 'examples_data.json');

// Files to ignore (boilerplate)
const IGNORE_FILES = [
  'index.js',
  'README.md',
  '.gitignore',
  'package-lock.json',
  'node_modules'
];

// Common boilerplates to check against (if md5 is too complex, we'll just check content or ignore by name)
const isBoilerplateIndex = (content) => {
  return content.includes('react-dom/client') && content.includes('<App />');
};

function getFiles(dir, relativeTo) {
  let results = {};
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const relPath = path.relative(relativeTo, filePath);
    const stat = fs.statSync(filePath);

    if (stat && stat.isDirectory()) {
      if (!IGNORE_FILES.includes(file)) {
        Object.assign(results, getFiles(filePath, relativeTo));
      }
    } else {
      if (!IGNORE_FILES.includes(file)) {
        const content = fs.readFileSync(filePath, 'utf8');
        // Simple heuristic to skip boilerplate index.js in src/
        if (file === 'index.js' && relPath.includes('src/') && isBoilerplateIndex(content)) {
          return;
        }
        results[relPath] = content;
      }
    }
  });
  return results;
}

const isExampleFolder = (list) => {
  return list.includes('package.json') || list.includes('index.html') || list.includes('demo.html');
};

function migrate() {
  const examples = [];
  const walk = (dir) => {
    const list = fs.readdirSync(dir);
    if (isExampleFolder(list)) {
      let pkg = {};
      const pkgPath = path.join(dir, 'package.json');
      if (fs.existsSync(pkgPath)) {
        pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      }
      
      const relDir = path.relative(ROOT_DIR, dir);
      
      const parts = relDir.split(path.sep);
      // Path format: component/[react|vanilla]/[category]/[name] or Vanilla/[category]/...
      let framework = 'vanilla';
      let category = 'general';
      let name = parts[parts.length - 1];

      if (parts[0] === 'component') {
        framework = parts[1];
        category = parts[2] || 'general';
      } else if (parts[0] === 'Vanilla') {
        framework = 'vanilla';
        category = parts[1] || 'general';
      } else if (parts[0] === 'patterns') {
        framework = 'vanilla';
        category = parts[1] || 'general';
      }

      console.log(`Extracting: [${framework}] ${category}/${name}...`);

      const files = getFiles(dir, dir);
      
      examples.push({
        name,
        category,
        framework,
        dependencies: pkg.dependencies || {},
        files,
        original_path: relDir
      });
      return;
    }

    list.forEach(file => {
      const filePath = path.join(dir, file);
      if (fs.statSync(filePath).isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
        walk(filePath);
      }
    });
  };


  walk(ROOT_DIR);

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(examples, null, 2));
  console.log(`\nFinished! Total examples found: ${examples.length}`);
  console.log(`Data saved to: ${OUTPUT_FILE}`);
}

migrate();
