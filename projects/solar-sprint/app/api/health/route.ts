import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function GET(req: NextRequest) {
  const timestamp = new Date().toISOString();
  let dbStatus: 'ok' | 'error' = 'error';

  try {
    await prisma.$queryRaw`SELECT 1`;
    dbStatus = 'ok';
  } catch (e) {
    // Handle DB error explicitly
  }

  return NextResponse.json({
    status: 'ok',
    service: 'solar-sprint',
    timestamp,
    db: dbStatus,
  });
}