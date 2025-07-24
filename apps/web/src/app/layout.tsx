import type { Metadata } from 'next';
import Providers from '@/components/providers';
import './globals.css';

export const metadata: Metadata = {
  title: 'DROP.AZ - Dərmanları evə çatdırırıq',
  description: 'Azərbaycanda ilk professional dərman çatdırılma platforması',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="az">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}