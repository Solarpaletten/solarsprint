import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { hashPassword } from '@/lib/auth/password';


export async function POST(request: NextRequest) {
  const body = await request.json();

  const { email, password, tenantName } = body;

  if (!email || !password || !tenantName) {
    return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
  }

  try {
    // Create new Tenant
    const tenant = await prisma.tenant.create({
      data: {
        name: tenantName,
      },
    });

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);

    // Create first User linked to Tenant
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash: hashedPassword,
        tenantId: tenant.id,
      },
    });

    return NextResponse.json({
      userId: user.id,
      email: user.email,
      tenantId: tenant.id,
    });
  } catch (error) {
    console.error('Signup error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}