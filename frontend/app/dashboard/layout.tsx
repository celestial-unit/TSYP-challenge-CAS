'use client';

import { Sidebar } from '@/components/dashboard';
import DashboardAuthWrapper from './auth-wrapper';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <DashboardAuthWrapper>
      <div className="flex h-screen overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-muted/10">
          {children}
        </main>
      </div>
    </DashboardAuthWrapper>
  );
}
