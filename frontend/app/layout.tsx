import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HarvestGuard AI | Predict. Protect. Preserve.",
  description: "Advisory monitoring and predictive-risk tools for solar-powered agricultural cold storage.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
