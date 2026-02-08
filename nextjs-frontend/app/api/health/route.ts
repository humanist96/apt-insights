/**
 * Next.js Health Check API Route
 *
 * Provides health status for the Next.js frontend application.
 * Used by load balancers, monitoring tools, and deployment platforms.
 */

import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'nextjs-frontend',
    version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV,
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'not-configured',
  });
}

export const runtime = 'edge';
