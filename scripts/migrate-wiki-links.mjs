import fs from 'fs';

const filePath = '/home/ubuntu/llm-wiki/03_Resources/References/Code_Examples.md';

let content = fs.readFileSync(filePath, 'utf-8');

const originalContent = content;

// Replace CodeSandbox URLs
content = content.replace(
  /https:\/\/codesandbox\.io\/s\/github\/hotssi\/sandbox\/tree\/master\//g,
  'https://codesandbox.io/s/github/mindulle/sonagi-playgrounds/tree/main/examples/'
);

// Replace GitHub URLs
content = content.replace(
  /https:\/\/github\.com\/hotssi\/sandbox/g,
  'https://github.com/mindulle/sonagi-playgrounds'
);

// Replace plain text mentions
content = content.replace(/hotssi\/sandbox/g, 'sonagi-playgrounds');

if (content !== originalContent) {
  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`✅ Updated links in ${filePath}`);
} else {
  console.log(`No changes made to ${filePath}`);
}
