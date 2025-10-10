/**
 * Frame of the website:
 * - Create basic HTML structure that wraps around EVERY page in Next.js app
 */

import type { Metadata } from "next"; // import type def from Next.js
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Font setup
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Blankey's Generate AI-powered captions for your images",
  description: "Generate AI-powered captions for your images",
};

export default function RootLayout({
  children, // Destructuring, func receives a "props" object
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
        {/* placeholder is where your actual page content (like page.tsx) gets inserted */}
      </body>
    </html>
  );
}
