import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'EcoScholar — Learn for a living planet', description: 'Evidence-led sustainability learning and environmental intelligence.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
