# Contributing Guidelines

## Code Standards

### TypeScript
- Use strict mode (enforced in tsconfig.json)
- Define types for all props and returns
- Avoid `any` type

### React Components
- Functional components only
- Use hooks for state management
- Memoize components when appropriate
- Keep components focused and single-purpose

### Styling
- Use Tailwind classes (avoid inline styles)
- Follow mobile-first responsive design
- Maintain consistent spacing (4px grid)
- Use design tokens from globals.css

### File Structure
\`\`\`
components/
├── feature-name.tsx        # Component logic
├── feature-name.test.tsx   # Tests (when applicable)
└── index.ts               # Barrel export (optional)
\`\`\`

## Commit Messages

Use conventional commits:
\`\`\`
feat: add new feature
fix: fix a bug
docs: documentation changes
style: formatting changes
refactor: code restructuring
test: add or update tests
chore: maintenance tasks
\`\`\`

## Pull Request Process

1. Create feature branch from `develop`
2. Make changes following code standards
3. Test thoroughly in development
4. Submit PR with clear description
5. Address review feedback
6. Merge after approval

## Testing

\`\`\`bash
# Run tests (when configured)
npm test

# Run linter
npm run lint

# Type check
npx tsc --noEmit
