import prisma from '@/lib/prisma';

export async function getCurrentUser(request: Request) {
  const userId = request.headers.get('x-user-id');

  if (!userId) {
    return null;
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      email: true,
      tenantId: true,
    },
  });

  return user ?? null;
}
