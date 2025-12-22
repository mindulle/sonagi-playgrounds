# Migration from Git Repository to Supabase for CodeSandbox Examples

## Goal

Transition the current file-based example repository (redundant project structures) to a database-driven approach using Supabase and CodeSandbox (specifically the **Sandpack SDK**).

## Background

The current repository contains over 1,000 files across multiple categories (`component`, `Vanilla`, etc.). Most of these are individual project structures with identical configuration files. The primary purpose is to allow users to view and edit examples via a sandbox environment.

## Proposed Architecture

### 1. Supabase Schema

We can store the snippets in a relational database for better organization and search.

- **Table: `examples`**
  - `id`: UUID (Primary Key)
  - `name`: String (e.g., "CountdownTimer")
  - `category`: String (e.g., "display", "hooks")
  - `framework`: String (e.g., "react", "vanilla")
  - `files`: JSONB (Mapped file paths to content)
  - `dependencies`: JSONB (Overrides for `package.json`)
  - `metadata`: JSONB (Tags, descriptions, difficulty)
  - `created_at`: Timestamp

### 2. CodeSandbox (Sandpack) Integration

Instead of fixed GitHub URLs, we use `@codesandbox/sandpack-react` (or the vanilla JS equivalent) to render the sandbox dynamically from DB content.

```javascript
import { Sandpack } from "@codesandbox/sandpack-react";

const ExampleSandbox = ({ example }) => {
  return (
    <Sandpack
      template={example.framework === "react" ? "react" : "vanilla"}
      files={{
        ...example.files,
        // Optional: override specific files
      }}
      customSetup={{
        dependencies: {
          ...DEFAULT_DEPENDENCIES,
          ...example.dependencies,
        },
      }}
    />
  );
};
```

> [!TIP] > **Sandpack** is extremely powerful because it runs the bundler in the browser, providing a much faster and more integrated experience than traditional iframe-based sandboxes.

## Pros and Cons

| Feature        | Current (GitHub)               | Proposed (Supabase + CodeSandbox) |
| :------------- | :----------------------------- | :-------------------------------- |
| **Storage**    | Highly Redundant (1000+ files) | Lean (Only source code)           |
| **UX**         | External Redirect (StackBlitz) | Inline or External (Sandpack)     |
| **Search**     | Limited to File Search         | Powerful SQL Search / Tags        |
| **Updates**    | `git push`                     | API call / Admin Dashboard        |
| **Setup Cost** | Low                            | Medium (Requires Frontend)        |

## Implementation Steps

1. **Extraction Script**: Create a script to traverse the current repository, extract the "unique" source code, and upload it to Supabase.
2. **Template Definition**: Define standard templates for React (Sandpack `react`) and Vanilla JS (Sandpack `vanilla`) to avoid redundant file storage.
3. **Gallery UI**: Build a frontend (e.g., Next.js) that fetches examples from Supabase and renders them using the `Sandpack` component.
4. **Maintenance Tool**: A CLI tool to "push" local changes to the Supabase database.

## Recommendation

If you plan to scale these examples significantly or want to build a "UI Library Documentation" (like Shadcn or Radix documentation), **moving to Supabase is highly recommended**. It allows for a more professional and manageable data structure.

If you just want a quick and dirty way to host files and don't care about redundancy, Git is fine. However, since you're already asking, you likely feel the weight of managing thousands of redundant files.
