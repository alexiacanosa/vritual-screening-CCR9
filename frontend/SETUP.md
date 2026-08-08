# Local Development Setup Guide

## Initial Setup

### 1. System Requirements
- Node.js 18.x or higher
- npm 9.x or pnpm 8.x (yarn also supported)
- 2GB minimum disk space
- Modern browser (Chrome, Firefox, Safari, Edge)

### 2. Installation

\`\`\`bash
# Install Node.js from https://nodejs.org/

# Clone/extract project
cd proxecto-integrador

# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

### 3. Verify Installation

Visit `http://localhost:3000` and you should see:
- Header: "Proxecto Integrador"
- Document upload area on the left
- Processing options on the right
- File list below the upload area

## Development Workflow

### Adding New Dependencies

\`\`\`bash
# Install new package
npm install package-name

# Install dev dependency
npm install --save-dev package-name

# Update all packages
npm update
\`\`\`

### Code Style

- **Formatting**: Prettier (configured in `.prettierrc`)
- **Linting**: ESLint (Next.js config)
- **Type Checking**: TypeScript strict mode

### Git Workflow

\`\`\`bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: description of changes"

# Push to remote
git push origin feature/your-feature-name
\`\`\`

## Building for Production

\`\`\`bash
# Create optimized build
npm run build

# Test production build locally
npm start

# Visit http://localhost:3000
\`\`\`

## Environment Setup

1. Copy `.env.example` to `.env.local`:
   \`\`\`bash
   cp .env.example .env.local
   \`\`\`

2. Update `.env.local` with your values (don't commit this file)

3. Restart dev server after changing env vars

## Debugging

### Enable Debug Logging

\`\`\`typescript
// In your component
console.log('[v0] Debug message:', data);
\`\`\`

### Next.js Debug Mode

\`\`\`bash
DEBUG=* npm run dev
\`\`\`

### Browser DevTools

- Open DevTools: F12 or Right-click → Inspect
- Check Console for errors
- Use React DevTools extension for component debugging

## Performance Optimization

### Lighthouse Audit

\`\`\`bash
# In production build
npm run build
npm start

# Run Lighthouse in Chrome DevTools
\`\`\`

### Bundle Analysis

\`\`\`bash
# Install next-bundle-analyzer
npm install @next/bundle-analyzer

# Add to next.config.mjs and rebuild
\`\`\`

## Deployment

### Vercel (Recommended)

\`\`\`bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
\`\`\`

### Other Platforms

1. Build: `npm run build`
2. Start command: `npm start`
3. Environment variables: Set in platform dashboard
4. Node version: 18.x or higher

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `npm run dev -- -p 3001` |
| Module not found | Delete `.next` folder, reinstall dependencies |
| Styles not loading | Check `app/globals.css` imports |
| Hot reload not working | Restart dev server |
| TypeScript errors | Run `npx tsc --noEmit` for full report |

## Support & Resources

- Next.js: https://nextjs.org/docs
- TypeScript: https://www.typescriptlang.org/docs
- Tailwind: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com
