# Proxecto Integrador - Document Upload Application

A modern, full-stack Next.js application for uploading and managing documents with processing options.

## 🚀 Quick Start

### Prerequisites
- **Node.js**: v18.x or higher
- **npm**: v9.x or higher (or pnpm v8.x+)
- **Git**: For version control

### Installation Steps

1. **Clone or Extract the Project**
   \`\`\`bash
   # If extracted from ZIP
   cd proxecto-integrador
   
   # Or if cloned from Git
   git clone <repository-url>
   cd proxecto-integrador
   \`\`\`

2. **Install Dependencies**
   \`\`\`bash
   npm install
   # or
   pnpm install
   \`\`\`

3. **Run Development Server**
   \`\`\`bash
   npm run dev
   # or
   pnpm dev
   \`\`\`

4. **Open in Browser**
   Navigate to `http://localhost:3000`

## 📁 Project Structure

\`\`\`
proxecto-integrador/
├── app/
│   ├── layout.tsx              # Root layout with metadata
│   ├── page.tsx                # Main page with document upload
│   └── globals.css             # Global styles and theme
├── components/
│   ├── document-uploader.tsx   # File upload component
│   ├── document-options.tsx    # Processing options component
│   ├── theme-provider.tsx      # Theme context provider
│   └── ui/                     # Reusable UI components (shadcn)
├── hooks/
│   ├── use-mobile.ts           # Mobile detection hook
│   └── use-toast.ts            # Toast notifications hook
├── lib/
│   └── utils.ts                # Utility functions and cn() helper
├── public/
│   ├── icon.svg                # Application icon
│   ├── placeholder.svg         # Placeholder images
│   └── apple-icon.png          # Apple touch icon
├── styles/
│   └── globals.css             # Additional global styles
├── next.config.mjs             # Next.js configuration
├── tsconfig.json               # TypeScript configuration
├── postcss.config.mjs          # PostCSS configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── package.json                # Dependencies and scripts
└── components.json             # shadcn/ui configuration
\`\`\`

## 🛠️ Available Scripts

\`\`\`bash
# Development server (with hot reload)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Run ESLint
npm run lint
\`\`\`

## 📦 Tech Stack

### Core
- **Next.js 16**: React framework with App Router
- **React 19**: UI library with new hooks
- **TypeScript**: Type-safe development

### Styling
- **Tailwind CSS v4**: Utility-first CSS framework
- **PostCSS**: CSS transformation
- **next-themes**: Dark mode support

### UI Components
- **shadcn/ui**: High-quality accessible components
- **Radix UI**: Primitive components for accessibility
- **Lucide React**: Beautiful icon library

### Forms & Validation
- **React Hook Form**: Efficient form handling
- **Zod**: Schema validation
- **@hookform/resolvers**: Form validation resolvers

### Other
- **Vercel Analytics**: Usage tracking
- **Sonner**: Toast notifications
- **Date-fns**: Date manipulation
- **Recharts**: Data visualization

## 🎨 Design System

The app uses a cohesive design system with:
- **Color Scheme**: Primary purple with neutral grays
- **Typography**: Geist font family for clean, modern text
- **Components**: Reusable UI components from shadcn/ui
- **Spacing**: Tailwind spacing scale (consistent 4px grid)
- **Responsive**: Mobile-first design with breakpoints

## 🔧 Configuration Files

### `next.config.mjs`
- TypeScript build error handling
- Image optimization settings

### `tsconfig.json`
- TypeScript compiler options
- Path aliases (@/* for root imports)

### `tailwind.config.ts`
- Tailwind CSS customization
- Theme colors and typography
- Custom plugins

### `postcss.config.mjs`
- Tailwind CSS PostCSS plugin configuration

### `components.json`
- shadcn/ui component configuration

## 🚀 Features

- ✅ Drag-and-drop file upload
- ✅ Multiple document management
- ✅ Processing options (OCR, compression, conversion, etc.)
- ✅ Responsive design (mobile & desktop)
- ✅ Accessible UI components
- ✅ Dark mode support
- ✅ Real-time file list updates

## 📝 Environment Variables

This project doesn't require environment variables for basic functionality. If you add backend services (database, API), add them to `.env.local`:

\`\`\`env
# .env.local (never commit this file)
NEXT_PUBLIC_API_URL=http://localhost:3000
# Add other variables as needed
\`\`\`

## 🐛 Troubleshooting

**Port 3000 already in use?**
\`\`\`bash
npm run dev -- -p 3001
\`\`\`

**Module not found errors?**
\`\`\`bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
\`\`\`

**Styles not loading?**
\`\`\`bash
# Rebuild Tailwind CSS
npm run build
\`\`\`

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues or questions, please check the documentation or open an issue in the repository.
